# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Contains the hook_point, the code actually executed in place of
application code
"""
import logging
import sys
from traceback import extract_stack

from .._vendors.wrapt import FunctionWrapper
from ..constants import ACTIONS, LIFECYCLE_METHODS, VALID_ACTIONS_PER_LIFECYCLE
from ..exceptions import (
    ActionBlock,
    ActionRedirect,
    AttackBlocked,
    MissingDataException,
    SqreenException,
)
from ..remote_exception import RemoteException
from ..runtime_storage import runtime
from ..utils import Iterable, Mapping
from .helpers import guard_call

LOGGER = logging.getLogger(__name__)


def _compute_result_action(current_result, next_result, valid_actions):
    """ Compute the next result_action based on current one and the callback
    result
    """
    current_status = current_result.get("status")
    next_status = next_result.get("status")
    # Check the validity of action per method
    if next_status not in valid_actions:
        # Ignore it
        return current_result

    if current_status not in valid_actions:
        return next_result

    current_result_order = valid_actions.index(current_result.get("status"))
    next_result_order = valid_actions.index(next_result.get("status"))

    # Return the old one only if it has more priority
    if current_result_order < next_result_order:
        return current_result
    else:
        return next_result


def valid_args(new_args):
    """ Check that new_args match the format ([], {}), else returns None
    """
    try:
        args, kwargs = new_args
    except (TypeError, ValueError):
        msg = "Invalid number of args or type, %s"
        LOGGER.debug(msg, new_args)
        return False

    # Check that new_args[0] is a valid type for passing to *
    if not isinstance(args, Iterable) or isinstance(args, Mapping):
        msg = "Invalid type for args[0]: %s"
        LOGGER.debug(msg, args)
        return False

    # Check that new_args[1] is a valid type for passing to **
    if not isinstance(kwargs, Mapping):
        msg = "Invalid type for args[1]: %s"
        LOGGER.debug(msg, kwargs)
        return False

    return True


def execute_callback(
    queue, callback, method, instance, result_action, args, kwargs,
    storage=runtime, override_budget=None, **options
):
    """ Execute a callback protected inside a broad try except.

    The queue argument is used to push a RemoteException when an exception is raised by the callback.
    The result_action argument is a dict where each callback pushes its results.
    """

    callback_method = getattr(callback, method)

    if args is None:
        args = tuple()

    if kwargs is None:
        kwargs = {}

    if override_budget is not None and callback.collaborative:
        options["__sqreen_override_budget"] = override_budget

    if result_action:
        # Give access to the previous callbacks result action
        # For example, it allows a callback to know if the return value
        # will be overwritten or if the args have been changed
        options["result_action"] = result_action

    try:
        result = callback_method(instance, args, kwargs, **options)

        # First process of result
        if not result or not isinstance(result, dict):
            return result_action, args, kwargs

        # Update the request store
        data = result.pop("request_store", None)
        if data:
            storage.update_request_store(data)

        if not callback.block:
            LOGGER.debug("%s cannot block, ignoring return value", callback)
            return result_action, args, kwargs

        # Set rule_name if not set
        result.setdefault("rule_name", callback.rule_name)

        valid_actions = VALID_ACTIONS_PER_LIFECYCLE[method]
        result_action = _compute_result_action(
            result_action, result, valid_actions
        )

        # We need to process MODIFY_ARGS for next callbacks
        if result_action.get("status") == ACTIONS["MODIFY_ARGS"]:
            if valid_args(result_action["args"]):
                args, kwargs = result_action["args"]

        return result_action, args, kwargs

    except MissingDataException:
        raise

    except Exception as exception:
        LOGGER.exception(
            "An exception occurred while trying to execute %s", callback
        )

        exc_info = sys.exc_info()
        current_request = storage.get_current_request()
        stack = extract_stack()

        if current_request:
            callback.record_exception(exception, exc_info, stack)
        else:
            callback_exception_payload = callback.exception_infos()

            # Try to recover some infos from the exception if it's a SqreenException
            exception_infos = {}
            if isinstance(exception, SqreenException):
                exception_infos.update(exception.exception_infos())  # pylint: disable=no-member

            remote_exception = RemoteException.from_exc_info(
                exc_info,
                callback_payload=callback_exception_payload,
                exception_payload=exception_infos,
                stack=stack,
            )
            queue.put(remote_exception)

        return result_action, args, kwargs


def execute_callbacks(
    queue, callbacks, method, instance, args=None, kwargs=None,
    storage=runtime, override_budget=None, **options
):
    """ Execute a list of callbacks method (pre/post/fail), catch any exception
    that could happens.

    Aggregate the callbacks result (format {"status": COMMAND}), compute the
    final ACTION to execute and return it.
    For every ACTION, each callback is executed even if the first callback
    detected an attack except specified otherwise with the "immediate" key.

    The performance cap budget can be ignored by the caller by specifying an
    `override_budget` value though it is currently only used by the PHP daemon.
    """
    result_action = {}
    # Test if override_budget is already negative
    overtime = override_budget <= 0 if override_budget is not None else None
    total_duration = 0
    budget = None

    # Execute the callbacks
    for callback in callbacks:

        if callback.whitelisted:
            continue

        # Budget must be updated before executing the first callback
        if overtime is None and budget is None:
            budget = override_budget or callback.get_remaining_budget()
            overtime = budget <= 0 if budget is not None else False

        # Budget is exhausted, skip the callback if possible
        if overtime and callback.skippable:
            callback.record_overtime(lifecycle=method)
            continue

        with storage.trace() as callback_trace:
            result = execute_callback(
                queue, callback, method, instance, result_action, args, kwargs,
                storage=storage, override_budget=budget, **options
            )

        result_action, args, kwargs = result

        total_duration += callback_trace.duration_ms
        if budget is not None:
            budget -= callback_trace.duration_ms
            overtime = budget <= 0
            if overtime:
                callback.record_overtime(lifecycle=method)

        if result_action.get("immediate", False):
            # Stop execution of other callbacks on this hook point if the result must be immediate.
            break

    # It is either empty dict if no override or the last one
    return result_action


def execute_pre_callbacks(
    key, strategy, instance, args=None, kwargs=None, storage=runtime,
    override_budget=None
):
    """ Execute pre_callbacks. Pre callbacks will receive these arguments:
    (instance, args, kwargs)
    """
    pre_callbacks = strategy.get_pre_callbacks(key)
    if pre_callbacks:
        return guard_call(
            key,
            execute_callbacks,
            strategy.queue,
            pre_callbacks,
            LIFECYCLE_METHODS["PRE"],
            instance,
            args,
            kwargs,
            storage=storage,
            override_budget=override_budget,
        )
    return {}


def execute_failing_callbacks(
    key, strategy, instance, exc_info, args=None, kwargs=None, storage=runtime,
    override_budget=None
):
    """ Execute failing_callbacks. Failing callbacks will receive these arguments:
    (instance, args, kwargs, exc_info=exc_info)
    """
    failing_callbacks = strategy.get_failing_callbacks(key)
    if failing_callbacks:
        return guard_call(
            key,
            execute_callbacks,
            strategy.queue,
            failing_callbacks,
            LIFECYCLE_METHODS["FAILING"],
            instance,
            args,
            kwargs,
            exc_info=exc_info,
            storage=storage,
            override_budget=override_budget,
        )
    return {}


def execute_post_callbacks(
    key, strategy, instance, result, args=None, kwargs=None, storage=runtime,
    override_budget=None
):
    """ Execute post_callbacks. Post callbacks will receive these arguments:
    (instance, args, kwargs, result=result)
    """
    post_callbacks = strategy.get_post_callbacks(key)
    if post_callbacks:
        return guard_call(
            key,
            execute_callbacks,
            strategy.queue,
            post_callbacks,
            LIFECYCLE_METHODS["POST"],
            instance,
            args,
            kwargs,
            result=result,
            storage=storage,
            override_budget=override_budget,
        )
    return {}


def hook_point_wrapper(strategy, hook_name, hook_method, storage=runtime):
    """ Execute the original method and pre/post/failing callbacks
    If an exception happens, create a RemoteException, call
    callback.exception_infos for more debugging infos and send it via
    the provided queue.
    """
    key = (hook_name, hook_method)

    def wrapper(wrapped, instance, args, kwargs):
        strategy.before_hook_point()

        # Call pre callbacks
        action = execute_pre_callbacks(
            key,
            strategy,
            instance,
            args,
            kwargs,
            storage=storage
        )

        if action.get("status") == ACTIONS["RAISE"]:
            LOGGER.debug(
                "Callback %s detected an attack", action.get("rule_name")
            )
            raise AttackBlocked(action.get("rule_name"))
        elif action.get("status") == ACTIONS["ACTION_BLOCK"]:
            LOGGER.debug(
                "Action %s blocked the request", action.get("action_id")
            )
            raise ActionBlock(action.get("action_id"))
        elif action.get("status") == ACTIONS["ACTION_REDIRECT"]:
            LOGGER.debug(
                "Action %s redirected the request to %r",
                action.get("action_id"),
                action["target_url"],
            )
            raise ActionRedirect(action.get("action_id"), action["target_url"])
        elif action.get("status") == ACTIONS["OVERRIDE"]:
            return action.get("new_return_value")
        elif action.get("status") == ACTIONS["MODIFY_ARGS"]:
            if valid_args(action["args"]):
                args, kwargs = action["args"]

        # Call original method
        retry = True
        while retry is True:
            try:
                retry = False
                # Try to call original function
                result = wrapped(*args, **kwargs)
            except Exception:
                # In case of error, call fail callbacks with exception infos
                exc_info = sys.exc_info()

                # Either raise an exception, set a return value or retry
                action = execute_failing_callbacks(
                    key, strategy, instance, exc_info, args, kwargs,
                    storage=storage
                )

                if action.get("status") == ACTIONS["RAISE"]:
                    LOGGER.debug(
                        "Callback %s detected an attack",
                        action.get("rule_name"),
                    )
                    raise AttackBlocked(action.get("rule_name"))
                elif action.get("status") == ACTIONS["RETRY"]:
                    retry = True
                elif action.get("status") == ACTIONS["OVERRIDE"]:
                    return action.get("new_return_value")

                # Be sure to raise if no retry or override
                if retry is False:
                    raise

        # Then call post callback in reverse order to simulate decorator
        # behavior
        action = execute_post_callbacks(
            key, strategy, instance, result, args, kwargs, storage=storage,
        )

        if action.get("status") == ACTIONS["RAISE"]:
            LOGGER.debug(
                "Callback %s detected an attack", action.get("rule_name")
            )
            raise AttackBlocked(action.get("rule_name"))
        elif action.get("status") == ACTIONS["OVERRIDE"]:
            return action.get("new_return_value")

        # And return the original value
        return result
    return wrapper


def hook_point(strategy, hook_name, hook_method, original, storage=runtime):
    wrapper = hook_point_wrapper(strategy, hook_name, hook_method, storage)
    return FunctionWrapper(original, wrapper)

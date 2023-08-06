"""Aporia SDK.

Usage:
    >>> import aporia
    >>> aporia.init(
    >>>     token='12345',
    >>>     host='production.myorg.cloud.aporia.com',
    >>>     port=443,
    >>>     environment="production"
    >>> )
    >>> model = aporia.Model(model_name='my-model'], model_version='v1')
    >>> model.set_features(feature_names=['x1', 'x2', 'x3'], categorical=['x2'])
    >>> model.log_predict(x=[1.3, 0.7, 0.2], y=[0.09])
"""
from dataclasses import dataclass
import logging
import sys
from typing import Optional

from aporia.consts import LOG_FORMAT, LOGGER_NAME
from aporia.errors import AporiaError
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient
from aporia.model import Model

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


__all__ = ["init", "flush", "Model"]


@dataclass
class Context:
    """Global context."""

    graphql_client: GraphQLClient
    event_loop: EventLoop
    environment: str
    debug: bool
    throw_errors: bool


context: Optional[Context] = None
logger = logging.getLogger(LOGGER_NAME)


def init(
    token: str,
    host: str,
    port: int,
    environment: str,
    debug: bool = False,
    throw_errors: bool = False,
):
    """Initializes the Aporia SDK.

    Args:
        token (str): Authentication token.
        host (str): Controller host.
        port (int): Controller port.
        environment (str): Controller environment name.
        debug (bool): True to enable debug mode - this will cause additional logs
            and stack traces during exceptions. Defaults to False.
        throw_errors (bool): True to cause errors to be raised as exceptions. Defaults to False.
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, style="{"))
    logger.addHandler(handler)

    logger.debug("Initializing Aporia SDK.")

    try:
        # Init graphql client and event loop
        event_loop = EventLoop()
        graphql_client = GraphQLClient(token=token, host=host, port=port)
        event_loop.run_coroutine(graphql_client.open())

        global context
        context = Context(
            graphql_client=graphql_client,
            event_loop=event_loop,
            environment=environment.strip().lower(),
            debug=debug,
            throw_errors=throw_errors,
        )
        logger.debug("Aporia SDK initialized.")
    except Exception as err:
        if throw_errors:
            if debug:
                raise AporiaError(f"Initializing Aporia SDK failed") from err

            raise AporiaError(f"Initializing Aporia SDK failed, error: {str(err)}")
        else:
            logger.error(f"Initializing Aporia SDK failed, error: {str(err)}")


def flush():
    """Waits for all of the prediction logs to reach the controller."""
    if context is None:
        logger.error("Flush failed, Aporia SDK was not initialized.")
        return

    logger.debug("Flushing remaining data")
    context.event_loop.flush()

"""The broker abstraction for Serori applications.

This module contains an in-memory implementation for use in tests.
"""

import abc
import asyncio
from typing import TYPE_CHECKING, AsyncIterator


class Broker(abc.ABC):
    """The broker abstraction for Serori."""

    @abc.abstractmethod
    async def publish(self, message: str) -> None:
        """Publish a message to the broker message queue."""

    @abc.abstractmethod
    async def consume(self) -> AsyncIterator[str]:
        """Yields messages from the broker message queue."""
        if TYPE_CHECKING:
            yield ""


class InMemoryBroker(Broker):
    """A simple broker that keeps messages in a memory FIFO.

    Its intended use is as a broker for tests.
    """

    def __init__(self):
        self._queue = asyncio.Queue()

    async def publish(self, message: str) -> None:
        await self._queue.put(message)

    async def consume(self) -> AsyncIterator[str]:
        while True:
            yield await self._queue.get()

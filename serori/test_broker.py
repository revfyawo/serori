"""Tests for the broker implementations."""

import asyncio

import pytest

from serori.broker import InMemoryBroker


@pytest.mark.asyncio
async def test_in_memory_broker():
    """Tests that the InMemoryBroker can publish a message and consume it after."""
    broker = InMemoryBroker()

    test_message = "test_message"
    published = await asyncio.wait_for(broker.publish(test_message), timeout=1)
    assert published is None

    async def first_message():
        async for message in broker.consume():
            return message
        raise AssertionError("no messages")

    received = await asyncio.wait_for(first_message(), timeout=1)
    assert received == test_message

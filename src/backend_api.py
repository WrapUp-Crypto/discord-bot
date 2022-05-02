import logging
from datetime import timedelta, datetime

from src.exceptions import BackendAPIError
from src.constants import BACKEND_API

URL = f"{BACKEND_API}/discord"

logger = logging.getLogger("bot")


async def get_channel_top_reacted_messages(
    session, server_id, channel_id, limit=5, since_days=1
):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/channels/{channel_id}/"
        + f"most-reacted/?limit={limit}&from_time={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching most reacted messages from {url}. Status code: {r.status}."
            logger.error(msg)
            raise BackendAPIError(msg)


async def get_channel_most_replied_messages(
    session, server_id, channel_id, limit=5, since_days=1
):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/channels/{channel_id}/"
        + f"most-replied/?limit={limit}&from_time={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching most replied messages from {url}. Status code: {r.status}."
            logger.error(msg)
            raise BackendAPIError(msg)


async def get_server_top_reacted_messages(session, server_id, limit=5, since_days=1):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/"
        + f"most-reacted/?limit={limit}&from_time={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching most reacted messages from {url}. Status code: {r.status}."
            logger.error(msg)
            raise BackendAPIError(msg)


async def get_server_most_replied_messages(session, server_id, limit=5, since_days=1):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/"
        + f"most-replied/?limit={limit}&from_time={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching most replied messages from {url}. Status code: {r.status}."
            logger.error(msg)
            raise BackendAPIError(msg)


async def get_emerging_channels(session, server_id, limit=3, since_days=1):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/channels/"
        + f"emerging/?limit={limit}&from_time={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Failed to fetch emerging channels from {url}. Status code: {r.status}."
            logger.error(msg)
            raise BackendAPIError(msg)


async def get_busiest_channels(session, server_id, limit=3, since_days=1):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = f"{URL}/servers/{server_id}/channels/?from_time={from_timestamp}"
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            resp_filtered = filter(lambda x: x["n_messages"] > 0, resp)
            resp_sorted = sorted(
                resp_filtered, key=lambda x: x["n_messages"], reverse=True
            )
            return resp_sorted[:limit]
        else:
            msg = (
                f"Failed to fetch busiest channels from {url}. Status code: {r.status}."
            )
            logger.error(msg)
            raise BackendAPIError(msg)


async def get_server_pinned_messages(session, server_id, limit=3, since_days=1):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/"
        + f"pinned/?limit={limit}&from_time={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching pinned messages from {url}. Status code: {r.status}."
            logger.error(msg)
            raise BackendAPIError(msg)

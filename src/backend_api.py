from datetime import timedelta, datetime

from src.exceptions import BackendAPIError
from src.constants import BACKEND_API

URL = f"{BACKEND_API}/discord"


async def get_channel_top_reacted_messages(
    session, server_id, channel_id, limit=3, since_days=1
):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/channels/{channel_id}/"
        + f"most-reacted/?limit={limit}&from={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching most reacted messages from {url}. Status code: {r.status}."
            raise BackendAPIError(msg)


async def get_channel_most_replied_messages(
    session, server_id, channel_id, limit=3, since_days=1
):
    from_timestamp = int((datetime.now() - timedelta(days=since_days)).timestamp())
    url = (
        f"{URL}/servers/{server_id}/channels/{channel_id}/"
        + f"most-replied/?limit={limit}&from={from_timestamp}"
    )
    async with session.get(url) as r:
        if r.status == 200:
            resp = await r.json()
            return resp["results"]
        else:
            msg = f"Error while fetching most replied messages from {url}. Status code: {r.status}."
            raise BackendAPIError(msg)

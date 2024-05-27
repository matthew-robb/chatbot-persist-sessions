
import uuid
from typing import Annotated
from fastapi import FastAPI, Body, Depends
from langchain_core.language_models import BaseChatModel
from psycopg import Connection, AsyncConnection
from starlette.responses import StreamingResponse

from .utils import fetch_chain, fetch_connection, fetch_async_connection, chunk_processor, fetch_llm

app = FastAPI()


@app.post("/chat/{session_id}")
async def chat(
    session_id: str,
    llm: Annotated[BaseChatModel, Depends(fetch_llm)],
    sync_conn: Annotated[Connection, Depends(fetch_connection)],
    async_conn: Annotated[AsyncConnection, Depends(fetch_async_connection)],
    message: str = Body(..., media_type="text"),
) -> StreamingResponse:
    chain = await fetch_chain(session_id, llm, sync_conn, async_conn)
    return StreamingResponse(
        chunk_processor(chain.astream_log(input=message)),
        media_type="text/event-stream",
        headers={"content-type": "text/event-stream"},
    )


@app.post("/chat")
async def create_chat() -> str:
    return str(uuid.uuid4())

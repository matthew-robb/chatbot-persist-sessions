import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body
from starlette.responses import StreamingResponse

from .utils import fetch_chain, fetch_connection, fetch_async_connection, chunk_processor, fetch_llm

dependencies = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    dependencies["llm"] = fetch_llm
    dependencies["sync_conn"] = fetch_connection
    dependencies["async_conn"] = fetch_async_connection
    yield dependencies
    dependencies["sync_conn"].close()
    dependencies["async_conn"].close()



app = FastAPI()


@app.post("/chat/{session_id}")
async def chat(
    session_id: str,
    message: str = Body(..., media_type="text"),
) -> StreamingResponse:
    chain = await fetch_chain(session_id, dependencies['llm'], dependencies['sync_conn'], dependencies['async_conn'])
    return StreamingResponse(
        chunk_processor(chain.astream_log(input=message)),
        media_type="text/event-stream",
        headers={"content-type": "text/event-stream"},
    )


@app.post("/chat")
async def create_chat() -> str:
    return str(uuid.uuid4())

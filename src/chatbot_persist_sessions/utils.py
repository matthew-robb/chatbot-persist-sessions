import os
from typing import AsyncIterator, AsyncIterable

import psycopg
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessageChunk
from langchain_core.tracers import RunLogPatch
from langchain_openai import ChatOpenAI
from langchain_postgres import PostgresChatMessageHistory
from psycopg import AsyncConnection, Connection

_message_history_table = "chat_context"
_conn_info = f"postgresql://postgres:postgres@{os.getenv('DB_HOST')}/postgres"


def fetch_llm() -> BaseChatModel:
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL"), api_key=os.getenv("OPENAI_API_KEY"), streaming=True)


def fetch_connection() -> Connection:
    connection = psycopg.connect(_conn_info)
    PostgresChatMessageHistory.create_tables(connection, _message_history_table)
    return connection


async def fetch_async_connection() -> AsyncConnection:
    connection = await psycopg.AsyncConnection.connect(_conn_info)
    return connection


async def fetch_chain(
    session_id: str, llm: BaseChatModel, sync_conn: Connection, async_conn: AsyncConnection
) -> ConversationChain:
    history = PostgresChatMessageHistory(
        _message_history_table, session_id, async_connection=async_conn, sync_connection=sync_conn
    )

    return ConversationChain(
        llm=llm,
        memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=10000, chat_memory=history),
        verbose=False,
    )


async def chunk_processor(generator: AsyncIterator[RunLogPatch]) -> AsyncIterable[str]:
    async for chunk in generator:
        for op in chunk.ops:
            if op.get("op") == "add":
                value = op.get("value")
                if isinstance(value, AIMessageChunk):
                    yield value.content

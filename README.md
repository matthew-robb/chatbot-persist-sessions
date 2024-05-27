
A lightweight example that demonstrates how to create a chat-bot service that persists session context using FastAPI and Langchain. This particular example uses postgres to persist session data and an OpenAI endpoint, however, there are many alternatives, see: [chat memory](https://js.langchain.com/v0.1/docs/integrations/chat_memory/), [chat models](https://python.langchain.com/v0.2/docs/integrations/chat/).

This example shows how to setup [chuncked transfer encoding](https://en.wikipedia.org/wiki/Chunked_transfer_encoding) i.e. response streaming (text/event-stream) in combination with Langcahin memory. Using the `astream` method on the Langchain type `ConversationChain` results in the entire response to be flushed in one go, hence a workaround was adopted which utilises the `astream_log` method.

### Run the App using Docker Compose
1. Create a .env file and set OPENAI_MODEL and OPENAI_API_KEY. 
2. Run `docker compose up -d` in repo root dir.

### Demo
1. Generate a session id: `curl -X POST http://localhost:8000/chat`
> eb0397f7-1818-4c8c-8ba8-3a717aa8ac5b
<br/>

2. Introduce yourself as Bob: `curl -N -X POST --data "Hi, my name is Bob!" http://localhost:8000/chat/eb0397f7-1818-4c8c-8ba8-3a717aa8ac5b`
> Hello Bob! It's nice to meet you. How can I assist you today?
<br/>

3. Generate another session id `curl -X POST http://localhost:8000/chat`
> c3e9da2b-3fad-40f9-917b-5fdd5ea80050
<br/>

4. Introduce yourself as someone else: `curl -N -X POST --data "Hi, my name is Matt!" http://localhost:8000/chat/c3e9da2b-3fad-40f9-917b-5fdd5ea80050`
> Hello Matt! It's nice to meet you. How can I assist you today?
<br/>

5. Ask what your name is using the first session id: `curl -N -X POST --data "What's my name again?" http://localhost:8000/chat/eb0397f7-1818-4c8c-8ba8-3a717aa8ac5b`
> Your name is Bob
<br/>

6. Ask what your name is using the second session id: `curl -N -X POST --data "What's my name again?" http://localhost:8000/chat/c3e9da2b-3fad-40f9-917b-5fdd5ea80050`
> Your name is Matt

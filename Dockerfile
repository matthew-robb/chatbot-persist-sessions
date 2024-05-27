FROM python:3.11

COPY . .
RUN pip install ./
EXPOSE 8000
CMD ["fastapi", "dev", "--host", "0.0.0.0", "src/chatbot_persist_sessions/main.py"]
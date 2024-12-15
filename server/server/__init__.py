from dotenv import load_dotenv
from fastapi import FastAPI
import socketio

load_dotenv()

from lib.td_client import start_api_conversation

start_api_conversation()

fastapi_app = FastAPI()
socket = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")

socket_app = socketio.ASGIApp(socket)
fastapi_app.mount("/", socket_app)

import lib.authentication

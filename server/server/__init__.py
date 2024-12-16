from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from lib.td_util import start_telegram_api_conversation
from server.socket_connection import socket_app

start_telegram_api_conversation()

fastapi_app = FastAPI()
fastapi_app.mount("/", socket_app)

import lib.authorization

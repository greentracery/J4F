#
#
from typing import List, Union, Optional
from typing_extensions import Annotated

from fastapi import FastAPI, Depends, Cookie, HTTPException, Header, status, Query, Form, Body, File, UploadFile, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse , Response, JSONResponse, HTMLResponse, RedirectResponse, FileResponse
#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from starlette.background import BackgroundTask

import asyncio
import datetime
import time
import sys
import os
import io
import json
import uuid
import platform

from faker import Faker ## https://faker.readthedocs.io/en/stable/index.html

fake = Faker()

from . libs.logger import LogWriter

lw = LogWriter('WSChat')

from . libs.speach_gen import SpeachGen

spg = SpeachGen()

from . libs.wsconn_manager import WSConnectionManager

manager = WSConnectionManager()


API_title = "WSChat WebApp"
API_description = """
Demo Application using websockets
"""

## Конфигурация DEV/PROD:
env = os.environ.get('ENVTYPE')
if env is not None and env == 'DEV':
    app = FastAPI(title=API_title, description = API_description)
else:
    app = FastAPI(title=API_title, description = API_description, openapi_url=None, docs_url=None, redoc_url=None)

## Конфигурация CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

APP_DIR = os.getcwd()
APP_PATH = os.path.dirname(os.path.realpath(__file__))
APP_STATIC = os.path.join(APP_DIR, "app", "static")
templates = Jinja2Templates(directory=os.path.join(APP_DIR, "app", "templates"))
app.mount('/static', StaticFiles(directory=APP_STATIC), name="static")

lw.log_info(f"App. {API_title} started with Python version {platform.python_version()}")

fake_names = {}

@app.get("/")
async def get(
    request: Request,
    response: Response,
    session_guid: Union[str, None] = Cookie(default=None),
):
    if session_guid is None:
        guid = str(uuid.uuid4())
    else:
        guid = session_guid
    
    if guid not in fake_names.keys():
        fake_name = fake.name()
        fake_names.update({ guid : fake_name })
    else:
        fake_name = fake_names[guid]
    
    response.set_cookie(key="session_guid", value=guid)
    
    return templates.TemplateResponse("main.html", {"request": request, 'guid': guid, 'name': fake_name}, status_code=200)


@app.websocket("/ws/{guid}")
async def websocket_endpoint(
    websocket: WebSocket, 
    guid: str,
):
    if guid not in fake_names.keys():
        fake_name = fake.name()
        fake_names.update({ guid : fake_name })
    else:
        fake_name = fake_names[guid]
    
    await manager.connect(websocket)
    
    try:
    
        #print(dir(websocket))
        #print(websocket.base_url, websocket.url.path, websocket.url.port, websocket.url.scheme, websocket.headers)
        #print(websocket.application_state, websocket.client.host, websocket.client.port)
    
        now = datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")
    
        #await manager.broadcast_text(f"{now}: {guid} connected")
        
        msg = f"connected ({websocket.headers['user-agent']}; address {websocket.client.host}:{websocket.client.port})"
        
        await manager.broadcast_json({"time": now, "guid": guid, "msg": msg, "name": fake_name, "msgtype": 'status'})
        
        lw.log_info(f"{guid} - {fake_name} {msg}")
        
        while websocket.application_state.CONNECTED:
            now = datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")
            
            msg = await websocket.receive_text()
            
            #await manager.send_text(f"{now}: Me: {msg}", websocket)
            #await manager.broadcast_text(f"{now}: {guid}: {msg}")
            
            #await manager.send_json({"time": now, "guid": guid, "msg": msg, "name": fake_name, "msgtype": 'message'}, websocket)
            await manager.broadcast_json({"time": now, "guid": guid, "msg": msg, "name": fake_name, "msgtype": 'message'})
            
    except WebSocketDisconnect as e:
        #print(e) ## 1001 - закрыт браузер, 1005 - отключил клиент, 1006 - отключил сервер etc см. RFC6455, §7.4.1.
        lw.log_warning(f"{guid} - {fake_name} disconnected ({e})")
        manager.disconnect(websocket)
        try:
            #await manager.broadcast_text(f"{now}: {guid} disconnected")
            await manager.broadcast_json({"time": now, "guid": guid, "msg": f" disconnected ({e})", "name": fake_name, "msgtype": 'status'})
        except:
            lw.log_error(e, True)
        
    except (RuntimeError, Exception) as e:
        lw.log_warning(f"{guid} - {fake_name} disconnected ({e})")
        manager.disconnect(websocket)
        lw.log_error(e, True)


async def send_ai_flood() -> None:
    try:
        now = datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")
        await manager.broadcast_json({"time": now, "guid": None, "name": None, "msg": spg.run(), "msgtype": 'flood'})
    except Exception as e:
        lw.log_error(e, True)


@app.get("/qq")
async def run_bg_task() -> JSONResponse:
    task = BackgroundTask(send_ai_flood)
    return JSONResponse({"status": "ok"}, background=task)

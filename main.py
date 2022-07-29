import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import Response
from rustplus import RustSocket


load_dotenv()
IP = os.environ['IP']
PORT = os.environ['PORT']
STEAMID = int(os.environ['STEAMID'])
PLAYERTOKEN = int(os.environ['PLAYERTOKEN'])

app = FastAPI()
rust_socket = RustSocket(IP, PORT, STEAMID, PLAYERTOKEN)


@app.on_event('startup')
async def on_startup():
    print('Connecting to the Rust socket...')
    await rust_socket.connect()
    print('Successfully connected to the Rust socket')


@app.on_event('shutdown')
async def on_shutdown():
    print('Disconnecting from the Rust socket...')
    await rust_socket.disconnect()
    print('Successfully disconnected from the Rust socket')


@app.get('/')
async def index():
    return Response('UP & RUNNING', status_code=200)


@app.get('/turn-on/{entity_id}')
async def turn_on(entity_id: int):
    print(f'Turning device #{entity_id} on...')
    await rust_socket.turn_on_smart_switch(entity_id)
    print(f'Successfully turned device #{entity_id} on')
    return Response(status_code=200)


@app.get('/turn-off/{entity_id}')
async def turn_off(entity_id: int):
    print(f'Turning device #{entity_id} off...')
    await rust_socket.turn_off_smart_switch(entity_id)
    print(f'Successfully turned device #{entity_id} off')
    return Response(status_code=200)

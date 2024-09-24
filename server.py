#! /usr/bin/env python

import asyncio
import websockets
import sys

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

# -----------------------------------------------------------------------------

async def wsConnectionHandler(websocket: websockets.WebSocketServerProtocol) -> None:
    
    print(f'WS-Server: Connection established with {websocket.remote_address[0]}:{websocket.remote_address[1]}')
    print(f'WS-Server: Connection ID: {websocket.id}')

    try:
        async for message in websocket:
            await websocket.send(message)

    except websockets.exceptions.ConnectionClosed:
        pass

    print(f'WS-Server: Connection {websocket.id} closed')

# -----------------------------------------------------------------------------

async def wsServer(host: str, port: int) -> None:

    async with websockets.serve(wsConnectionHandler, WS_HOST, WS_PORT):

        print(f'WS-Server: Listening for connections at {host}:{port}')

        try:
            await asyncio.Future()

        except asyncio.exceptions.CancelledError:
            pass

    print('\nWS-Server: Shutdown')

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    asyncio.run( wsServer(WS_HOST, WS_PORT) )

    sys.exit(0)

# -----------------------------------------------------------------------------

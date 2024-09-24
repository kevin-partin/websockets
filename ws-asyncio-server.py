#! /usr/bin/env python

'''
websocket server example
'''

import asyncio
import datetime
import json
import sys

import websockets.exceptions
import websockets.server

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

# -----------------------------------------------------------------------------

async def wsConnectionHandler(websocket: websockets.WebSocketServerProtocol) -> None:

    print(f'WS-Server: Connection established with {websocket.remote_address[0]}:{websocket.remote_address[1]}')
    print(f'WS-Server: Connection ID: {websocket.id}')

    while True:

        message = json.dumps({'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')})

        try:
            await websocket.send( message )

        except websockets.exceptions.ConnectionClosed:
            break

        await asyncio.sleep(5)

    print('WS-Server: Connection closed')

# -----------------------------------------------------------------------------

async def wsServer(host: str, port: int) -> None:

    print(f'WS-Server: Listening for connections at {host}:{port}')

    async with websockets.server.serve(wsConnectionHandler, host, port):
        await asyncio.Future()

    print('WS-Server: Shutdown')

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        asyncio.run( wsServer(WS_HOST, WS_PORT) )
    except KeyboardInterrupt:
        print()

    sys.exit(0)

# -----------------------------------------------------------------------------

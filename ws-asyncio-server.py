#!/usr/bin/env python

'''
websocket server example
'''

import asyncio
import base64
import datetime
import gzip
import json
import os
import sys

import websockets.exceptions
import websockets.server

USE_BINARY = False


async def wsServer(host: str, port: int):

    print(f'websocket server listening for connections on {host}:{port}')

    async with websockets.server.serve(wsConnectionHandler, host, port):
        await asyncio.Future()


async def wsConnectionHandler(websocket):

    print('websocket connection established')

    response = {}

    # Send a ISO timestamp as a JSON-string every 5 seconds.
    while True:

        dt = datetime.datetime.now()
        response['Timestamp'] = dt.isoformat()
        msg = json.dumps( response )

        if USE_BINARY:
            msg = base64.b64encode( gzip.compress( msg.encode() ) )

        try:
            await websocket.send( msg )
        except websockets.exceptions.ConnectionClosed:
            break

        await asyncio.sleep(5)

    print('websocket connection closed')


WS_HOST = '127.0.0.1'
WS_PORT = 8765

try:
    asyncio.run( wsServer(WS_HOST, WS_PORT) )
except KeyboardInterrupt:
    print('KeyboardInterrupt exception trapped')

print(f'{os.path.basename(__file__)} exiting')
sys.exit(0)

#!/usr/bin/env python

'''
websocket asyncio client example
'''

import asyncio
import base64
import gzip
import json
import os
import sys

import websockets.exceptions
import websockets.client

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

USE_BINARY = False


async def wsClient(uri: str):

    async with websockets.client.connect(uri) as websocket:

        print('websocket connection established')

        while True:
            try:
                msg = await websocket.recv()
            except websockets.exceptions.ConnectionClosed:
                break
            except asyncio.CancelledError:
                break

            if USE_BINARY:
                msg = gzip.decompress( base64.b64decode( msg ) ).decode()

            print( json.loads( msg ) )

    print('websocket connection closed')


asyncio.run( wsClient(WS_URI) )

print(f'{os.path.basename(__file__)} exiting')
sys.exit(0)

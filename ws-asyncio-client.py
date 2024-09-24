#! /usr/bin/env python

'''
websocket asyncio client example
'''

import asyncio
import json
import sys

import websockets.exceptions
import websockets.client

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

# -----------------------------------------------------------------------------

async def wsClient(uri: str):

    print(f'WS-Client: Attemping to establish a websocket connection to {uri}')

    async with websockets.client.connect(uri) as websocket:

        print('WS-Client: Connection established')

        while True:

            try:
                message = await websocket.recv()

            except websockets.exceptions.ConnectionClosed:
                break

            except asyncio.CancelledError:
                break

            print( json.loads( message ) )

    print('WS-Client: Connection closed')

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    asyncio.run( wsClient(WS_URI) )

    print('WS-Client: Shutdown')

    sys.exit(0)

# -----------------------------------------------------------------------------

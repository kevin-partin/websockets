#!/usr/bin/env python

'''
websocket client example
'''

import base64
import gzip
import json
import os
import sys

import websockets.exceptions
import websockets.sync.client

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

USE_BINARY = False

try:
    websocket = websockets.sync.client.connect(WS_URI)
except ConnectionRefusedError:
    print('websocket connection refused')
    sys.exit(1)

print('websocket connection established')

try:

    while True:
        try:
            msg = websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            break

        if USE_BINARY:
            msg = gzip.decompress( base64.b64decode( msg ) ).decode()

        print( json.loads( msg ) )

except KeyboardInterrupt:
    print('KeyboardInterrupt exception trapped')

websocket.close()
print('websocket connection closed')

print(f'{os.path.basename(__file__)} exiting')
sys.exit(0)

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

with websockets.sync.client.connect(WS_URI) as websocket:

    print('websocket connection established')

    try:
        for message in websocket:

            if USE_BINARY:
                message = gzip.decompress( base64.b64decode( message ) ).decode()

            print( json.loads( message ) )
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception trapped')

print('websocket connection closed')

print(f'{os.path.basename(__file__)} exiting')
sys.exit(0)

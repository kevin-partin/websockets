#! /usr/bin/env python

'''
websocket threaded client example
'''

import json
import os
import sys
import time

import websockets.exceptions
import websockets.sync.client

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

print(f'Attemping to establish a websocket connection to {WS_URI} ', end='', flush=True)

while True:

    print('.', end='', flush=True)

    try:
        with websockets.sync.client.connect(WS_URI) as websocket:

            print(' Done.\nWS-Client: connection established')

            try:

                for message in websocket:
                    print( json.loads( message ) )

            except websockets.exceptions.ConnectionClosed:
                break

    except ConnectionRefusedError:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break

    except KeyboardInterrupt:
        break

print('\nWS-Client: connection closed')

print(f'{os.path.basename(__file__)} exiting')
sys.exit(0)

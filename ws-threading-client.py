#! /usr/bin/env python

'''
websocket threaded client example
'''

import json
import sys
import time

import websockets.exceptions
import websockets.sync.client

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

enabled = True

while enabled:

    print(f'WS-Client: Attemping to establish a websocket connection to {WS_URI}')

    while True:

        try:

            with websockets.sync.client.connect(WS_URI) as websocket:

                print('WS-Client: Connection established')

                while True:

                    try:
                        message = websocket.recv()
                        print( json.loads( message ) )

                    except KeyboardInterrupt:
                        print()
                        websocket.close()
                        enabled = False
                        break

                    except websockets.exceptions.ConnectionClosed:
                        break

                print('WS-Client: Connection closed')
                break

        except ConnectionRefusedError:
                    
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print()
                enabled = False
                break

        except KeyboardInterrupt:
            print()
            break

print('WS-Client: Shutdown')

sys.exit(0)

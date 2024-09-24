#! /usr/bin/env python

from datetime import datetime
import json
import sys
import time

import websockets.sync.client

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

# -----------------------------------------------------------------------------

def wsClient():

    print(f'WS-Client: Attemping to establish a websocket connection to {WS_URI}')

    try:

        with websockets.sync.client.connect(WS_URI) as websocket:
                    
            print('WS-Client: Connection established')

            while True:
                
                message = json.dumps({'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')})

                print('Sent:', message)
                try:
                    websocket.send(message)
                except websockets.exceptions.ConnectionClosed:
                    break

                message = websocket.recv()
                print('Received:', message)

                try:
                    time.sleep(5)
                except KeyboardInterrupt:
                    print()
                    break

            print('WS-Client: Connection closed')

    except ConnectionRefusedError:
        print('WS-Client: Connection Refused')

    print('WS-Client: Shutdown')

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        wsClient()
    except KeyboardInterrupt:
        print()

    sys.exit(0)

# -----------------------------------------------------------------------------

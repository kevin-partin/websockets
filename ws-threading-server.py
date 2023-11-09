#! /usr/bin/env python

'''
websocket threaded server example
'''

import datetime
import json
import signal
import time

import websockets.exceptions
import websockets.sync.server

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

def handler(websocket:websockets.sync.server.ServerConnection):

    print('WS-Server: connection established')

    while True:
        message = {'Timestamp': datetime.datetime.now().isoformat()}
        try:
            websocket.send(json.dumps(message))
            print('.', end='', flush=True)
        except websockets.exceptions.ConnectionClosed:
            break
        time.sleep(5)

    print('\nWS-Server: connection closed')

def signalHandler(server: websockets.sync.server.WebSocketServer, signum: int, *args) -> None:
    if signum == signal.SIGINT:
        print('SIGINT')
        server.shutdown()

try:
    with websockets.sync.server.serve(handler, host=WS_HOST, port=WS_PORT) as server:
        signal.signal(signal.SIGTERM, lambda x, y: signalHandler(server, x, y))
        server.serve_forever()
except KeyboardInterrupt:
    print()

#! /usr/bin/env python

'''
websocket threaded server example
'''

from datetime import datetime
import json
import sys
import threading
import time
from uuid import UUID

import websockets.exceptions
import websockets.sync.server

WS_HOST = '127.0.0.1'
WS_PORT = 8765
WS_URI  = f'ws://{WS_HOST}:{WS_PORT}'

# -----------------------------------------------------------------------------

class WebSocketServer():

    # -----------------------------------------------------------------------------

    def __init__(self) -> None:

        self.websockets: dict[UUID, websockets.sync.server.ServerConnection] = {}

        self.thread = threading.Thread(
            target=self._wsServer
        )
        self.enabled = True
        self.thread.start()

    # -----------------------------------------------------------------------------

    def wsConnectionHandler(self, websocket: websockets.sync.server.ServerConnection):

        print(f'WS-Server: Established connection with {websocket.remote_address[0]}:{websocket.remote_address[1]}')

        wsid = websocket.id
        self.websockets[wsid] = websocket

        while self.enabled:

            message = {'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')}

            try:
                websocket.send(json.dumps(message))

            except websockets.exceptions.ConnectionClosed:
                break

            time.sleep(5)

        websocket.close()

        del self.websockets[wsid]

        print(f'WS-Server: Connection {wsid} closed')

    # -----------------------------------------------------------------------------

    def shutdown(self) -> None:

        self.enabled = False

        # Wait for all of the websockets to close.
        while len(self.websockets):
            pass

    # -----------------------------------------------------------------------------

    def _wsServer(self) -> None:

        with websockets.sync.server.serve(self.wsConnectionHandler, WS_HOST, WS_PORT) as self.server:

            print('WS-Server: Listening on', WS_URI)

            self.server.serve_forever()
            self.shutdown()

            print('WS-Server: Shutdown')

# -----------------------------------------------------------------------------

wsserver = WebSocketServer()

try:
    while True:
        time.sleep(0.25)
except KeyboardInterrupt:
    print()
    wsserver.server.shutdown()

sys.exit(0)

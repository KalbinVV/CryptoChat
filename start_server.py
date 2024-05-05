import logging
import threading

from server.server_class import CryptoChatServer

logging.basicConfig(level=logging.DEBUG)

server = CryptoChatServer()

try:
    server_thread = threading.Thread(target=server.start)

    server_thread.start()
    server_thread.join()
except (KeyboardInterrupt, ):
    server.stop()

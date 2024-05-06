import logging

from client.client_gui.init_app import InitApp

logging.basicConfig(level=logging.DEBUG)

init_app = InitApp()

init_app.mainloop()

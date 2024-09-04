import logging
from handlers import Handler


class HelpHandler(Handler):

    def __init__(self):
        self.pattern = r'''^/help.*'''

    async def handler(self, event):
        await event.respond('''Usage:
                            ''')
    logging.info("printed help")

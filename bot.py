import uuid
from datetime import datetime
import os
import logging
import time
import re
import json
from dotenv import find_dotenv, load_dotenv
from telethon import TelegramClient, events, Button, errors
import openai
from handlers.command import CommandHandler
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


load_dotenv(find_dotenv())
time.sleep(5)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

openai.api_key = os.environ.get("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4o")
improve_button_list = [Button.inline('Nice!')]
api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
bot_token = os.environ.get("telegram_bot_token")
session_name = os.environ.get("telegram_session_name")

if api_id is None or api_hash is None or bot_token is None:
    logging.error("Please set the environment variables: telegram_api_id, telegram_api_hash, telegram_bot_token")
    exit(1)

class Bot:

    def __init__(self):
        self.bot_name = os.environ.get("telegram_bot_name")
        self.client = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)
        self.attach_handlers()

    def attach_handlers(self):
        #command_handler = CommandHandler()
        self.client.on(events.NewMessage(pattern=f"^{self.bot_name}.*"))(self.handler)
        #self.client.on(events.NewMessage(pattern=command_handler.pattern))(command_handler.handler)
        #self.client.on(events.CallbackQuery)(self.callback)

    async def handler(self, event):
        logging.info("Got a message" + event.raw_text)
        try:
            question = event.raw_text.replace(self.bot_name, '').replace('@', '').strip()
            #if event.is_group:
            PROMPT = '''You are the best teacher of the Latin language. 
                        You are accurate and make a point out of correcting student grammar.
                        When a student ask's you a general questions you will reply in Latin.
                        When a student ask's you a question about Latin you will reply in Latin providing all the relevant information and examlpes.
                        You will correct if needed any input provided by the student and provide examples.
                        Any input provided by the student needs to be grammatically parsed into parts of speach, tenses and classified when applicable into conjucations and declensions.

                        The student's input is:
                        '''


            if self.bot_name in event.raw_text:
                logging.info(f"event user: {event.sender.username}")
                content = PROMPT + f' \n {question}'
                #response = self.chain({"question": question})
                response = model.invoke([HumanMessage(content=content)])
                await event.respond(f"""{response.content}""")
        except Exception as e:
            logging.error(f"error in handling message {e}")

    
    def run_bot(self):
        self.client.start()
        logging.info("Running Bot!")
        self.client.run_until_disconnected()


if __name__ == '__main__':
    try:
        bot = Bot()
        bot.run_bot()
    except errors.FloodWaitError as e:
        logging.warning('Have to sleep', e.seconds, 'seconds')
        time.sleep(e.seconds)
    except Exception as e:
        logging.error(f"error in running bot {e}", stack_info=True, exc_info=True)

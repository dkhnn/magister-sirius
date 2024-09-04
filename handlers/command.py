from datetime import datetime
from langchain_openai import AzureChatOpenAI
import requests
import logging
import os
from handlers import Handler



class CommandHandler(Handler):

    def __init__(self):
        self.pattern = r'''^/command\s+["\'\u2018\u2019\u201c\u201d`\xb4](.*?)["\'\u2018\u2019\u201c\u201d`\xb4]'''
        self.llm = AzureChatOpenAI(
            deployment_name=os.environ.get('AZURE_MODEL_DEPLOYMENT'),
            openai_api_version=os.environ.get('OPEN_AI_API_VER'),
            openai_api_key=os.environ.get('OPENAI_API_KEY'),
            azure_endpoint=os.environ.get('AZURE_ENDPOINT'),
            max_tokens=4096
        )

    async def handler(self, event):
        await event.respond('Building an answer')
        matched = event.pattern_match.groups()
        claim = matched[0]
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            context = f'prompt'
            refutal = self.agent.run(context)
            await event.respond(refutal)
        except Exception as e:
            logging.error(f"error in improving answer {e}")

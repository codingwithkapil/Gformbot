import logging
import requests
import re
from telethon import TelegramClient
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from test import formAutomation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Telegram API credentials
api_id = 'XXX'
api_hash = 'XXX'

# Dictionary to store the Google Form URL and field names
form_data = {
    'url': '',
    'fields': ["XXX","XXX","XXX"]
}

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def getChatMessages(client: TelegramClient, chatName, message):
    await handle_message(message)

    raise ValueError(f"Chat with title '{chatTitle}' not found")

async def handle_message(message):
    link=""
    link = re.search("(?P<url>https?://[^\s]+)",  message.message.text).group("url")

    if link!="":
        form_data['url']=link
        logger.info(f"Detected Google Form link: {form_data['url']}")
        await client.send_message('me', 'Detected Google Form link. Now send the field names and their corresponding IDs in the format: field_name1:field_id1,field_name2:field_id2')
        formAutomation(form_data)
        await client.send_message('me', 'Form submitted successfully!')

@client.on(events.NewMessage(chats="XXX"))
async def message_handler(event):
    try:
        # RUssian language department chat
        await getChatMessages(client, "XXX", event)
    except ValueError as e:
        await event.respond(str(e))
    except Exception as e:
        logger.error(f"Error handling message: {e}")

async def main():
    # Start the client
    await client.start(phone=lambda: input("Enter your phone number: "))

    # Print out the bot's dialog list to help identify the correct group ID or username
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        logger.info(f"Chat: {dialog.name}, ID: {dialog.id}")

    logger.info("Client created and started")

    # Keep the client running
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    

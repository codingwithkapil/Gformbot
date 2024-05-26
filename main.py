import logging
import requests
import re
from telethon import TelegramClient, events

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials
api_id = 'XXX'
api_hash = 'XXX'
chatid='XXXX'

# Dictionary to store the Google Form URL and field names
form_data = {
    'url': '',
    'fields': {}
}


# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=chatid))  # Replace with actual group username or ID
async def handler(event):
    try:
        message = event.message.message
        logger.info(f"Received message: {message}")
        
        form_link_pattern = r'https://docs.google.com/forms/d/e/[^/]+/formResponse'
        match = re.search(form_link_pattern, message)
        
        if match:
            form_data['url'] = match.group(0)
            logger.info(f"Detected Google Form link: {form_data['url']}")
            await event.respond('Detected Google Form link. Now send the field names and their corresponding IDs in the format: field_name1:field_id1,field_name2:field_id2')
    
        elif ':' in message:
            fields = message.split(',')
            for field in fields:
                name, field_id = field.split(':')
                form_data['fields'][name.strip()] = field_id.strip()
            await event.respond(f"Fields set: {form_data['fields']}. Now send your name and email in the format: name,email")
    
        elif ',' in message:
            if not form_data['url'] or not form_data['fields']:
                await event.respond('Form URL or fields not set. Post a Google Form link and provide field mappings first.')
                return
            
            name, email = map(str.strip, message.split(',', 1))
            data = {
                form_data['fields']['name']: name,
                form_data['fields']['email']: email,
            }
            response = requests.post(form_data['url'], data=data)
            
            if response.status_code == 200:
                await event.respond('Form submitted successfully!')
            else:
                await event.respond('Failed to submit the form. Please try again.')
    except Exception as e:
        logger.error(f"Error handling message: {e}")

async def main():
    # Start the client
    await client.start()
    logger.info("Client created and started")
    
    # Print out the bot's dialog list to help identify the correct group ID or username
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        logger.info(f"Chat: {dialog.name}, ID: {dialog.id}")
    
    # Keep the client running
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

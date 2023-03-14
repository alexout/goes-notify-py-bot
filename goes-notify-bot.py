import json
import logging
import os

import requests

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    # Parse event data
    body = json.loads(event["body"])
    chat_id = body["message"]["chat"]["id"]
    first_name = body["message"]["chat"]["first_name"]
    message_text = body["message"]["text"]

    response = "Please /start, {}".format(first_name)

    if "start" in message_text:
        response = "Hello {}".format(first_name)

    # Send message to user
    response = send_message(chat_id, response)

    return {"statusCode": 200, "body": json.dumps(response)}


def send_message(chat_id, message_text):
    # Build message payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
    }

    # Send message via Telegram API
    telegram_bot_token = os.environ["TELEGRAM_TOKEN"]
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    response = requests.post(telegram_api_url, json=payload)

    logger.info(f"Telegram API response: {response.content}")

    return response.content
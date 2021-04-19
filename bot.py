import time
import datetime
import configparser
import json

from channels import channels
"""
{
    "id": <int:ID>,
    "name": <str:name>,
    "category": <str:category>
    "title": <str:title>
}
"""

from telethon.sync import TelegramClient

from datetime import date, datetime, timedelta

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from telethon.tl.functions.messages import GetHistoryRequest

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

date_now = datetime.now()
offset_date = date_now - timedelta(days=1)

client.start()

class DateTimeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)

async def dump_all_messages(channel, channel_name):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 50
    limit_msg = 100

    all_messages = []
    total_messages = 0
    total_count_limit = 10

    messages = []

    async for message in client.iter_messages(channel, offset_date=offset_date, reverse=True):
        messages.append({
            "text": message.raw_text,
            "date": message.date,
            "channel": channel_name,
            "internal_id": message.id
        })

    with open(f'results/{channel_name}.json', 'w', encoding='utf8') as outfile:
        json.dump(messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():

    for ch in channels:
        time.sleep(3)
        print(ch["name"])
        channel = await client.get_entity(f'https://t.me/{ch["name"]}')
        await dump_all_messages(channel, ch["name"])


with client:
    client.loop.run_until_complete(main())

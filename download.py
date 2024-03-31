import asyncio
from datetime import datetime
import os
import json
import telethon
import telethon.sessions


class App:
    tg: telethon.TelegramClient
    settings: dict

    def __init__(self) -> None:
        self.tg = telethon.TelegramClient(
            telethon.sessions.StringSession(os.environ["TELEGRAM_SESSION_TELETHON"]),
            int(os.environ["TELEGRAM_API_ID"]),
            os.environ["TELEGRAM_API_HASH"],
        )

        self.settings = json.load(open("settings.json"))
        self.settings["download"]["from_date"] = datetime.strptime(
            self.settings["download"]["from_date"], "%Y-%m-%d"
        )

    async def __aenter__(self):
        await self.tg.start()  # type: ignore
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.tg.disconnect()  # type: ignore


async def amain():
    async with App() as app:
        for chat in app.settings["download"]["from_chats"]:
            async for msg in app.tg.iter_messages(
                chat,
                offset_date=app.settings["download"]["from_date"],
                reverse=True,
                limit=1,
            ):
                if msg.message:
                    print(f"{msg.from_id.user_id} at {msg.date}: {msg.message}")


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()

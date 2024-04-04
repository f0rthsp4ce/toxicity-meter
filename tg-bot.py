import asyncio
import os
import logging
import telethon
import telethon.sessions
import torch
import json
from detoxify import Detoxify


async def amain():
    config = json.load(open("settings.json"))

    assert torch.cuda.is_available()
    toxicity_clf = Detoxify("multilingual", device="cuda")

    async with telethon.TelegramClient(
        telethon.sessions.StringSession(os.environ["TELEGRAM_SESSION_TELETHON"]),
        int(os.environ["TELEGRAM_API_ID"]),
        os.environ["TELEGRAM_API_HASH"],
        sequential_updates=True,  # no GPU races
    ) as tg:

        @tg.on(
            telethon.events.NewMessage(
                chats=config["bot"]["monitor-chats"], incoming=True
            )
        )
        async def h(event):
            score = toxicity_clf.predict(event.raw_text)["toxicity"]
            if score >= 0.8:
                await tg(
                    telethon.tl.functions.messages.SendReactionRequest(
                        peer=event.peer_id,
                        msg_id=event.id,
                        reaction=[
                            telethon.types.ReactionCustomEmoji(
                                5406772623415720314
                            )  # https://t.me/addemoji/BeBrilliant
                        ],
                    )
                )

        await asyncio.Event().wait()


def main():
    logging.basicConfig(
        format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
        level=logging.WARNING,
    )
    asyncio.run(amain())


if __name__ == "__main__":
    main()

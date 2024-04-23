import asyncio
import os
import logging
import telethon
import telethon.sessions
import transformers
import torch
import json
from detoxify import Detoxify


async def amain():
    config = json.load(open("settings.json"))

    assert torch.cuda.is_available()
    toxicity_clf = Detoxify("multilingual", device="cuda")

    sentiment_clf = transformers.pipeline(
        model="blanchefort/rubert-base-cased-sentiment", device="cuda"
    )

    def negative_predict(x) -> float:
        return next(
            row["score"]
            for row in sentiment_clf(x, top_k=None)
            if row["label"] == "NEGATIVE"
        )

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
            toxicity = toxicity_clf.predict(event.raw_text)["toxicity"]
            negativity = negative_predict(event.raw_text)

            reactions = []

            if toxicity >= 0.60:
                reactions.append(
                    telethon.types.ReactionCustomEmoji(
                        5406748567303900401
                    )  # https://t.me/addemoji/BeBrilliant
                )
            if toxicity >= 0.8:
                reactions.append(
                    telethon.types.ReactionCustomEmoji(
                        5407118673225730467
                    )  # https://t.me/addemoji/BeBrilliant
                )
            if toxicity >= 0.98:
                reactions.append(
                    telethon.types.ReactionCustomEmoji(
                        5406772623415720314
                    )  # https://t.me/addemoji/BeBrilliant
                )
            #if negativity >= 0.9:
            #    reactions.append(telethon.types.ReactionEmoji("😢"))

            if reactions:
                await tg(
                    telethon.tl.functions.messages.SendReactionRequest(
                        peer=event.peer_id,
                        msg_id=event.id,
                        reaction=reactions[:3],
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

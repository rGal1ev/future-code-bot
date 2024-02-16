import ssl

from aiogram.types import Update
from fastapi import FastAPI
from os import getenv, path

from store import init_tables
from bot import bot, dispatcher
from pyngrok import ngrok, conf, installer

pyngrok_config = conf.get_default()

if not path.exists(pyngrok_config.ngrok_path):
    m_ssl = ssl.create_default_context()
    m_ssl.check_hostname = False
    m_ssl.verify_mode = ssl.CERT_NONE

    installer.install_ngrok(pyngrok_config.ngrok_path, context=m_ssl)

ngrok.set_auth_token(getenv("NGROK_KEY"))
tunnel = ngrok.connect(addr="http://localhost:8000")

WEBHOOK_PATH = f"/bot/{getenv('TELEGRAM_KEY')}"
WEBHOOK_URL = f"{tunnel.public_url}{WEBHOOK_PATH}"

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_tables()
    info = await bot.get_webhook_info()

    if info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def on_bot_update(update: dict):
    update = Update.model_validate(update, context={
        "bot": bot
    })

    await dispatcher.feed_update(
        bot=bot,
        update=update
    )


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


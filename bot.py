# Pedrinho Tips IA - Protótipo

Protótipo inicial de um bot Telegram que:
- compara odds entre Bet365 e Betano
- detecta possíveis oportunidades
- envia sinais automaticamente

## Estrutura
- bot.py -> bot principal
- requirements.txt -> bibliotecas
- config_example.py -> exemplo de configuração

## Como usar

1. Crie um bot no Telegram:
https://t.me/BotFather

2. Pegue sua API:
https://the-odds-api.com/

3. Instale:
pip install -r requirements.txt

4. Configure:
-  seu token =
8661600392:AAHqi3MSLBuvAqXRY__3rZaiMALLvIGL0zU
- seu token = 3febe8e47b826ea1608c8349f6dc03bc

5. Rode:
python bot.py

## Próximos passos
- adicionar IA
- painel web
- estatísticas
- machine learning
- múltiplas casas
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = "SEU_TOKEN_AQUI"

tips_futebol = [
    "⚽ Tip: Mais de 1.5 gols no jogo",
    "⚽ Tip: Ambas marcam (BTTS)",
    "⚽ Tip: Favorito vence a partida",
    "⚽ Tip: Menos de 3.5 gols"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Pedrinho Tips IA Futebol ONLINE")

async def auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def enviar(context):
        chat_id = context.job.chat_id
        tip = random.choice(tips_futebol)
        await context.bot.send_message(chat_id=chat_id, text=tip)

    context.job_queue.run_repeating(enviar, interval=3600, first=5, chat_id=update.effective_chat.id)

    await update.message.reply_text("📊 Tips de futebol automáticas ATIVADAS!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("auto", auto))

app.run_polling()
import os
import requests
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

bot = Bot(token=BOT_TOKEN)

SPORT = "soccer"
REGIONS = "eu"
MARKETS = "h2h"  # vencedor

BOOKMAKERS = ["bet365", "betano"]

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": "decimal"
    }

    r = requests.get(url, params=params)
    return r.json()

def extract_bookmaker_odds(event):
    result = {}

    for bookmaker in event.get("bookmakers", []):
        name = bookmaker.get("key")

        if name in BOOKMAKERS:
            outcomes = bookmaker["markets"][0]["outcomes"]

            result[name] = {
                o["name"]: o["price"] for o in outcomes
            }

    return result

def find_opportunity(data):
    alerts = []

    for event in data:
        odds = extract_bookmaker_odds(event)

        if "bet365" in odds and "betano" in odds:
            for team in odds["bet365"]:
                if team in odds["betano"]:
                    diff = abs(odds["bet365"][team] - odds["betano"][team])

                    if diff >= 0.20:  # filtro de oportunidade
                        alerts.append(
                            f"🔥 VALUE BET DETECTADO\n"
                            f"{event['home_team']} vs {event['away_team']}\n"
                            f"{team}\n"
                            f"Bet365: {odds['bet365'][team]}\n"
                            f"Betano: {odds['betano'][team]}\n"
                        )

    return alerts


async def send_loop(chat_id):
    while True:
        try:
            data = get_odds()
            alerts = find_opportunity(data)

            if alerts:
                for msg in alerts[:3]:
                    await bot.send_message(chat_id=chat_id, text=msg)
            else:
                await bot.send_message(chat_id=chat_id, text="📊 Nenhuma oportunidade agora")

        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Erro: {e}")

        await asyncio.sleep(1800)  # 30 minutos


async def start_bot(chat_id):
    await send_loop(chat_id)


if __name__ == "__main__":
    print("Bot rodando...")
    asyncio.run(start_bot(YOUR_CHAT_ID))
    pip install python-telegram-bot requests python-dotenv

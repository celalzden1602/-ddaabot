import telebot
import math
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def poisson(lmbda, k):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

def analiz(ev_gol, dep_gol):
    skorlar = {}
    for i in range(5):
        for j in range(5):
            skorlar[f"{i}-{j}"] = poisson(ev_gol, i) * poisson(dep_gol, j)
    return max(skorlar, key=skorlar.get)

def guven_hesapla(ev_gol, dep_gol):
    fark = abs(ev_gol - dep_gol)
    return min(85, round(50 + fark * 10))

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "⚽ Maçı şu formatta yaz:\nFenerbahçe - Galatasaray")

@bot.message_handler(commands=['banko'])
def banko(message):
    bot.reply_to(message, "🔥 Günün Bankosu:\nEv Sahibi Kazanır\nGüven: %72")

@bot.message_handler(func=lambda message: True)
def tahmin(message):
    ev_gol = 1.7
    dep_gol = 1.2

    skor = analiz(ev_gol, dep_gol)
    guven = guven_hesapla(ev_gol, dep_gol)

    cevap = f"""
📊 ANALİZ SONUCU

Tahmini Skor: {skor}

1X2: 1
Üst 2.5: %{round(ev_gol/(ev_gol+dep_gol)*100)}

Güven Skoru: %{guven}
"""
    bot.reply_to(message, cevap)

bot.infinity_polling()

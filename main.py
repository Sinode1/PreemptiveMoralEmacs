import telebot
import requests
import re
import xml.etree.ElementTree as ET

bot = telebot.TeleBot("6604061152:AAE7p2qBLOK00szndMWy4en2RpytglhBtUk")

target_chat_id = -1001925244785
allowed_user_ids = [1544361472]


def decline_word(word):
  url = "https://ws3.morpher.ru/russian/declension"

  headers = {
      'Content-type': 'text/plain; charset=utf-8',
      'Host': 'ws3.morpher.ru',
      'Content-Length': str(len(word)),
      'User-Agent': 'python'
  }

  response = requests.post(url, data=word.encode('utf-8'), headers=headers)

  if response.status_code == 200:
    root = ET.fromstring(response.text)

    nominative = root.find(".//И")
    genitive = root.find(".//Р")
    dative = root.find(".//Д")
    ablative = root.find(".//Т")
    nominative_plural = root.find(".//М")

    if not nominative_plural:
      nominative_plural = nominative

    return {
        'nominative':
        nominative.text if nominative is not None else word,
        'genitive':
        genitive.text if genitive is not None else word,
        'dative':
        dative.text if dative is not None else word,
        'ablative':
        ablative.text if ablative is not None else word,
        'nominative_plural':
        nominative_plural.text if nominative_plural is not None else word,
    }
  else:
    return {
        'nominative': word,
        'genitive': word,
        'dative': word,
        'ablative': word,
        'nominative_plural': word,
    }


@bot.message_handler(func=lambda message: message.text.startswith('+тема'))
def handle_plus_tema(message):
  lines = message.text.split('\n')[1:]
  response = "<b>🎨 Тема модераторов готова!</b>\n\n<code>Модераторы названия\n"

  for line in lines:
    parts = line.split('=')
    if len(parts) >= 2:
      number = parts[0].strip()
      words = parts[1].strip().split(" ")
      combined_words = " ".join(words)
      declined_word = decline_word(combined_words)

      response += f"{number} и=<code>{combined_words}</code>;р=<code>{declined_word['genitive']}</code>;д=<code>{declined_word['dative']}</code>;т=<code>{declined_word['ablative']}</code>;мн=<code>{declined_word['nominative_plural']}</code>\n"

  response += "</code>"
  bot.reply_to(message, response, parse_mode="HTML")
               
bot.polling()

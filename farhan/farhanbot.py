import http.client
import random
import json
import mimetypes
import requests
import telebot
from codecs import encode
import pymongo
import re
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from bs4 import BeautifulSoup
from time import sleep

TELEGRAM_TOKEN = "TOKEN"  5278314620:AAFrGIN1y8m6WIY9QCTTgDMsj9KcY7cxUks
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
payload = {}

@bot.message_handler(content_types=['text'])
def echo_all(message):
    try:
        if message.text.startswith("https://www.bartleby.com/questions-and-answers"):
            url = message.text
            headers = {
                'authority': 'www.bartleby.com',
                'cache-control': 'max-age=0',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="92", "Opera";v="78"',
                'sec-ch-ua-mobile': '?0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.231',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.bartleby.com/questions-and-answers/a-4-ft-b-3-ft-c-2-ft-d-2.5-ft-f1-25i20j35k-lb-f2-12i-28j40k-lb-find-the-x-component-of-the-moment-of/0690badb-3510-436b-bcf3-1aa8ed530de8',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': '', 1601057639
                'if-none-match': '"422e3-dnDH/+OSkINYfaZKG2vcMnfRtd0"'
            }

            response = requests.request("GET", url, headers=headers)
            b = BeautifulSoup(response.text, "html.parser")
            uid = re.findall("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", str(message.text))[0]
            print(uid)
            url = f"https://prod-api.bnedcompass.com/qna/answer/{uid}"
            headers = {
                'User-Agent': 'Bartleby/196 CFNetwork/1240.0.4 Darwin/20.5.0',
                'Authorization': 'Bearer 4f6064e00735f1c47e32ad8b60047630c796b099',
            }
            response = requests.request("GET", url, headers=headers)
            stats = json.loads(response.text)['data']['question']['status']
            if ("Rejected") in str(stats):
                bot.send_message(message.chat.id,
                                 "⚠️ *Your Question has been Rejected & Deleted\nتم رفض السؤال وحذفه * ⚠️",
                                 parse_mode='Markdown', reply_to_message_id=message.message_id)
            elif ('Pending') in str(stats):
                bot.send_message(message.chat.id, "⚠️ *Your Question hasn't answered yet\nلم تتم الاجابة بعد* ⚠️",
                                 parse_mode='Markdown', reply_to_message_id=message.message_id)
            else:
                uid = re.findall("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", str(message.text))[0]
                print(uid)
                url = f"https://prod-api.bnedcompass.com/qna/answer/{uid}"
                headers = {
                    'User-Agent': 'Bartleby/196 CFNetwork/1240.0.4 Darwin/20.5.0',
                    'Authorization': 'Bearer 4f6064e00735f1c47e32ad8b60047630c796b099',
                }
                response = requests.request("GET", url, headers=headers)
                stats = json.loads(response.text)['data']['question']['status']
                department = json.loads(response.text)['data']['question']['subjects'][1]['title']
                questionPhoto = json.loads(response.text)['data']['question']
                print(questionPhoto)
                print(questionPhoto['images'])
                if questionPhoto['images'] == []:
                    img = questionPhoto['text']
                elif questionPhoto['images']:
                    qq = questionPhoto['images']
                    img = f"<img src='{qq[0]['imageUrl']}'>"
                x1 = b.find('div', '</div>', class_="styles__MyAnswerStepsWrapper-sc-1fepi3e-6 kEqoef")
                x1.find('div', '</div>', class_="styles__MyAnswerBottomContainer-sc-1fepi3e-9 foOIRd").decompose()
                images = x1.findAll('img')
                f = open("solutions.html", "w", encoding='UTF-8')
                print("reach")
                messagee = str("""
                     <meta charset="UTF-8">
        <html>
          <body>
        <style>
          .x {
            background-color: #bbddc5;

            border:solid red 5px;  }
          .y {
            background-color: white;

            border:solid green 5px;
          }
          .center {
            text-align: center;
          }
                                                                .hidden {
                                                                    display: none;
                                                                }
                                                                i.Icon__IconStyledComponent-sc-kxi3sy-0.hcTcBi.styles__StepperIcon-sc-1fepi3e-7.dZJgAx.material-icons {
                                                                visibility: hidden;}
        </style>
        <h1>
                <div class='center'>
            <p><span class="highlighted-text">الســؤال</span> </p></div>
            </p>
        </h1>
        <div class="x">""" + str(img) + """</div>
        <h1>
                <div class='center'>
                  <p><span class="highlighted-text">الـجواب</span> </p>
                 </div>
        </h1>
        <div class="y"><p><br>""" + str(x1) + """</div></body>

                            """)
                f.write(messagee)
                f.close()
                i = open('./solutions.html', 'rb')
                bot.send_document(message.chat.id, i,caption=f"""تم حصول الحل بنجاح""" ,disable_notification=True, reply_to_message_id=message.message_id)


    except:
        pass



bot.polling(none_stop=True)

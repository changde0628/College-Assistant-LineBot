import os
from datetime import datetime
from flask import Flask, abort, request
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
app = Flask(__name__)
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return "OK"

import requests
import json
def get_QA_answer_test(getanswer_url, body):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Authorization': '3b339818-7351-4ca7-86e1-17733a5a974f'    ## 填入 EndpointKey 後面那亂碼
    }
    url = getanswer_url
    response = requests.request("POST", url, data = body, headers=headers)
    #將json轉成string
    response_text = json.loads(response.text)
    reply_arr = []
    if 'context' in response_text['answers'][0]:
        if len(response_text['answers'][0]['context']['prompts']):
            reply_arr.append(response_text['answers'][0]['answer'])
            tmp = ''
            for i in response_text['answers'][0]['context']['prompts']:
                tmp += i['displayText']
                tmp += ' '
            reply_arr.append(tmp)
            return reply_arr
        else:
            reply_arr.append(response_text['answers'][0]['answer'])
            return reply_arr 
    else:
        reply_arr.append(response_text['answers'][0]['answer'])
        return reply_arr

# 按照格式貼入剛剛要記錄的 Host, Post
getanswer_url = 'https://qna-maker-for-nknu-line-bot.azurewebsites.net/qnamaker/knowledgebases/638b593b-a04a-45cc-8530-39c94685b025/generateAnswer' 
last = 'empty'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    question_sentence_json = json.dumps({"question":get_message})
    answer = get_QA_answer_test(getanswer_url, question_sentence_json)
    if answer[0] == '測驗重新':
        reply_arr = []
        reply_arr.append(TextSendMessage('我們會透過一系列的問題來分析\n你適合就讀什麼科系\n就把我們當成你的好朋友\n用平常說話的方式和我們交談就可以了'))
        reply_arr.append(TextSendMessage('首先，第一個問題 :\n文科/理科/醫科 你對哪個有興趣呢?'))
    elif answer[0] == 'No good match found in KB.':
        reply_arr = []
        reply_arr.append(TextSendMessage('抱歉，我不瞭解你的意思。'))
        reply_arr.append(TextSendMessage('如果你想要重新測驗，可以跟我說你想要再測驗一次喔!'))
    else:
        reply_arr = []
        for i in answer:
            reply_arr.append(TextSendMessage(i))
        if answer[0] == '喜歡創造材料的話，那你適合材料工程學系喔!':
            reply_arr.append(TextSendMessage('國立清華大學 材料科學工程學系\n國立台灣大學 材料科學與工程學系\n國立成功大學 材料科學與工程學系\n國立中興大學 材料科學與工程學系\n國立陽明交通大學 材料科學與工程學系\n國立中央大學 化學工程與材料工程學系\n國立中山大學 材料與光電科學學系'))
        if answer[0] == '喜歡化學反應的話，那你適合化學工程學系或是化學系喔!':
            reply_arr.append(TextSendMessage('國立清華大學 化學系\n國立清華大學 化學工程系\n國立台灣大學 化學系\n國立台灣大學 化學工程學系\n國立成功大學 化學系\n國立成功大學 化學工程學系\n國立中興大學 化學系\n國立中興大學 化學工程學系\n國立陽明交通大學 應用化學系\n國立中央大學 化學學系\n國立中央大學 化學工程與材料工程學系\n國立中山大學 化學系\n國立中正大學 化學暨生物化學系\n國立中正大學 化學工程學系\n國立高雄師範大學 化學系'))
        if answer[0] == '喜歡計算整個地球再加上宇宙的話，那你適合地球科學系喔':
            reply_arr.append(TextSendMessage('國立台灣大學 地質科學系\n國立台灣大學 大氣科學系\n國立成功大學 地球科學系\n國立中央大學 地球科學學系\n國立中央大學 大氣科學學系\n國立中央大學 太空科學與工程學系\n國立中山大學 海洋科學系\n國立中正大學 地球與環境科學系'))
        if answer[0] == '喜歡計算純物理的話，那你適合物理學系喔!':
            reply_arr.append(TextSendMessage('國立政治大學 應用物理系\n國立清華大學 物理學系\n國立清華大學 應用科學系\n國立台灣大學 物理學系\n國立成功大學 物理學系\n國立中興大學 物理學系\n國立陽明交通大學 電子物理學系\n國立中央大學 物理學系\n國立中山大學 物理學系\n國立中正大學 物理學系\n國立高雄師範大學 物理學系'))
        if answer[0] == '喜歡計算數學的話，那你適合數學系喔':
            reply_arr.append(TextSendMessage('國立政治大學 統計學系\n國立政治大學 應用數學系\n國立清華大學 數學系\n國立清華大學 應用數學系\n國立台灣大學 數學系\n國立成功大學 數學系\n國立成功大學 統計學系\n國立中興大學 應用數學系\n國立中央大學 數學系\n國立中山大學 應用數學系\n國立中正大學 數學系\n國立高雄師範大學 數學系'))
        if answer[0] == '喜歡設計電路的話，那你適合電子工程學系或是光電工程學系喔!':
            reply_arr.append(TextSendMessage('國立清華大學 電機工程學系\n國立清華大學 光電工程學系\n國立台灣大學 電機工程學系\n國立成功大學 電機工程學系\n國立成功大學 工程科學系\n國立成功大學 光電科學與工程學系\n國立中興大學 電機工程學系\n國立陽明交通大學 電機工程學系\n國立陽明交通大學 光電工程學學系\n國立陽明交通大學 電子工程學系\n國立中央大學 光電科學與工程學系\n國立中央大學 電機工程學系\n國立中央大學 通訊工程學系\n國立中山大學 電機工程學系\n國立中山大學 光電工程學系\n國立中正大學 電機工程學系\n國立中正大學 通訊工程學系\n國立高雄師範大學 電機工程學系'))
        if answer[0] == '喜歡設計硬體的話，那你適合電機工程學系喔!':
            reply_arr.append(TextSendMessage('國立清華大學 電機工程學系\n國立台灣大學 電機工程學系\n國立成功大學 電機工程學系\n國立成功大學 工程科學系\n國立中興大學 電機工程學系\n國立陽明交通大學 電機工程學系\n國立中央大學 電機工程學系\n國立中央大學 通訊工程學系\n國立中山大學 電機工程學系\n國立中正大學 電機工程學系\n國立中正大學 通訊工程學系\n國立高雄師範大學 電機工程學系'))
        if answer[0] == '喜歡寫程式又會溝通、個性外向的話，那你適合資訊管理學系!':
            reply_arr.append(TextSendMessage('國立政治大學 資訊管理學系\n國立台灣大學 資訊管理學系\n國立中興大學 資訊管理學系\n國立中央大學 資訊管理學系\n國立中山大學 資訊管理學系\n國立中正大學 資訊管理學系\n國立高雄師範大學 軟體工程與管理學系'))
        if answer[0] == '想要保護環境的話，那你適合環境工程學系喔!':
            reply_arr.append(TextSendMessage('國立清華大學 環境與文化資源學系\n國立台灣大學 生物環境系統工程學系\n國立成功大學 環境工程學系\n國立中興大學 水土保持學系'))
        if answer[0] == '喜歡蓋建築的話，那你適合土木工程學系喔!':
            reply_arr.append(TextSendMessage('國立台灣大學 土木工程學系\n國立成功大學 土木工程學系\n國立成功大學 測量及空間資訊學系\n國立成功大學 建築學系\n國立成功大學 都市計畫系\n國立中興大學 土木工程學系\n國立陽明交通大學 土木工程學系\n國立中央大學 土木工程學系'))
        if answer[0] == '喜歡寫程式又比較沈默寡言、個性內向的話，那你適合資訊工程系!':
            reply_arr.append(TextSendMessage('國立政治大學 資訊科學系\n國立清華大學 資訊工程學系\n國立台灣大學 資訊工程學系\n國立成功大學 資訊工程學系\n國立中興大學 資訊科學與工程學系\n國立陽明交通大學 資訊工程學系\n國立中央大學 資訊工程學系\n國立中山大學 資訊工程學系\n國立中正大學 資訊工程學系\n國立高雄師範大學 軟體工程與管理學系'))
    line_bot_api.reply_message(event.reply_token, reply_arr)
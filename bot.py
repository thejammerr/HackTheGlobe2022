from asyncio.windows_events import NULL
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import utils
app = Flask(__name__)
# https://timberwolf-mastiff-9776.twil.io/demo-reply

'''
Global State variables


new_user_flag = True
error_flag = False
bot_state = "" # "form" or "rss"
form_type = ""

'''


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if utils.new_user_flag:
        msg.body("""Hello! Welcome to the Nigerian Land Registration Digital Assistant service. 
        What can I help you with? Please respond with the corresponding menu choice number:
        \n\n
        1. Help me understand something
        2. Help me fill out a form
        """)
        utils.new_user_flag = False
        responded = True
    else:
        if utils.bot_state == "":
            if incoming_msg == "1":
                utils.bot_state = "rss"
                msg.body("""What would you like help with?""")
            elif incoming_msg == "2":
                utils.bot_state = "form"
                msg.body("""Which form process would you like to complete? Please respond with the corresponding menu choice number:
                        \n\n
                        1. Land excision
                        2. Transfer of land ownership
                        3. First-time land registration
                        """)
            else:
                msg.body("Please enter a valid menu choice.")
            responded = True
        elif utils.bot_state == "form":
            pass
        elif utils.bot_state == "rss":
            if 'process' in incoming_msg:
                msg.body('Here are some helpful links with land processes: https://www.bellanaija.com/2021/12/dennis-isong-excision-of-land-in-nigeria/')
            responded = True

    if not responded:
        msg.body("Please enter a valid input.")
    return str(resp)


if __name__ == '__main__':


    app.run()

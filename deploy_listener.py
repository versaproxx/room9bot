from flask import Flask, request
from os import system

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        system('sh new_build.sh')
        return "Webhook received!"

        
         
app.run(host='0.0.0.0', port=1209)
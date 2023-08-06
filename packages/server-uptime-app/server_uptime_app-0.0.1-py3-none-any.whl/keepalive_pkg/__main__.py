from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main(msg="Online"):
    return msg

def run(ip="0.0.0.0", port=8080):
    app.run(host=ip, port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()
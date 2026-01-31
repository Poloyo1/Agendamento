from flask import Flask
from src.controllers.webhook_controller import webhook_handler
from src.database.db import init_db

init_db()


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    return webhook_handler()

if __name__ == "__main__":
    app.run(port=5000)

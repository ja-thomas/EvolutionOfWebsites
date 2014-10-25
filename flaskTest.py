from flask import Flask
from crawler import Crawler
app = Flask(__name__)

@app.route("/")
def hello():
    return Crawler("octoprint.org")

if __name__ == "__main__":
    app.run()

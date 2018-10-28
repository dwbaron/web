from flask import Flask
from config import DevConfig

app = Flask(__name__)

app.config.from_object(DevConfig)

# Import the views module
views = __import__('views')


if __name__ == '__main__':
    app.run()
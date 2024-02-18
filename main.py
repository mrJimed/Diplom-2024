from flask import Flask

from controllers.summarization_controller import summarization_controller

app = Flask(__name__)
app.register_blueprint(summarization_controller)

if __name__ == '__main__':
    app.run(debug=True)

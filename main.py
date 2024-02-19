from flask import Flask
from db_models import db

from controllers.summarization_controller import summarization_controller

app = Flask(__name__)
app.register_blueprint(summarization_controller)

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)

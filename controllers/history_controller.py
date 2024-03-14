from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from db_models import SummarizedText, db

history_controller = Blueprint('history_controller', __name__, url_prefix='/history')


@history_controller.route('', methods=['POST'])
@login_required
def get_summarized_text():
    data = request.get_json()
    new_summarized_text = SummarizedText(
        title=data['title'],
        text=data['text'],
        user_id=current_user.id
    )
    db.session.add(new_summarized_text)
    db.session.commit()
    return '', 200


@history_controller.route('', methods=['GET'])
@login_required
def get_summarized_texts():
    summarized_texts = SummarizedText.query.filter(SummarizedText.user_id == current_user.id).all()
    return jsonify([text.serialize() for text in summarized_texts]), 200

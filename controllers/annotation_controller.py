from flask import Blueprint, request

from services import email_service
from summarization.abstractive.t5_summarizer import T5Summarizer as t5
from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank

annotation_controller = Blueprint('annotation_controller', __name__, url_prefix='/annotation')


@annotation_controller.post('/extractive')
def extractive():
    data = request.get_json()
    text = str(data['text'])
    top_n = int(data['topN'])
    annotation = lexrank.summarize_text(text, top_n, False)
    if bool(data['isSendEmail']):
        to_email = data['toEmail']
        email_service.send_email(
            to_email=to_email,
            subject='Результат аннотирования',
            text=annotation
        )
    return annotation


@annotation_controller.post('/abstractive')
def abstractive():
    data = request.get_json()
    text = str(data['text'])
    annotation = t5().summarize_text(text)
    if bool(data['isSendEmail']):
        to_email = data['toEmail']
        email_service.send_email(
            to_email=to_email,
            subject='Результат аннотирования',
            text=annotation
        )
    return annotation

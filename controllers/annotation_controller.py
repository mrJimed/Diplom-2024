from flask import Blueprint, request
from werkzeug.datastructures.file_storage import FileStorage

from services import email_service
from summarization.abstractive.t5_summarizer import T5Summarizer as t5
from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank

annotation_controller = Blueprint('annotation_controller', __name__, url_prefix='/annotation')


def get_file_content(file: FileStorage):
    return file.stream.read().decode("utf-8")


@annotation_controller.post('/extractive')
def extractive():
    file = request.files['file']
    top_n = int(request.form['topN'])
    text = get_file_content(file)
    annotation = lexrank.summarize_text(text, top_n, False)

    if request.form['isSendEmail'].lower() == 'true':
        to_email = request.form['toEmail']
        email_service.send_email(
            to_email=to_email,
            subject=f'Результат аннотирования для файла \"{file.filename}\"',
            text=annotation
        )
    return annotation


@annotation_controller.post('/abstractive')
def abstractive():
    file = request.files['file']
    text = get_file_content(file)
    annotation = t5().summarize_text(text)

    if request.form['isSendEmail'].lower() == 'true':
        to_email = request.form['toEmail']
        email_service.send_email(
            to_email=to_email,
            subject=f'Результат аннотирования для файла \"{file.filename}\"',
            text=annotation
        )
    return annotation

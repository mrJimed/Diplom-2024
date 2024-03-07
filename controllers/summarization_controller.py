from flask import Blueprint, request

from summarization.abstractive.t5_summarizer import T5Summarizer as t5
from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank

summarization_controller = Blueprint('summarization_controller', __name__, url_prefix='/summarization')


@summarization_controller.route('/extractive', methods=['POST'])
def extractive():
    data = request.get_json()
    text = str(data['text'])
    top_n = int(data['top_n'])
    return lexrank.summarize_text(text, top_n, False)


@summarization_controller.route('/abstractive', methods=['POST'])
def abstractive():
    data = request.get_json()
    text = str(data['text'])
    return t5().summarize_text(text)

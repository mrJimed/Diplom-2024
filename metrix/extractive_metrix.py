from collections import defaultdict

import pandas as pd
from datasets import load_dataset
from nltk import word_tokenize
from nltk.translate import meteor_score
from prettytable import PrettyTable
from rouge import Rouge

from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank
from summarization.extractive.lsa_summarizer import LsaSummarizer as lsa
from summarization.extractive.text_rank_summarizer import TextRankSummarizer as textrank
from summarization.extractive.tfidf_summarizer import TfidfSummarizer as tfidf


def extractive_metrix(summarize_method, top_n: int, lemmatize: bool, n_rows: int) -> list[str]:
    result = []
    dataset = load_dataset('IlyaGusev/gazeta', revision="v2.0", trust_remote_code=True)
    df_test = pd.DataFrame(dataset['train'], columns=['text', 'summary'])
    rouge = Rouge()
    rouges = defaultdict(list)
    meteors = []
    for idx, (text, orig_summary) in enumerate(zip(df_test['text'][:n_rows], df_test['summary'][:n_rows])):
        summary = summarize_method(text=text, top_n=top_n, lemmatize=lemmatize)
        tokenize_summary = word_tokenize(summary)
        tokenize_orig_summary = word_tokenize(orig_summary)
        meteors.append(meteor_score.meteor_score([tokenize_orig_summary], tokenize_summary))
        scores = rouge.get_scores(summary, orig_summary)[0]
        for metric, value in scores.items():
            rouges[metric].append(value['f'])
    result.append(format(sum(meteors) / len(meteors), '.3f'))
    for metric, values in rouges.items():
        result.append(format(sum(values) / len(values), '.3f'))
    return result


top_n = 3
n_rows = 200

table = PrettyTable()
table.field_names = ["-", "METEOR", "rouge-1", "rouge-2", "rouge-L", "lemmatize"]

summarize_methods = {
    'lsa': lsa.summarize_text,
    'tfidf': tfidf.summarize_text,
    'lexrank': lexrank.summarize_text,
    'textrank': textrank.summarize_text
}

for lemmatize in [True, False]:
    for name, method in summarize_methods.items():
        print(f'Начал {name} (lemmatize = {lemmatize})')
        result = extractive_metrix(method, top_n, lemmatize, n_rows)
        table.add_row([name, result[0], result[1], result[2], result[3], lemmatize])
        print(f'Закончил {name} (lemmatize = {lemmatize})\n')

print(table)

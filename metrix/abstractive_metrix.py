from collections import defaultdict

import pandas as pd
from datasets import load_dataset
from nltk.tokenize import word_tokenize
from nltk.translate import meteor_score
from prettytable import PrettyTable
from rouge import Rouge

from summarization.abstractive.bart_summarizer import BartSummarizer as bart
from summarization.abstractive.t5_summarizer import T5Summarizer as t5


def abstractive_metrix(model, max_length: float, min_length: float, n_rows: int = 15) -> list[str]:
    result = []
    dataset = load_dataset('IlyaGusev/gazeta', revision="v2.0", trust_remote_code=True)
    df_test = pd.DataFrame(dataset['train'], columns=['text', 'summary'])
    results = []
    for idx, (text, orig_summary) in enumerate(zip(df_test['text'][:n_rows], df_test['summary'][:n_rows])):
        summarize = model.summarize_text(text, max_length=max_length, min_length=min_length)
        results.append((summarize, orig_summary))
    rouge = Rouge()
    rouges = defaultdict(list)
    meteors = []
    for (summary, orig_summary) in results:
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


max_length = 0.7
min_length = 0.4
n_rows = 200

table = PrettyTable()
table.field_names = ["-", "METEOR", "rouge-1", "rouge-2", "rouge-L"]

summarize_methods = {
    't5': t5(),
    'bart': bart()
}

for name, model in summarize_methods.items():
    print(f'Начал {name}')
    result = abstractive_metrix(model, max_length, min_length, n_rows)
    table.add_row([name, result[0], result[1], result[2], result[3]])
    print(f'Закончил {name}\n')

print(table)

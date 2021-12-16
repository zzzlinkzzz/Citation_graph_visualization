import json
from random import shuffle

def dump_option(file,filename):
    with open(f'./temp/{filename}.json','w') as f:
        json.dump(file,f)

def load_option(filename):
    with open(f'./temp/{filename}.json','r') as f:
        option = json.load(f)
    return option


def search_text(keywords,titles):
    result = []
    index = []
    for i,title in enumerate(titles):
        if keywords in title:
            result.append(title)
            index.append(i)
    if len(result) > 50:
        result = list(zip(result, index))
        shuffle(result)
        result, index = list(zip(*result[:50]))
    return result, index
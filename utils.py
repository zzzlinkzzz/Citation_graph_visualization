import json
from random import shuffle
from pymongo import MongoClient
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.tokenize import MWETokenizer
from autocorrect import Speller
# =============================================================================
db_user = os.environ.get('username')
db_password = os.environ.get('mongo_cn_pass')

client = MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@cluster0.7tetj.mongodb.net/visualization?retryWrites=true&w=majority")
db = client.get_database('visualization')
collection = db.get_collection('citation_network')
# =============================================================================
def find_ref(id_list):
    '''
    tim kiem paper trong database
    return: 
        metadata cua paper trong list (list of object (json))
        danh sach id cac bai bao da trich dan (list of paper id (str))
    '''
    result, ref_list = list(), set()
    for id in id_list:
        items = collection.find({'id': id})
        for item in items:
            result.append(item)
            for ref in item['references']:
                ref_list.add(ref)
        items.close()
    return result, list(ref_list)
# =============================================================================
def dump_option(file,filename):
    with open(f'./temp/{filename}.json','w') as f:
        json.dump(file,f)

def load_option(filename):
    with open(f'./temp/{filename}.json','r') as f:
        option = json.load(f)
    return option
# =============================================================================
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
# =============================================================================
def map_algs(g, alg="barnes"):
    if alg == "barnes":
        g.barnes_hut(gravity=-100000, central_gravity=0.3, spring_length=1000, spring_strength=0.0005, damping=0.09, overlap=0)
    if alg == "forced":
        g.force_atlas_2based()
    if alg == "hr":
        g.hrepulsion()
# =============================================================================
stopwords = load_option('stopwords')
multiwords = load_option('multiwords')
spell = Speller(lang='en')
tokenizer = MWETokenizer(multiwords,separator='_')
# =============================================================================
def remove_symbols(text):
    text = re.sub(r'[^\w]',' ',text)
    return re.sub(' +',' ',text).strip()
# =============================================================================
def tfidf(filename):
    titles = load_option(filename)
    titles = list(map(remove_symbols,titles))
    filted_titles = []
    for title in titles:
        text = ' '.join([spell(word) for word in title.split(' ') if word not in stopwords])
        filted_titles.append(text)
    titles = [' '.join(tokenizer.tokenize(title.split())) for title in filted_titles]
    vectorizer = TfidfVectorizer()
    vector = vectorizer.fit_transform(titles)
    feature_names = vectorizer.get_feature_names()
    denselist = vector.todense()
    denselist = denselist.tolist() #.reshape(denselist.shape[1],-1)
    dump_option(filted_titles, 'temp_filted_titles')
    dump_option(feature_names,'temp_feature_names')
    dump_option(denselist,'temp_denselist')
# =============================================================================




# =============================================================================
if __name__ == '__main__':
    tfidf('base_titles')
    sub_titles = load_option('base_titles')
    feature_names = load_option('base_feature_names')
    denselist = load_option('base_denselist')
    filted_titles = load_option('base_filted_titles')
    text = tokenizer.tokenize(filted_titles[0].split())
    indies = [feature_names.index(x) for x in text]
    score = [round(denselist[0][col_index],3) for col_index in indies]


    
    
    
    
    
    
    
    
    
    
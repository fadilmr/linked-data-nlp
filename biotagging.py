from nltk.tokenize import word_tokenize
import itertools
import re
import pandas as pd
import numpy as np
import string
from tqdm import tqdm

def text_to_tagDF(input):
    try:
         from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
         stopwords = StopWordRemoverFactory().get_stop_words()
    except ModuleNotFoundError:
        stopwords = []
        
    if isinstance(input, pd.Series):
        text = input
    else:
        raise TypeError('Input must be a pandas Series')
    
    punctAndSpace = string.punctuation + ' '
    punctAndSpace = punctAndSpace.replace('(','')
    punctAndSpace = punctAndSpace.replace(')','')
    punctAndSpace = punctAndSpace.replace('.','')
    
    dflist = []
    for i, t in tqdm(enumerate(text)):
        tokens = [[word_tokenize(w), ' '] for w in t.split()]
        tokens = list(itertools.chain(*list(itertools.chain(*tokens))))
        tokens = tokens[:-1]
        
        split_res = []
        for t in tokens:
            if re.match(r'\w+\-\w+.*', t):
                line = t.split('-')
                for i,j in enumerate(line):
                    split_res.append(j)
                    if i < len(line)-1:
                        split_res.append('-')
            else:
                split_res.append(t)
                
        blank = ['' if i.lower() not in list(punctAndSpace) + stopwords else 'O' for i in split_res]
        
        dftemp = pd.DataFrame([split_res, blank]).T
        dftemp.columns = ['token_' + str(i),'BIO_tag_' + str(i)]
        dflist.append(dftemp)
    df = pd.concat(dflist, axis=1)
    
    return df

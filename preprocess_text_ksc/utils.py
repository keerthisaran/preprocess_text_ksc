import re
import os
import sys

import pandas as pd
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
import re
from bs4 import BeautifulSoup
import unicodedata
from textblob import TextBlob
from collections import Counter
from sklearn import model_selection
from collections.abc import Iterable

def _get_word_counts(string):
    length=len(str(string).split())
    return length

def _get_char_counts(string):
    length=len(''.join(string.split()))
    return length

def _get_avg_wordlength(string):
    avg=_get_char_counts(string)/_get_word_counts(string)
    return avg

def _get_stopwords_counts(string):
    length=len([word for word in string.split() if word in stopwords])
    return length
    

def _get_hashtag_counts(string):
    length=len([word for word in string.split() if word.startswith('#')])  
    return length

def _get_mention_counts(string):
    length=len([word for word in string.split() if word.startswith('@')])

def _get_digit_counts(string):
    length=len([word for word in string.split() if word.isdigit()])
  
def _get_uppercase_counts(string):
    length=len([word for word in string.split() if word.isupper()])
    
def _get_expanded(string):
    contractions = { 
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how does",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    " u ": " you ",
    " ur ": " your ",
    " n ": " and ",
    "won't": "would not",
    'dis': 'this',
    'bak': 'back',
    'brng': 'bring'}
    
    if type(string) is str:
        for key,value in contractions.items():
            string=string.replace(key,value)
        return string
    return string
            
def _get_emails(string):
    
    emails=re.findall(r'[^\s]+@[^\s.]+.[^\s]+',string)
    return emails

def _get_email_counts(string):
    emails=_get_emails(string)
    return len(emails)

def _remove_emails(string):
    string=re.sub(r'[^\s]+@[^\s.]+.[^\s]+','',string)
    return string

def _get_urls(string):
    urls=re.findall(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', string)
    return urls

def _get_url_counts(string):
    urls=_get_urls(string)
    return len(urls)

def _remove_urls(string):
    string=re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?','', string)
    return string


def _remove_rt(string):
    string=re.sub(r'\brt\b','',string)
    return string

def _remove_special_chars(string):
    string=re.sub(r'[^\w ]','',string)
    words=string.split()
    string=' '.join(words)
    return string

def _remove_html_tags(string):
     
    string=BeautifulSoup(string, 'lxml').get_text().strip()
    return string

def _remove_accented_chars(string):
    
    string=unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return string

def _make_base(string):
    nlp = spacy.load('en_core_web_sm')

    x_list = []
    doc = nlp(string)
    
    for token in doc:
        lemma = token.lemma_
        if lemma == '-PRON-' or lemma == 'be':
            lemma = token.text

        x_list.append(lemma)
    return ' '.join(x_list)
    
def _remove_common_words(string,n=20):
    
    words=string.split()
    freq_word_counts=Counter(words).most_common(n)
    freq_words=set([word for word,count in freq_word_counts])
    words=[word for word in words if word not in freq_words]
    
    string=' '.join(words)
    return string


def _remove_rare_words(string,n=20):
    
    words=string.split()
    freq_word_counts=Counter(words).most_common()[-n:]
    freq_words=set([word for word,count in freq_word_counts])
    words=[word for word in words if word not in freq_words]
    
    string=' '.join(words)
    return string

def _correct_spells(string):
    string=TextBlob(string).correct()
    return string

    
def _lower(string):
    return str(string).lower()

def _repl_white_newline(string):
    import re
    string=re.sub(r'\n|\s',' ',string)
    return ' '.join(string.split())

def _remove_punct(string,punc_lets):
    
    for p in punc_lets:
        string=string.replace(p,' ')
    
    string=' '.join(string.split())
    
    return string
import string as string_module
def _sep_punct_for_tokens(string,punc_lets=None):
    if punc_lets is None:
        punc_lets=string_module.punctuation+'\n'
    string=re.sub(r'([{punc_lets}])'.format(punc_lets=punc_lets),
                  r' \1 ',string)
    string=' '.join(string.split())
    return string


def _create_folds(folds,label,train_data_path):
      
    train_df=pd.read_csv(train_data_path)
    train_df=train_df.sample(frac=1).reset_index(drop=True)
    kf=model_selection.StratifiedKFold(n_splits=folds)
    train_df['kfold']=-1
    train_df[label]=train_df[label].astype(str)
    for fold_ind,(train_inds,valid_inds) in enumerate(kf.split(train_df,train_df[label])):
        train_df.loc[valid_inds,'kfold']=fold_ind
    
    return train_df

def _apply_pipeline(piple_line,series):
    '''
    args:
        pipeline list of functions and arguments
        pipeline=[
            lower,
            remove_accented_chars,
            get_expanded,
            remove_html_tags,
            remove_urls,
            repl_white_newline,
            sep_punct_for_tokens
    #            [_remove_punct,[',"'+"'"]]
            ]
        series: pandas series
                  
    '''
    for func_and_args in piple_line:
        if isinstance(func_and_args,Iterable):
            func,args=func_and_args
            series=series.apply(lambda x:func(x,*args))
        else:
            func=func_and_args
            series=series.apply(func)
            
        print(str(func),'complete')
    return series

def _create_folds(df,folds,label,shuffle,fold_col='kfold'):
      
    if shuffle:
      df=df.sample(frac=1).reset_index(drop=True)
    kf=model_selection.StratifiedKFold(n_splits=folds)
    df[fold_col]=-1
    df[label]=df[label].astype(str)
    for fold_ind,(train_inds,valid_inds) in enumerate(kf.split(df,df[label])):
        train_df.loc[valid_inds,fold_col]=fold_ind
    
    return df

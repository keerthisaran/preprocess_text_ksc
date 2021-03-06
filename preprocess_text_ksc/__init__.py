from preprocess_text_ksc import utils

__version__='0.0.1'


def get_wordcounts(string):
    return utils._get_word_counts(string)

def get_charcounts(string):
    return utils._get_char_counts(string)

def get_avg_wordlengths(string):
    return utils._get_avg_wordlength(string)

def get_hashtag_counts(string):
    return utils._get_hashtag_counts(string)

def get_mentions_counts(string):
    return utils._get_mention_counts(string)

def get_digit_counts(string):
    return utils._get_digit_counts(string)

def get_upper_case_counts(string):
    return utils._get_uppercase_counts(string)

def get_expanded(string):
    return utils._get_expanded(string)

def get_emails(string):
    return utils._get_emails(string)

def remove_emails(string):
    return utils._remove_emails(string)

def remove_urls(string):
    return utils._remove_urls(string)

def remove_rt(string):
    return utils._remove_rt(string)

def remove_special_chars(string):
    return utils._remove_special_chars(string)

def remove_html_tags(string):
    return utils._remove_html_tags(string)

def remove_accented_chars(string):
    return utils._remove_accented_chars(string)

def make_base(string):
    return utils._make_base(string)

def remove_common_words(string):
    return utils._remove_common_words(string)

def remove_rare_words(string):
    return utils._remove_rare_words(string)

def correct_spells(string):
    return utils._correct_spells(string)

def repl_white_newline(string):
    import re
    string=re.sub(r'\n|\s',' ',string)
    return ' '.join(string.split())

def _remove_punct(string,punc_lets):
    
    
    for p in punc_lets:
        string=string.replace(p,' ')
    
    string=' '.join(string.split())
    
    return string
import string as string_module
import re
def _sep_punct_for_tokens(string,punc_lets=None):
    if punc_lets is None:
        punc_lets=string_module.punctuation+'\n'
    string=re.sub(r'([{punc_lets}])'.format(punc_lets=punc_lets),
                  r' \1 ',string)
    string=' '.join(string.split())
    return string

from collections.abc import Iterable
def apply_pipeline(piple_line,series):
    '''
    args:
        pipeline list of functions and arguments
        pipeline=[
            _lower,
            _remove_accented_chars,
            _get_expanded,
            _remove_html_tags,
            _remove_urls,
            _repl_white_newline,
            _sep_punct_for_tokens
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

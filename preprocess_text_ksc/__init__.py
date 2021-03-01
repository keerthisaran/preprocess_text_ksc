from preprocess_kc import utils

__version__='0.0.1'


def get_wordcounts(string):
    return utils._get_word_counts(string)

def get_charcounts(string):
    return utils._get_char_counts(strings)

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




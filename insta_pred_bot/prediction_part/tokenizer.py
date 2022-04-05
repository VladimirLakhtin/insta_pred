import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem.snowball import SnowballStemmer 
import re
import emoji

def text_transform(text):

    tokens = word_tokenize(text, language='russian')                                         # tokenizing
    tokens_wo_punct = [tok for tok in tokens if tok not in string.punctuation]               # delete punctuation marks
    tokens_wo_sw = [tok for tok in tokens_wo_punct if tok not in stopwords.words('russian')] # delete stop words
    tokens_deemoji = [emoji.demojize(tok) for tok in tokens_wo_sw]                           # decode emoji to delete them
    tokens_wo_emoji = [re.sub(r':[\w-]*:', '', tok) for tok in tokens_deemoji]               # delete emoji

    stemmer = SnowballStemmer(language='russian')                                             
    stemmed_words = [stemmer.stem(word) for word in tokens_wo_emoji if word != '']           # use stemmer

    return stemmed_words
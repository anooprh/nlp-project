__author__ = 'anoop'

from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

print stemmer.stem("running")

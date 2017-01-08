# cPickle in Python 3.x
#http://stackoverflow.com/questions/37132899/installing-cpickle-with-python-3-5
import pickle as cPickle

# open as binary
#http://stackoverflow.com/questions/5016078/problems-with-pickle-and-encodings
marvel = cPickle.load(open("smallG.pkl", 'rb'))
characters = cPickle.load(open("smallChr.pkl", 'rb'))
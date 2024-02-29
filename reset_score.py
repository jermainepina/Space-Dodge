import shelve

""" Run to reset high score to 0"""
d = shelve.open('score.txt')
d['score'] = 0  
d.close()
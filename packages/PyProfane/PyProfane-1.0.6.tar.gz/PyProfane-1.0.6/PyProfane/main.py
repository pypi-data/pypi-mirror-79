import functions
import constants
from constants import profaneWords
from pprint import pprint

if __name__ == "__main__":
    print(functions.censorSentences(['fucking hell']))
    print(len(profaneWords))
    print(len(constants.profaneWords))
    print('fucking' in constants.profaneWords)
    print('fucking' in profaneWords)
    f = open('PyProfane/data/comments.txt')
    lines = f.read().splitlines()
    pprint(functions.censorSentences(lines))

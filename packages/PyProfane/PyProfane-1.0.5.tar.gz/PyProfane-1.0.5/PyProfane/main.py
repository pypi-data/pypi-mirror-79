import functions
import constants
from constants import profaneWords

if __name__ == "__main__":
    print(functions.censorSentences(['fucking hell']))
    print(len(profaneWords))
    print(len(constants.profaneWords))
    print('fucking' in constants.profaneWords)
    print('fucking' in profaneWords)

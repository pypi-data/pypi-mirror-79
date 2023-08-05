import functions
import constants

if __name__ == "__main__":
    print(functions.censorSentences(['fucking hell']))
    print(len(constants.profaneWords))
    functions.updateSwearwords('t.txt')

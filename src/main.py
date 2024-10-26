import sys

import storygen
import character

storygen.run(character.load_directory(sys.argv[1]), int(sys.argv[2]))
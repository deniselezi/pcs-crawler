# Command line interface 

# COMMAND: python3 [link] [max_repos]

import sys


# Gets the arguments from the command line interface
def getArguments(arguments):
    arguments.pop(0) # Removes file name from arguments array

    number_of_arguments = len(arguments)
    print("Number of arguments", number_of_arguments)

    if number_of_arguments <= 1 or number_of_arguments > 2:
        print("Incorrect command usage, please follow the correct format")
        print("COMMAND: python3 [link] [max_repos]")
    return arguments

if __name__ == "__main__":
    # Get arguments in command line
    getArguments(sys.argv)


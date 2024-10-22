import sys


def get_arguments(arguments):
    arguments.pop(0)

    number_of_arguments = len(arguments)
    print("Number of arguments", number_of_arguments)

    if number_of_arguments <= 1 or number_of_arguments > 2:
        print("Incorrect command usage, please follow the correct format")
        print("COMMAND: python3 [link] [max_repos]")
        return []
    return arguments


def validate_arguments(arguments):
    if len(arguments) == 0:
        return

    second_argument = arguments[1]

    try:
        if int(second_argument):
            pass
    except ValueError:
        print("Incorrect command usage, argument 2 is not an integer")


def generate_url(arguments):
    first_argument = arguments[0]
    repo_link = first_argument.split("/")[-2:]
    print(repo_link)
    group_name, repo_name = repo_link[0], repo_link[1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    url = f"https://github.com/search?q=repo%3A{group_name}/{repo_name}%20path%3A.md&type=code"
    print(url)
    return url


if __name__ == "__main__":
    arguments = get_arguments(sys.argv)
    validate_arguments(arguments)
    url = generate_url(arguments)
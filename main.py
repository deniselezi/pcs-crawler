import sys
import os
from crawler import *
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def command_failed():
    return None


def get_arguments(arguments):
    arguments.pop(0)

    number_of_arguments = len(arguments)
    print("Number of arguments", number_of_arguments)

    if number_of_arguments < 1 or number_of_arguments > 2:
        print("Incorrect command usage, please follow the correct format")
        print("COMMAND: python3 [link] [max_repos]")
        return command_failed()
    return arguments


def validate_arguments(arguments):
    if not arguments:
        return command_failed()
    


        

    first_argument = arguments[0]

    try:
        if first_argument.startswith("http"):
            pass
        else:
            return command_failed()
    except ValueError:
        print("Incorrect command usage, argument 1 is not a valid URL.")
        return command_failed()

    if len(arguments) == 2:
        second_argument = arguments[1]
        try:
            if int(second_argument):
                pass
        except ValueError:
            print("Incorrect command usage, argument 2 is not an integer")
            return command_failed()

    return arguments


def generate_url(arguments):
    if not arguments:
        return command_failed()

    first_argument = arguments[0]
    repo_link = first_argument.split("/")[-2:]
    group_name, repo_name = repo_link[0], repo_link[1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    url = f"https://github.com/search?q=repo%3A{group_name}/{repo_name}%20path%3A.md&type=code"
    return url


def create_crawler(url):
    crawler = Crawler(url)
    crawler.crawl(os.getenv("USER"), os.getenv("PASSWORD"))


if __name__ == "__main__":
    arguments = get_arguments(sys.argv)
    arguments_validated = validate_arguments(arguments)
    url = generate_url(arguments_validated)
    if url:
        print("URL:", url)
    else:
        exit()

    create_crawler(url)

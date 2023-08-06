import sys
from colorama import init as init_terminal_colors

from howfairis import HowFairIsChecker


def cli():

    init_terminal_colors()

    print("Checking compliance with fair-software.eu...")

    if len(sys.argv) != 2:
        raise Exception("Expected exactly one argument, i.e. the URL for " +
                        "which GitHub repository to run the analysis.")

    url = sys.argv[1]
    print("Running for {0}".format(url))
    checker = HowFairIsChecker(url)
    checker.deconstruct_url()
    checker.get_readme()
    checker.check_five_recommendations()
    checker.check_badge()


if __name__ == "__main__":
    cli()

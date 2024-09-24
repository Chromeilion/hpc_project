import matplotlib.pyplot as plt
import json


def create_plots(resdic: dict):
    ...


def main():
    saveloc = "./the_results_of_mand.json"
    with open(saveloc, "r") as f:
        resdic = json.load(f)

    create_plots(resdic)


if __name__ == '__main__':
    main()
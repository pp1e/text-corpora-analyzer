import argparse
import time

from typing import List

from corpora_analyzer.corpora_analyzer import CorporaAnalyzer


def pretty_print_paths(doc_paths: List[str]):
    for path in doc_paths:
        print(path)


def main():
    args = parse_arguments()
    analyzer = CorporaAnalyzer(corpora_dir=args.corpora_dir)

    analyzer.print_statistic()

    while True:
        print("Press 1 to show Zipf plot")
        print("Press 2 to show Heaps plot")
        print("Press 3 to check is term exist")
        print("Press 4 to show all documents path for term")
        print("Press 5 to exit")

        choice = input("\nInput your choice: ")
        if choice == '1':
            print("Please wait until the plot will be generated...\n")
            analyzer.show_zipf_plot()
        elif choice == '2':
            print("Please wait until the plot will be generated...\n")
            analyzer.show_heaps_plot()
        elif choice == '3':
            first_term = input("Input the first term: ").strip()
            second_term = input("Input the second term (empty if not needed): ").strip()

            if not second_term:
                second_term = None

            if analyzer.is_term_exists(first_term, second_term):
                print("Exist!\n")
            else:
                print("Not exist :(\n")

        elif choice == '4':
            first_term = input("Input the first term: ").strip()
            second_term = input("Input the second term (empty if not needed): ").strip()

            if not second_term:
                term_as_str = first_term
                second_term = None
            else:
                term_as_str = f'{first_term} {second_term}'

            doc_paths = analyzer.term_word_positions_list(first_term, second_term)
            if doc_paths:
                print(f"Found docs for '{term_as_str}':\n")
                pretty_print_paths(doc_paths)
                print()
            else:
                print(f"'{term_as_str}' not found :(\n")

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print(f"No idea what '{choice}' it is!\n")
            time.sleep(1)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'corpora_dir', type=str, default=""
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()

# Description

Tool to build indexes from text corpora and work with it.

# Installation

To compile installation file, execute `python3 setup.py sdist`.
The file will appear in `dist` folder.

To install package, execute `pip install *path to compiled file*`.

# Dependencies

* `python >= 3.8`.
* Make sure `matplotlip` correctly set up in your system.

# Usage

To build index, create `corpora_analyzer.CorporaAnalyzer` object by passing path to corpora directory in it.
Then you can: 
1. View Zipf and Heaps plots using `show_zipf_plot` and `show_heaps_plot` methods.
2. View overall corpora statistic using `print_statistic` method.
3. Check is term exist in indexes using `is_term_exists` method (if you want to search in inverted index, pass only `first_term`, if in two-word index -- pass `first_term` and `second_term`).
4. Find all documents paths for term using `is_term_exists` method (if you want to search in inverted index, pass only `first_term`, if in two-word index -- pass `first_term` and `second_term`).
5. Save inverted and two-word indexes to files using `save_index_to_file` and `save_tw_index_to_file` methods.

# Example

You can view and use [`run.py`](run.py) as example how to interact with library.
Usage: 
1. Install `corpora-analyzer` package *or* install dependencies via `poetry install` (in this case, make sure you have `poetry` installed).
2. Run via `poetry run python3 run.py *path to corpora directory*`.

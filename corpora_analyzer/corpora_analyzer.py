import datetime
import json
import math
import os
import sys
import typing
from collections import defaultdict

import nltk
from matplotlib import pyplot
from tqdm import tqdm
from typing import Set, List


class CorporaAnalyzer:
    def __init__(
            self,
            corpora_dir: str,
    ):
        # Initialize fields
        if not os.path.isdir(corpora_dir):
            raise ValueError(f"'{corpora_dir}' is not a directory!")
        self.corpora_dir = corpora_dir

        self.inverted_index = defaultdict(set)
        self.two_word_index = defaultdict(set)

        self.documents = {}

        self.corpora_files_count = 0
        self.total_tokens = 0
        self.frequency_dist = nltk.FreqDist()
        self.lemmatizer = nltk.WordNetLemmatizer()

        self.hips_vocab_sizes = []
        self.hips_tokens_numbers = []

        # Build index
        self.download_nltk_dependencies()
        start_time = datetime.datetime.now()
        self.build_index()
        end_time = datetime.datetime.now()
        print(f"Finished in {format(end_time - start_time)}")

    @staticmethod
    def download_nltk_dependencies():
        nltk.download('punkt')
        nltk.download('wordnet')

    def build_index(self):
        current_doc_id = 0
        punctuations = r"""!"#$%&'()*+,–./:;<=>?@[\]^_`{|}~"""

        for root, _, files in os.walk(self.corpora_dir):
            if files:
                print()
                for file in tqdm(files, desc=f'Processing files in {root}'):

                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        self.corpora_files_count += 1
                        text = f.read()
                        cleaned_text = text.translate(str.maketrans('', '', punctuations))
                        tokens = nltk.word_tokenize(cleaned_text)
                        filepath = os.path.join(root, file)
                        self.documents[current_doc_id] = filepath

                        if tokens:
                            self.total_tokens += len(tokens)

                            previous_term = self.normalize_term(tokens[0])
                            self.inverted_index[previous_term].add(current_doc_id)
                            self.frequency_dist.update([previous_term])

                            for i in range(1, len(tokens)):
                                term = self.normalize_term(tokens[i])
                                self.inverted_index[term].add(current_doc_id)
                                self.two_word_index[f'{previous_term} {term}'].add(current_doc_id)
                                self.frequency_dist.update([term])

                                previous_term = term

                            current_doc_id += 1

                    if self.corpora_files_count % 100 == 0:
                        self.hips_vocab_sizes.append(math.log10(self.frequency_dist.N()))
                        self.hips_tokens_numbers.append(math.log10(self.frequency_dist.B()))

    def save_index_to_file(self, filename: str):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.inverted_index))

    def save_tw_index_to_file(self, filename: str):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.two_word_index))

    def print_statistic(self):
        # Report statistics
        print("Corpora files count:", self.corpora_files_count)
        print("Total tokens:", self.total_tokens)
        print("Unique tokens:", len(self.inverted_index))
        print(
            "Inverted index size:",
            round(sys.getsizeof(self.inverted_index) / (1024**3), 3),
            "GB"
        )
        print(
            "Two-word index size:",
            round(sys.getsizeof(self.two_word_index) / (1024**3), 3),
            "GB"
        )
        print(
            "Frequency distribution size:",
            round(sys.getsizeof(self.frequency_dist) / (1024**3), 3),
            "GB"
        )

    def show_zipf_plot(self):
        frequencies = [math.log10(freq) for _, freq in self.frequency_dist.most_common()]
        ranks = list(range(1, len(frequencies) + 1))
        ranks = [math.log10(rank) for rank in ranks]
        pyplot.figure(figsize=(12, 6))
        pyplot.title("Zipf's Law")
        pyplot.plot(ranks, frequencies)
        pyplot.xlabel("Log10(Rank)")
        pyplot.ylabel("Log10(Frequency)")
        pyplot.show()

    def show_heaps_plot(self):
        pyplot.figure(figsize=(12, 6))
        pyplot.title("Heaps' Law")
        pyplot.plot(self.hips_vocab_sizes, self.hips_tokens_numbers)
        pyplot.xlabel("Log10(Vocabulary size)")
        pyplot.ylabel("Log10(Tokens number)")
        pyplot.show()

    def doc_paths_doc_ids(self, doc_ids: Set[int]):
        doc_paths = []
        for doc_id in doc_ids:
            if doc_id in self.documents:
                doc_paths.append(self.documents[doc_id])

        return doc_paths

    def normalize_term(self, term: str) -> str:
        return self.lemmatizer.lemmatize(term.lower())

    def is_term_exists(self, first_term: str, second_term: str = None, should_normalize: bool = True):
        if should_normalize:
            first_term = self.normalize_term(first_term)

        if second_term:
            if should_normalize:
                second_term = self.normalize_term(second_term)
            if f'{first_term} {second_term}' in self.two_word_index:
                return True
        else:
            if first_term in self.inverted_index:
                return True

        return False

    def term_word_positions_iterator(self, first_term: str, second_term: str = None,
                                     should_normalize: bool = True) -> typing.Iterator[str]:
        if should_normalize:
            first_term = self.normalize_term(first_term)

        if second_term:
            if should_normalize:
                second_term = self.normalize_term(second_term)

            two_word_term = f'{first_term} {second_term}'
            if two_word_term in self.two_word_index:
                doc_ids = self.two_word_index[two_word_term]
                return iter(self.doc_paths_doc_ids(doc_ids))
        else:
            if first_term in self.inverted_index:
                doc_ids = self.inverted_index[first_term]
                return iter(self.doc_paths_doc_ids(doc_ids))

        return None

    def term_word_positions_list(self, first_term: str, second_term: str = None,
                                 should_normalize: bool = True) -> List[str]:
        if should_normalize:
            first_term = self.normalize_term(first_term)

        if second_term:
            if should_normalize:
                second_term = self.normalize_term(second_term)

            two_word_term = f'{first_term} {second_term}'
            if two_word_term in self.two_word_index:
                doc_ids = self.two_word_index[two_word_term]
                return self.doc_paths_doc_ids(doc_ids)
        else:
            if first_term in self.inverted_index:
                doc_ids = self.inverted_index[first_term]
                return self.doc_paths_doc_ids(doc_ids)

        return None

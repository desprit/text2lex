"""
Test.
"""
import os
import re
import pickle
from typing import List, Set, Union, Dict

import spacy
from spacy.pipeline import Sentencizer

from vocabulary import prefixes, parts_of_speech
from shared.config import NLP_SERVICE_ROOT, NLP_ASSETS_FOLDER


class Relic:
    """
    Keep information about specific token.
    """

    lemma: str
    pos: str
    example: str
    i: int
    idx: int
    score: int
    translations: List[str]

    def __init__(
        self, token: spacy.tokens.token.Token, sentence: spacy.tokens.span.Span
    ):

        self.lemma = token.lemma_.lower().strip()
        self.pos = token.pos_
        self.i = token.i
        self.idx = token.idx
        self.example = sentence.string

    def as_dict(self) -> Dict[str, Union[str, int]]:
        """
        Return dict representation of the Relic.
        """

        return self.__dict__

    def set_score(self, score: int):
        """
        Assign score value.
        """

        self.score = score

    def set_translations(self, translations: List[str]):
        """
        Assign translations value.
        """

        self.translations = translations


class Dictionary:
    """
    Keep information about extracted lemmas.
    """

    _relics: List[Relic]
    _lemmas: Set[str]
    _ignore: List[str]
    _debug: bool
    _count: int
    _frequency: Dict[str, int]
    _translations: Dict[str, List[Dict[str, str]]]

    def __init__(self, debug: bool = False):
        self._relics = []
        self._lemmas = set()
        self._ignore = ["PUNCT", "SPACE", "ADP", "DET", "PART", "NUM"]
        self._debug = debug
        self._count = 0
        self._frequency = {}
        self._translations = {}
        self._parse_frequency()
        self._parse_translations()

    def _parse_frequency(self):
        """
        Parse frequency list.
        """

        with open(f"{NLP_ASSETS_FOLDER}/frequency.txt") as f:
            content = f.readlines()
            for i, line in enumerate(content, start=1):
                self._frequency[line.strip()] = i

    def _parse_translations(self) -> None:
        """
        Parse translations dictionary.
        """

        lines = []
        with open(f"{NLP_ASSETS_FOLDER}/mueller.koi", encoding="koi8-r") as f:
            lines = f.readlines()
        for _, line in enumerate(lines, start=1):
            if line.startswith("_") or line.startswith(" "):
                continue
            word = line.strip().split("  ")[0].lower()
            translation_string = line.split("  ")[-1]
            translation_string = re.sub(
                r"(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})",
                "1.",
                translation_string,
            )
            translations = []
            by_part_of_speech = re.split(r"\d+\.", translation_string)
            by_part_of_speech = [ps.strip() for ps in by_part_of_speech]
            for ps in by_part_of_speech:
                pos = next((p for p in parts_of_speech if p in ps), None)
                if pos:
                    ps = ps.replace(pos, "").strip()
                    pos = parts_of_speech[pos]
                else:
                    continue
                versions = re.split(r"\d+>", ps)
                versions = [v.strip() for v in versions]
                for version in versions:
                    version = version.split(";")[0].strip()
                    version = re.sub(r"_comp\..+?$", "", version)
                    version = re.sub(r"_sup\..+?$", "", version)
                    version = re.sub(r"_Syn:.+?$", "", version)
                    version = re.sub(r" - .+?$", "", version)
                    for prefix in prefixes:
                        version = version.replace(prefix, "").strip()
                    if not version:
                        continue
                    translations.append({"text": version, "pos": pos})
            self._translations[word] = translations

    def add(self, relic: Relic) -> None:
        """
        Add relic to the dictionary.
        """

        self._count += 1

        if relic.pos in self._ignore:
            if self._debug:
                print(f"{relic.pos} is in ignore list, skipping")
            return
        if relic.lemma in self._lemmas:
            if self._debug:
                print(f"{relic.lemma} already present, skipping")
            return
        self._lemmas.add(relic.lemma)
        score = self.get_lemma_score(relic.lemma)
        relic.set_score(score)
        translations = self.get_lemma_translations(relic.lemma, relic.pos)
        relic.set_translations(translations)
        self._relics.append(relic)

    def get_lemma_score(self, lemma: str) -> int:
        """
        Return a score from a frequency list for a given lemma.
        """

        return self._frequency.get(lemma, -1)

    def get_lemma_translations(self, lemma: str, pos: str) -> Dict[str, str]:
        """
        Return a translations from a translations list for a given lemma.
        """

        translations = self._translations.get(lemma, [])
        pos_translations = next((t for t in translations if pos in t["pos"]), None)
        if not pos_translations:
            return translations
        return pos_translations

    def count(self) -> int:
        """
        Return the number of tokens added to the dictionary.
        """

        return self._count

    def count_unique(self) -> int:
        """
        Return the number of lemmas in the storage.
        """

        return len(self._lemmas)

    def get_lemmas(self) -> Set[str]:
        """
        Return a list of all lemmas in the storage.
        """

        return self._lemmas

    def get_relics(self, sort: bool = False, as_dict: bool = False) -> List[Relic]:
        """
        Return a list of all relics in the storage.
        """

        if sort:
            relics = sorted(self._relics, key=lambda relic: relic.score)
        else:
            relics = self._relics
        if as_dict:
            relics = [t.as_dict() for t in relics]

        return relics

    def get_lemma_info(self, lemma: str) -> Union[Relic, None]:
        """
        Return a relic for the given lemma.
        """

        return next((t for t in self._relics if t.lemma == lemma), None)


def process_text(text: str, debug: bool = False) -> Dictionary:
    """
    Process given text through NLP pipes.
    """

    nlp = spacy.load("en_core_web_sm")
    sentencizer = Sentencizer()
    nlp.add_pipe(sentencizer, before="parser")
    doc = nlp(text)
    dictionary_path = f"{NLP_SERVICE_ROOT}/assets/dictionary.pickle"

    if os.path.isfile(dictionary_path) and not debug:
        with open(dictionary_path, "rb") as f:
            dictionary = pickle.load(f)
    else:
        dictionary = Dictionary(debug=False)
        with open(dictionary_path, "wb") as w:
            pickle.dump(dictionary, w)

    for sentence in doc.sents:
        for token in sentence:
            relic = Relic(token, sentence)
            dictionary.add(relic)

    return dictionary


def main() -> None:
    """
    Module entry point.
    """

    text = "hello world"
    process_text(text)


if __name__ == "__main__":
    main()

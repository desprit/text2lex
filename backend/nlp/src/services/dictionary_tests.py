"""
Tests for backend/nlp/src/services/dictionary.py
"""
import spacy
from spacy.pipeline import Sentencizer

from services import dictionary
from shared.tests.base import TestsBaseClass


nlp = spacy.load("en_core_web_sm")
sentencizer = Sentencizer()
nlp.add_pipe(sentencizer, before="parser")
sample_text = "You are not prepared!"
doc = nlp(sample_text)
for sentence in doc.sents:
    for token in sentence:
        relic = dictionary.Relic(token, sentence)
        break
    break


class DictionaryTests(TestsBaseClass):
    """
    Tests for backend/nlp/src/services/dictionary.py
    """

    def test_01_test_relic_class_init(self):
        """
        Should contain required properties.
        """

        for prop in ["lemma", "pos", "i", "idx", "example"]:
            self.assertTrue(hasattr(relic, prop))

    def test_02_test_relic_class_as_dict(self):
        """
        Should return correct data type.
        """

        self.assertIsInstance(relic.as_dict(), dict)

    def test_03_test_relic_class_set_score(self):
        """
        Should set score value.
        """

        relic.set_score(10)
        self.assertEqual(relic.score, 10)

    def test_04_test_relic_class_set_translations(self):
        """
        Should set value of translations property.
        """

        translations = ["1", "2", "3"]
        relic.set_translations(translations)
        self.assertListEqual(relic.translations, translations)

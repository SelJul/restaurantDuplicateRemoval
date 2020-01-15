from unittest import TestCase

from fmt_methods import levenshtein, dice_coefficient, soundex


class TestLevenshtein(TestCase):
    def test_levenshtein_empty(self):
        assert levenshtein("", "") == 0

    def test_levenshtein_same(self):
        assert levenshtein("hallo", "hallo") == 0

    def test_levenshtein_substitution(self):
        assert levenshtein("hallo", "tallo") == 1

    def test_levenshtein_insertion(self):
        assert levenshtein("hallo", "hallog") == 1

    def test_levenshtein_delete(self):
        assert levenshtein("hallo", "halo") == 1

    def test_levenshtein_s_s(self):
        assert levenshtein("hallo", "halon") == 2

    def test_levenshtein_s_i(self):
        assert levenshtein("hallo", "halg") == 2

    def test_levenshtein_s_d(self):
        assert levenshtein("tier", "tor") == 2


class TestDiceCoefficient(TestCase):
    def test_dice_coefficient_empty(self):
        assert dice_coefficient("", "") == 1.0

    def test_dice_coefficient_a_empty(self):
        assert dice_coefficient("", "test") == 0.0

    def test_dice_coefficient_b_empty(self):
        assert dice_coefficient("test", "") == 0.0

    def test_dice_coefficient_same_value(self):
        assert dice_coefficient("test", "test") == 1.0

    def test_dice_coefficient_values_switched(self):
        assert dice_coefficient("test name", "name test") == 1.0

    def test_dice_coefficient_white_spaces(self):
        assert dice_coefficient("   test name", "test   name") == 1.0

    def test_dice_coefficient_different_values(self):
        assert dice_coefficient("super test name", "super test na") != 1.0


class TestSoundex(TestCase):
    def test_soundex_empty(self):
        assert soundex("") == "0000"

    def test_soundex_one_char_case_1(self):
        assert soundex("a") == "a000"

    def test_soundex_one_char_case_2(self):
        assert soundex("z") == "z000"

    def test_soundex_vowel(self):
        assert soundex("aeii") == "a000"

    def test_soundex_char_repetition(self):
        assert soundex("abbbba") == "a100"

    def test_soundex(self):
        assert soundex("abrakadabra") == "a162"

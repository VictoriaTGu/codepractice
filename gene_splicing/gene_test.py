import unittest

from gene import find_index_of_overlap
from gene import get_substring_match
from gene import concat_two_seqs
from gene import find_substring_pairs
from gene import get_head
from gene import concat_sequences
from linked_lst import SeqList
from linked_lst import Node


class TestConcatSeqs(unittest.TestCase):
    def test_find_index_of_overlap(self):
        fst_string = 'CCAGTAC'
        snd_string = 'AGTAC'
        assert find_index_of_overlap(fst_string, snd_string) == 2

    def test_find_index_of_overlap_one_char(self):
        fst_string = 'CCAGTAC'
        snd_string = 'C'
        assert find_index_of_overlap(fst_string, snd_string) == 6

    def test_find_index_of_overlap_no_match(self):
        fst_string = 'CCAGTAC'
        snd_string = ''
        assert find_index_of_overlap(fst_string, snd_string) is None

    def test_get_substring_match(self):
        fst_string = 'CCAGTAC'
        snd_string = 'AGTACGG'
        assert get_substring_match(fst_string, snd_string) == 2

    def test_get_substring_one_char_match(self):
        fst_string = 'CCAGTAC'
        snd_string = 'CGTACGG'
        assert get_substring_match(fst_string, snd_string) == 6

    def test_get_substring_no_match(self):
        fst_string = 'CCAGTAC'
        snd_string = 'GGTACGG'
        assert get_substring_match(fst_string, snd_string) is None

    def test_concat_sequences(self):
        fst_string = 'CCAGTAC'
        snd_string = 'AGTACGG'
        assert concat_two_seqs(fst_string, snd_string, 2) == 'CCAGTACGG'

    def test_find_substring_pairs(self):
        seq_lst = SeqList(['AAGT', 'GTCA', 'CATT'])
        fst_to_snd_match = {'AAGT': ('GTCA', 2), 'GTCA': ('CATT', 2)}
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        m1, m2 = find_substring_pairs(seq_lst)
        for head, (tail, ind) in m1.iteritems():
            assert str(head) in fst_to_snd_match
            assert fst_to_snd_match[str(head)] == (str(tail), ind)
        assert len(fst_to_snd_match) == len(m1)
        for head, tail in m2.iteritems():
            assert str(head) in snd_to_fst_match
            assert snd_to_fst_match[str(head)] == str(tail)
        assert len(snd_to_fst_match) == len(m2)

    def test_find_substring_pairs_out_of_order(self):
        seq_lst = SeqList(['CATT', 'GTCA', 'AAGT'])
        fst_to_snd_match = {'AAGT': ('GTCA', 2), 'GTCA': ('CATT', 2)}
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        m1, m2 = find_substring_pairs(seq_lst)
        for head, (tail, ind) in m1.iteritems():
            assert str(head) in fst_to_snd_match
            assert fst_to_snd_match[str(head)] == (str(tail), ind)
        assert len(fst_to_snd_match) == len(m1)
        for head, tail in m2.iteritems():
            assert str(head) in snd_to_fst_match
            assert snd_to_fst_match[str(head)] == str(tail)
        assert len(snd_to_fst_match) == len(m2)


    def test_get_head(self):
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        assert get_head(snd_to_fst_match) == 'AAGT'

    def test_concat_sequences(self):
        seq_lst = ['AAGT', 'GTCA', 'CATT']
        result = concat_sequences(seq_lst)
        assert concat_sequences(seq_lst) == 'AAGTCATT'

    def test_concat_sequences_out_of_order(self):
        seq_lst = ['CATT', 'GTCA', 'AAGT']
        result = concat_sequences(seq_lst)
        assert concat_sequences(seq_lst) == 'AAGTCATT'

    def test_concat_larger_sequences(self):
        seq_lst = ['CATTG', 'GTCAT', 'AAGT', 'CAAA']
        result = concat_sequences(seq_lst)
        assert concat_sequences(seq_lst) == 'CAAAGTCATTG'

    def test_even_larger_sequences(self):
        seq_lst = ['ATTAGACCTG', 'CCTGCCGGAA', 'AGACCTGCCG', 'GCCGGAATAC']
        result = concat_sequences(seq_lst)
        assert concat_sequences(seq_lst) == 'ATTAGACCTGCCGGAATAC'


if __name__ == "__main__":
    unittest.main()

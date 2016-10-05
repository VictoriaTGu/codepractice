import unittest
from sequence_list import SeqList

class TestSeqList(unittest.TestCase):
    def test_create_seq_lst(self):
        seq_lst = ['AB', 'BC', 'CD']
        s = SeqList(seq_lst)
        for i, seq in enumerate(s):
            assert seq_lst[i] == str(seq)
        assert len(seq_lst) == len(s)

    def test_remove(self):
        seq_lst = ['AB', 'BC', 'CD']
        s = SeqList(seq_lst)
        s.remove(s.head_node.next_node)
        new_seq_lst = ['AB', 'CD']
        for i, seq in enumerate(s):
            assert new_seq_lst[i] == str(seq)
        assert len(new_seq_lst) == len(s)

    def test_remove_head(self):
        seq_lst = ['AB', 'BC', 'CD']
        s = SeqList(seq_lst)
        s.remove(s.head_node)
        new_seq_lst = ['BC', 'CD']
        for i, seq in enumerate(s):
            assert new_seq_lst[i] == str(seq)
        assert len(new_seq_lst) == len(s)

    def test_remove_tail(self):
        seq_lst = ['AB', 'BC', 'CD']
        s = SeqList(seq_lst)
        tail = s.head_node.next_node.next_node
        s.remove(tail)
        new_seq_lst = ['AB', 'BC']
        for i, seq in enumerate(s):
            assert new_seq_lst[i] == str(seq)
        assert len(new_seq_lst) == len(s)

if __name__ == "__main__":
    unittest.main()

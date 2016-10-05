import unittest

class Node(object):
    def __init__(self, seq):
        self.seq = seq
        self.next_node = None
        self.prev_node = None

    def __eq__(self, other_node):
        return self.seq == other_node.seq

    def __str__(self):
        return self.seq

    def __len__(self):
        return len(self.seq)

class SeqList(object):
    def __init__(self, seq_lst):
        self.head_node = None
        self.create_list(seq_lst)

    def create_list(self, seq_lst):
        if len(seq_lst) < 1:
            return
        self.head_node = Node(seq_lst[0])
        prev_node = self.head_node
        if len(seq_lst) < 2:
            return
        for seq in seq_lst[1:]:
            new_node = Node(seq)
            prev_node.next_node = new_node
            new_node.prev_node = prev_node
            prev_node = new_node

    def __iter__(self):
        node = self.head_node
        while node is not None:
            yield node
            node = node.next_node

    def is_empty(self):
        return len(self) == 0

    def __len__(self):
        node = self.head_node
        counter = 0
        while node is not None:
            node = node.next_node
            counter += 1
        return counter

    def peek(self):
        return self.head_node

    def remove(self, node_to_remove):
        # need to update the head of the list
        preceding_node = node_to_remove.prev_node
        following_node = node_to_remove.next_node
        if following_node:
            following_node.prev_node = preceding_node
        if preceding_node:
            preceding_node.next_node = following_node
            self.head_node = preceding_node
        else:
            self.head_node = following_node

class TestSeqList(unittest.TestCase):
    def test_create_linked_lst(self):
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

if __name__ == "__main__":
    unittest.main()

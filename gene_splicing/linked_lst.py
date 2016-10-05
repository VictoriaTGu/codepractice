import unittest

class Node(object):
    def __init__(self, gene):
        self.gene = gene
        self.next_node = None
        self.prev_node = None

    def remove_node(self):
        # need to return the head of the list
        preceding_node = self.prev_node
        following_node = self.next_node
        if following_node:
            following_node.prev_node = preceding_node
        if preceding_node:
            preceding_node.next_node = following_node
            return preceding_node
        else:
            return following_node

def create_linked_list(seq_lst):
    head_node = Node(seq_lst[0])
    prev_node = head_node
    for gene in seq_lst[1:]:
        new_node = Node(gene)
        prev_node.next_node = new_node
        new_node.prev_node = prev_node
        prev_node = new_node
    return head_node


class TestLinkedList(unittest.TestCase):
    def test_create_linked_lst(self):
        seq_lst = ['AB', 'BC', 'CD']
        node = create_linked_list(seq_lst)
        for seq in seq_lst:
            assert node.gene == seq
            node = node.next_node
        assert node is None

    def test_remove_node(self):
        seq_lst = ['AB', 'BC', 'CD']
        head_node = create_linked_list(seq_lst)
        new_head = head_node.next_node.remove_node()
        node = new_head
        new_seq_lst = ['AB', 'CD']
        for seq in new_seq_lst:
            assert node.gene == seq
            node = node.next_node
        assert node is None

    def test_remove_head(self):
        seq_lst = ['AB', 'BC', 'CD']
        head_node = create_linked_list(seq_lst)
        new_head = head_node.remove_node()
        node = new_head
        new_seq_lst = ['BC', 'CD']
        for seq in new_seq_lst:
            assert node.gene == seq
            node = node.next_node
        assert node is None

if __name__ == "__main__":
    unittest.main()

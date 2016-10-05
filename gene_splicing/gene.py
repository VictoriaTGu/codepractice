import unittest

class Node(object):

    def __init__(self, gene):
        self.gene = gene
        self.next_node = None
        self.prev_node = None

def find_index_of_overlap(fst_string, snd_string):
    fst_index = len(fst_string) - 1
    snd_index = len(snd_string) - 1
    if snd_index < 0:
        return None
    while snd_index >= 0:
        if fst_index < 0 or fst_string[fst_index] != snd_string[snd_index]:
            return None
        else:
            fst_index -= 1
            snd_index -= 1
    return fst_index + 1


def get_substring_match(fst_string, snd_string):
    # start from the end of the string and find a match
    for snd_index in xrange(len(snd_string)-1, 0, -1):
        fst_index = find_index_of_overlap(fst_string, snd_string[:snd_index])
        if fst_index is not None:
            return fst_index


def concat_two_genes(gene1, gene2, gene1_index):
    return gene1[:gene1_index] + gene2


def find_substring_pairs(seq_lst):
    fst_to_snd_match = {}
    snd_to_fst_match = {}
    paired = set()
    for i, gene in enumerate(seq_lst):
        for j, other_gene in enumerate(seq_lst):
            if i != j and other_gene not in paired:
                index_of_match = get_substring_match(gene, other_gene)
                if index_of_match is not None and index_of_match <= len(gene) / 2:
                    fst_to_snd_match[gene] = (other_gene, index_of_match)
                    snd_to_fst_match[other_gene] = gene
                    paired.add(gene)
                    paired.add(other_gene)
    return fst_to_snd_match, snd_to_fst_match


def get_head(snd_to_fst_match):
    gene = snd_to_fst_match.keys()[0]
    while gene in snd_to_fst_match:
        gene = snd_to_fst_match[gene]
    return gene


def splice_into_single_genome(seq_lst):
    unpaired_sequences = create_linked_list(seq_lst)
    fst_to_snd_match, snd_to_fst_match = find_substring_pairs(seq_lst)
    gene = get_head(snd_to_fst_match)
    result = gene
    result_index = 0
    while gene in fst_to_snd_match:
        next_gene, index = fst_to_snd_match[gene]
        result = concat_two_genes(result, next_gene, result_index + index)
        result_index += index
        gene = next_gene
    return result

def create_linked_list(seq_lst):
    head_node = Node(seq_lst[0])
    prev_node = head_node
    for gene in seq_lst[1:]:
        new_node = Node(gene)
        prev_node.next_node = new_node
        new_node.prev_node = prev_node
        prev_node = new_node
    return head_node

def remove_node(node_to_remove):
    # need to return the head of the list
    preceding_node = node_to_remove.prev_node
    following_node = node_to_remove.next_node
    if following_node:
        following_node.prev_node = preceding_node
    if preceding_node:
        preceding_node.next_node = following_node
        return preceding_node
    else:
        return following_node


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
        remove_node(head_node.next_node)
        node = head_node
        new_seq_lst = ['AB', 'CD']
        for seq in new_seq_lst:
            assert node.gene == seq
            node = node.next_node
        assert node is None


class TestMatchGene(unittest.TestCase):
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

    def test_splice_into_single_genome(self):
        fst_string = 'CCAGTAC'
        snd_string = 'AGTACGG'
        assert concat_two_genes(fst_string, snd_string, 2) == 'CCAGTACGG'

    def test_find_substring_pairs(self):
        seq_lst = ['AAGT', 'GTCA', 'CATT']
        fst_to_snd_match = {'AAGT': ('GTCA', 2), 'GTCA': ('CATT', 2)}
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        m1, m2 = find_substring_pairs(seq_lst)
        assert m1 == fst_to_snd_match
        assert m2 == snd_to_fst_match

    def test_get_head(self):
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        assert get_head(snd_to_fst_match) == 'AAGT'

    def test_splice_into_single_genome(self):
        seq_lst = ['AAGT', 'GTCA', 'CATT']
        result = splice_into_single_genome(seq_lst)
        assert splice_into_single_genome(seq_lst) == result


if __name__ == "__main__":
    unittest.main()



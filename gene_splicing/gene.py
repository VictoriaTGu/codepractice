import unittest


def get_substring_match(fst_string, snd_string):
    # start from the end of the string and find a match
    fst_string_index = len(fst_string) - 1
    snd_string_index = len(snd_string) - 1
    while snd_string_index >= 0:
        if fst_string[fst_string_index] != snd_string[snd_string_index]:
            snd_string_index -= 1
        else:
            # check for match at that index
            match = True
            for i in range(snd_string_index, -1, -1):
                if fst_string[fst_string_index] != snd_string[i]:
                    match = False
                else:
                    fst_string_index -= 1
            if match:
                return fst_string_index + 1

def concat_two_genes(gene1, gene2, gene1_index):
    return gene1[:gene1_index] + gene2

def find_substring_pairs(gene_lst):
    fst_to_snd_match = {}
    snd_to_fst_match = {}
    paired = set()
    for i, gene in enumerate(gene_lst):
        for j, other_gene in enumerate(gene_lst):
            if i != j and other_gene not in paired:
                index_of_match = get_substring_match(gene, other_gene)
                if index_of_match is not None and index_of_match >= len(gene) / 2:
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


def splice_into_single_genome(gene_lst):
    fst_to_snd_match, snd_to_fst_match = find_substring_pairs(gene_lst)
    gene = get_head(snd_to_fst_match)
    result = gene
    result_index = 0
    while gene in fst_to_snd_match:
        next_gene, index = fst_to_snd_match[gene]
        result = concat_two_genes(result, next_gene, result_index + index)
        result_index += index
        gene = next_gene
    return result


class TestMatchGene(unittest.TestCase):
    def test_get_substring_match(self):
        fst_string = 'CCAGTAC'
        snd_string = 'AGTACGG'
        assert get_substring_match(fst_string, snd_string) == 2

    def test_splice_into_single_genome(self):
        fst_string = 'CCAGTAC'
        snd_string = 'AGTACGG'
        assert concat_two_genes(fst_string, snd_string, 2) == 'CCAGTACGG'

    def test_find_substring_pairs(self):
        gene_lst = ['AAGT', 'GTCA', 'CATT']
        fst_to_snd_match = {'AAGT': ('GTCA', 2), 'GTCA': ('CATT', 2)}
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        m1, m2 = find_substring_pairs(gene_lst)
        assert m1 == fst_to_snd_match
        assert m2 == snd_to_fst_match

    def test_get_head(self):
        snd_to_fst_match = {'GTCA': 'AAGT', 'CATT': 'GTCA'}
        assert get_head(snd_to_fst_match) == 'AAGT'

    def test_splice_into_single_genome(self):
        gene_lst = ['AAGT', 'GTCA', 'CATT']
        result = splice_into_single_genome(gene_lst)
        assert splice_into_single_genome(gene_lst) == result



if __name__ == "__main__":
    unittest.main()



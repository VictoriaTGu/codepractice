import unittest
from linked_lst import Node
from linked_lst import create_linked_list


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


def get_substring_match(fst_string, snd_string):
    # start from the end of the string and find a match
    for snd_index in xrange(len(snd_string)-1, 0, -1):
        fst_index = find_index_of_overlap(fst_string, snd_string[:snd_index])
        if fst_index is not None:
            return fst_index

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


def concat_two_genes(gene1, gene2, gene1_index):
    return gene1[:gene1_index] + gene2


def get_head(snd_to_fst_match):
    gene = snd_to_fst_match.keys()[0]
    while gene in snd_to_fst_match:
        gene = snd_to_fst_match[gene]
    return gene

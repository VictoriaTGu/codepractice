import unittest
from linked_lst import SeqList


def concat_seq_lst(seq_lst):
    unpaired_sequences = SeqList(seq_lst)
    head_to_tail, tail_to_head = find_substring_pairs(unpaired_sequences)
    first_seq = get_head(tail_to_head)
    result = str(first_seq)
    result_index = 0
    seq = first_seq
    while seq in head_to_tail:
        next_seq, index = head_to_tail[seq]
        result = concat_two_seqs(result, next_seq, result_index + index)
        result_index += index
        seq = next_seq
        return result


def find_substring_pairs(unpaired_sequences):
    head_to_tail = {}
    tail_to_head = {}
    while len(unpaired_sequences) > len(head_to_tail):
        current_seq = unpaired_sequences.peek()
        for other_seq in unpaired_sequences:
            if current_seq != other_seq:
                index_of_match = get_substring_match(str(current_seq), str(other_seq))
                if index_of_match is not None and index_of_match <= len(current_seq) / 2:
                    head_to_tail[current_seq] = (other_seq, index_of_match)
                    tail_to_head[other_seq] = current_seq
                    unpaired_sequences.remove(current_seq)
                    break
    return head_to_tail, tail_to_head


def get_substring_match(head_seq, tail_seq):
    # start from the end of the second string and find a match
    for snd_index in xrange(len(tail_seq)-1, 0, -1):
        fst_index = find_index_of_overlap(head_seq, tail_seq[:snd_index])
        if fst_index is not None:
            return fst_index


def find_index_of_overlap(head_seq, tail_seq):
    fst_index = len(head_seq) - 1
    snd_index = len(tail_seq) - 1
    if snd_index < 0:
        return None
    while snd_index >= 0:
        if fst_index < 0 or head_seq[fst_index] != tail_seq[snd_index]:
            return None
        else:
            fst_index -= 1
            snd_index -= 1
    return fst_index + 1


def concat_two_seqs(seq1, seq2, seq1_index):
    return str(seq1)[:seq1_index] + str(seq2)


def get_head(tail_to_head):
    if len(tail_to_head) == 0:
        return None
    seq = tail_to_head.keys()[0]
    while seq in tail_to_head:
        seq = tail_to_head[seq]
    return seq

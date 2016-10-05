import unittest
from linked_lst import SeqList


def concat_sequences(seq_lst):
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
    following_seq = None
    counter = 0
    while len(unpaired_sequences):
        # we only need to search for previous seq
        counter += 1
        if following_seq:
            current_seq = following_seq['seq']
            unpaired_sequences.remove(current_seq)
            following_seq = search_for_following_seq(current_seq, unpaired_sequences)
        else:
            current_seq = unpaired_sequences.peek()
            unpaired_sequences.remove(current_seq)
            prev_seq = search_for_prev_seq(current_seq, unpaired_sequences)
            following_seq = search_for_following_seq(current_seq, unpaired_sequences)

        # store information
        if prev_seq:
            head_to_tail[prev_seq['seq']] = (current_seq, prev_seq['index'])
            tail_to_head[current_seq] = prev_seq['seq']
        if following_seq:
            head_to_tail[current_seq] = (following_seq['seq'], following_seq['index'])
            tail_to_head[following_seq['seq']] = current_seq
    return head_to_tail, tail_to_head


def search_for_prev_seq(current_seq, unpaired_sequences):
    for other_seq in unpaired_sequences:
        index_of_match = get_substring_match(str(other_seq), str(current_seq))
        if index_of_match is not None and index_of_match <= len(current_seq) / 2:
            return {'seq': other_seq, 'index': index_of_match}


def search_for_following_seq(current_seq, unpaired_sequences):
    following_seq = None
    for other_seq in unpaired_sequences:
        index_of_match = get_substring_match(str(current_seq), str(other_seq))
        if index_of_match is not None and index_of_match <= len(current_seq) / 2:
            return {'seq': other_seq, 'index': index_of_match}


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

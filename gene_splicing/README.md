## Overview
The input to this problem is a list of DNA sequences (at most 50 of them), each of which has a length not exceeding 1000 characters.

The problem can be broken down into several main pieces:

1. Determining whether two DNA sequences should be glued together

2. Pairing up the DNA sequences to be glued together 

3. Gluing all the pairs of sequences together into one long sequence

The brute force approach for part 1 has a time complexity of O(k^2) where k is the length of each individual sequence. In this case k=100.

The brute force approach for part 2 can lead to combinatorial explosion (50 choose 2) because you need to evaluate for each pair of sequences whether they should be glued together.
It might not seem to matter with just 50 DNA sequence, but from my experience years ago in genomics, I believe that n is likely to grow a lot more quickly than k (there could be millions of short reads that are spliced together to create a complete genome).
Since factorial growth is much greater than polynomial growth, I decided to use a data structure and algorithm to optimize the pairing up of DNA sequences. See section 2 for more details.

Without any optimizations, the brute force approach would be O(k^2) * O(n choose 2) where n is the number of sequences and k is the length of each sequence. 

## Code Structure
- concat_sequences.py contains the main logic and helper functions
- concat_sequences_test.py contains tests for concat_sequences (some unit tests and some integration)
- sequence_lst.py contains the implementation of a data structure for holding unpaired DNA sequences. I made the interface generic so that it abstracts away the underlying implementation.
- sequence_lst_test.py contains tests for sequence_lst (some unit tests and some integration)

## Part 1 
This part of the problem can be described as finding the longest overlap between the suffix of one sequence and the prefix of another, and deciding these sequences should be paired together if the overlap is at least as long as half the length of the sequence.
The brute force approach is to have two pointers, starting with both pointing to the last character of string1 and string2. To illustrate: 

string1 CCTG

string2 TGAG

possible prefix = TGAG

Scan backwards on TGAG and string1 simultaneously (GTCC and GAGT respectively). They don't match, so decrement the pointer on string2 so it now points to the second to last character.

possible prefix = TGA

Scan backwards on TGA and string1 simultaneously (AGT and GTC respectively). They don't match, so decrement the pointer on string2 again.

possible prefix = TG

Scan backwards on TG and string1 simultaneously (GT and GT respectively). They match, so return the index on string1 where the overlap begins (2)

The function that implements this is get_substring_match.

#### Possible Optimizations

You could implement an algorithm that generates a finite state machine for each sequence (similar to what is used for regular expressions; see https://www.ics.uci.edu/~eppstein/161/960222.html), which then allows you to find the sequence in linear time, though the construction of the finite state machine is O(k^3) where k is the length of the sequence. Since you have to do this construction for every sequence, and the brute force approach is O(k^2) anyway which is still polynomial, I decided not to implement the finite state machine for now.

It would take O(k^3 * n) to construct finite state machines + O(n^2 * k) to match sequence pairs. This makes sense if k is smaller than n. If k=n then it's the same. I don't anticipate k growing much larger because biotechnology tends to use short sequences that can be sequenced in parallel.

## Part 2
As discussed in the overview, the bottleneck in running time is the combinatorial explosion from evaluating all pairs of sequences. Instead of evaluating all pairs, we could eliminate possible pairs as we pair off so it would be O(50 + 49 + 48 + ... + 1) which is (50)(50+1)/2 = O(n^2).

The function find_substring_pairs takes an unpaired sequence and finds the immediately preceding and immediately following sequences, if they exist. Since each sequence only has one unique preceding sequence and one unique following sequence (I confirmed this via email), once we find them we can eliminate the sequence from consideration in future pairings. 

In order to make the optimization work, I needed to be able to delete from the data structure holding the unpaired sequences in O(1) time. I decided to implement a doubly-linked list (sequence_list.py) since I didn't need to search the list (which would take linear time), only delete from it.

## Part 3

Gluing all the sequences together was relatively straightforward (see concat_sequences and concat_two_seqs) once you know which ones are paired and what index the overlap starts at. Basically I had a dictionary that maps the first sequence to the next sequence and so on, and I just traversed that dictionary and appended to a string, using the already computed indices for the overlap.

## Running Time
Other sections also discuss running time and tradeoffs, but in summary this solution that uses a data structure for unpaired DNA sequences would be O(n^2 * k^2) where n is the number of sequences and k is the length of each sequence.

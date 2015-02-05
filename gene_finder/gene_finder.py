# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Anisha Nakagawa

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    if nucleotide == 'A':
        return 'T'
    elif nucleotide == 'T':
        return 'A'
    elif nucleotide == 'C':
        return 'G'
    else:
        return 'C'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    comp_dna = ""
    for i in range(len(dna) - 1, -1, -1):
        next_base = get_complement(dna[i])
        comp_dna = comp_dna + next_base
    return comp_dna

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.

        stop codons: UAG, UAA, UGA
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("ATGAAACCCG")
    'ATGAAACCCG'
    >>> rest_of_ORF("ATGAAACCCGG")
    'ATGAAACCCGG'
    """
    # Loop through every 3 bases, and check the codon preceding that index
    for i in range(2, len(dna), 3):
        # Get next codon
        codon = dna[i - 2: i + 1]
        # Check if codon is a stop
        if codon == 'TAG' or codon == 'TAA' or codon == 'TGA':
            # Return the string up to the codon
            return dna[:i - 2]
    return dna
            

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    orfs = []
    i = 0
    while i < (len(dna) - 3):
        codon = dna[i: i + 3]
        # if start codon
        if codon == 'ATG':
            orf = rest_of_ORF(dna[i:])
            orfs.append(orf)
            i = i + len(orf) #skip to the end of the orf
        else:
            i = i + 3 #move to start of next codon
    return orfs

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    # Get lists of orfs
    first_frame_orfs = find_all_ORFs_oneframe(dna) #first reading frame
    second_frame_orfs = find_all_ORFs_oneframe(dna[1:]) #shifted over one
    third_frame_orfs = find_all_ORFs_oneframe(dna[2:]) #shifted over two

    orfs = first_frame_orfs + second_frame_orfs + third_frame_orfs
    return orfs

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    comp_dna = get_reverse_complement(dna)
    orfs = find_all_ORFs(dna) + find_all_ORFs(comp_dna)
    return orfs

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    all_orfs = find_all_ORFs_both_strands(dna)
    longest_orf = ""
    for orf in all_orfs:
        if len(orf) > len(longest_orf):
            longest_orf = orf
    return longest_orf

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    longest = 0
    for i in xrange(num_trials):
        shuffled = shuffle_string(dna)
        longest_shuffled = longest_ORF(shuffled) #longest ORF in shuffled
        if len(longest_shuffled) > longest:
            longest = len(longest_shuffled) #reset longest value
    return longest

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    protein = ""
    for i in xrange(0, len(dna) - 2, 3):
        codon = dna[i: i + 3]
        amino_acid = aa_table[codon]
        protein = protein + amino_acid
    return protein

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    # Find length threshold
    threshold = longest_ORF_noncoding(dna, 1500)

    # Find all open reading frames, both strands
    all_orfs = find_all_ORFs_both_strands(dna)

    # Get list of ORFs longer than threshold
    long_orfs = [i for i in all_orfs if len(i) > threshold]

    # return list of amino acids
    amino_acids = [coding_strand_to_AA(i) for i in long_orfs]
    return amino_acids
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()

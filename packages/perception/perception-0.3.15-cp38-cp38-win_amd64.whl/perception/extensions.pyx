# distutils: extra_compile_args=-fopenmp
# distutils: extra_link_args=-fopenmp
# cython: language_level=3

import math
import numpy as np
import cython
from cython.parallel import prange, parallel
from libc.stdlib cimport abort, malloc, free

cimport numpy as np
cdef extern from "limits.h":
    int INT_MAX

ctypedef np.uint8_t uint8

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_euclidean_pairwise_duplicates(int[:, :] X, float threshold, counts: int[:] = None, compute_overlap=False):
    """Find the pairwise overlap within an array of vectors, where there may be multiple
    vectors for the same file. This function is faster than using scipy.spatial.distance
    because it computes distances in parallel, avoids computing full distances when they're
    not necessary, skips computing distances for pairs of hashes that are for the
    same file, and skips computing distances for vectors if both have already been matched.
    
    Args:
        X: The vectors with shape (N, D). Vectors for the same file need to be
            supplied sequentially so that we can use the counts argument
            to determine which vectors are for the same file.
        counts: For each file, the number of sequential vectors in X. If not
            provided, each vector is assumed to be for a different file (i.e.,
            this is equivalent to `counts = np.ones(N)`).
        compute_overlap: If True, the values returned will be divided by the number
            of hashes in each file. If False, the raw duplicate counts will
            be returned.
    
    Returns:
        duplicates: An array of shape (M!/(2*((M-2)!)), 2) indicating
            the fraction of vectors for each file found in another file.
            The indexing matches that of scipy.spatial.pdist. M is the number of files.
            So if M = 4, the array will represent comparisons of the file indexes as follows:
            [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]. So (assuming compute_overlap=True),
            a possible return would be [(1.0, 1.0), (0, 0), (0, 0), (0.66, 1.0), (0.5, 0.25)]
            which means that:

            - There was 100% overlap between file 0 and file 1
            - 66% of file 1 was in file 2 and 100% of file 2 was in file 1
            - 50% of file 2 was in file 3 and 25% of file 3 was in file 2
    """
    if counts is None:
        counts_arr = np.ones(X.shape[0], dtype=np.int32)
        counts = counts_arr
    cdef Py_ssize_t n = X.shape[0]
    cdef Py_ssize_t m = counts.shape[0]
    cdef Py_ssize_t d = X.shape[1]
    cdef Py_ssize_t n_pairs = int(math.factorial(m)/(2*math.factorial(m-2)))
    cdef Py_ssize_t max_counts = np.max(counts)
    cdef int compute_overlap_int = 0
    if compute_overlap:
        compute_overlap_int = 1
    # i_1 is the index of file1, i_2 is the index of file2, i_d is the
    # index of the vector dimension we're on, i_i is used to compute
    # the starting index in the flattened vector in the different threads.
    # i_1_subhash is the index of the hash on file1, i_2_subhash is
    # the index of the hash on file2.
    cdef Py_ssize_t i_1, i_2, i_d, i_i, i_1_sub, i_2_sub, i_1_offset
    duplicate_arr = np.zeros((n_pairs, 2), dtype=np.double)
    cdef double[:, :] duplicate = duplicate_arr
    offsets_arr = np.zeros(m, dtype=np.int32)
    cdef np.int32_t[:] offsets = offsets_arr
    for i_1 in range(m):
        for i_i in range(i_1):
            offsets[i_1] += counts[i_i]
    cdef size_t local_buf_size = 4 # distance, flattened array offset, index_offset_1, index_offset_2
    cdef float threshold2 = threshold ** 2
    with nogil, parallel():
        local_buf = <int *> malloc(sizeof(int) * local_buf_size)

        # An array of flags indicating whether a vector in file 1 was
        # matched.
        matched_1 = <int *> malloc(sizeof(int) * max_counts)

        # An array of flags indicating whether a vector in file 2 was
        # matched.
        matched_2 = <int *> malloc(sizeof(int) * max_counts)
        if local_buf is NULL or matched_1 is NULL or matched_2 is NULL:
            abort()
        # Iterate over all of the files.
        for i_1 in prange(m-1):
            local_buf[1] = 0
            local_buf[2] = offsets[i_1]
            # Compute the index of the output vector
            # where we will count the number of duplicates.
            for i_i in range(i_1):
                local_buf[1] += m - i_i - 1
            # Iterate over all the other files to compare.
            for i_2 in range(i_1 + 1, m):
                local_buf[3] = offsets[i_2]
                # Initialize all match flags to zero for
                # both file 1 and file 2.
                for i_1_sub in range(counts[i_1]):
                    matched_1[i_1_sub] = 0
                for i_2_sub in range(counts[i_2]):
                    matched_2[i_2_sub] = 0
                # Iterate over all the hashes in file1
                for i_1_sub in range(counts[i_1]):
                    # Iterate over all the hashes in file2
                    for i_2_sub in range(counts[i_2]):
                        local_buf[0] = 0
                        if matched_1[i_1_sub] == 1 and matched_2[i_2_sub] == 1:
                            # Both the vectors in this pair have already been matched, so
                            # there is nothing to gain from this comparison.
                            continue
                        for i_d in range(d):
                            local_buf[0] += (X[local_buf[2] + i_1_sub, i_d] - X[local_buf[3] + i_2_sub, i_d]) ** 2
                            if local_buf[0] > threshold2:
                                # If we're already beyond the distance threshold,
                                # we don't need to continue computing squared
                                # distances.
                                break
                        if local_buf[0] < threshold2:
                            # A match was found. Set flags for both vectors
                            # to 1.
                            matched_1[i_1_sub] = 1
                            matched_2[i_2_sub] = 1
                # Add up the number of matches for file 1.
                for i_1_sub in range(counts[i_1]):
                    duplicate[local_buf[1], 0] += matched_1[i_1_sub]
                # Add up the number of matches for file 2.
                for i_2_sub in range(counts[i_2]):
                    duplicate[local_buf[1], 1] += matched_2[i_2_sub]
                # Divide by the total number of vectors for each file.
                if compute_overlap_int:
                    duplicate[local_buf[1], 0] /= counts[i_1]
                    duplicate[local_buf[1], 1] /= counts[i_2]
                # Advance to the next pair index.
                local_buf[1] += 1
        free(local_buf)
        free(matched_1)
        free(matched_2)
    return duplicate_arr

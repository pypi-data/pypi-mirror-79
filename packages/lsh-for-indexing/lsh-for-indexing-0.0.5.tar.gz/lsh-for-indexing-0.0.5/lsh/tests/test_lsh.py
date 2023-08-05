from random import randint
from lsh.random_projection import LshGaussianRandomProjection
from lsh.random_projection import LshSparseRandomProjection
from numpy.random import random
import pytest


@pytest.mark.parametrize("LSH", [LshGaussianRandomProjection,
                                 LshSparseRandomProjection])
def test_consistency(LSH):
    vector_dimension = randint(10, 300)
    bucket_size = randint(1, 30)
    num_of_buckets = randint(1, 30)
    seed = randint(1, 30)
    vec = random((1, vector_dimension))

    lsh = LSH(vector_dimension, bucket_size, num_of_buckets, seed)
    lsh.fit()
    a = lsh.indexable_transform(vec)

    lsh = LSH(vector_dimension, bucket_size, num_of_buckets, seed)
    lsh.fit()
    b = lsh.indexable_transform(vec)
    assert a == b


@pytest.mark.parametrize("LSH", [LshGaussianRandomProjection,
                                 LshSparseRandomProjection])
def test_lsh_basic(LSH):
    vector_dimension = randint(10, 300)
    bucket_size = randint(1, 5)
    num_of_buckets = randint(1, 30)
    seed = randint(1, 30)
    vec1 = random(vector_dimension)
    vec2 = random(vector_dimension)

    assert vec1.tolist() != vec2.tolist()

    lsh = LSH(vector_dimension, bucket_size, num_of_buckets, seed)
    lsh.fit()
    a = lsh.indexable_transform(vec1)
    b = lsh.indexable_transform(vec2)

    assert a != b

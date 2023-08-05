## LSH for indexing

This package helps search engines to index and easily search on vector using Local sensitivity hashing (LSH)

### Installation

    pip install -i https://test.pypi.org/simple/ lsh-for-indexing

### Usage example

    from lsh.random_projection import LshGaussianRandomProjection
    import numpy as np
    
    rp = LshGaussianRandomProjection(vector_dimension=6, bucket_size=3, num_of_buckets=2)    import numpy as np
    vec = np.asarray([1,0,1,1,0,0])
    rp.fit()
    rp.indexable_transform(vec)
    >> ['0_010', '1_000']

if you know your collection size and you want an optimal number of bucket_size

    rp.fit(sample_size=2000)

transforming a bulk of vectors

    mat = np.asarray([[1,0,1,1,0,0], [1,0,0,1,0,1]])
    rp.indexable_transform(mat)
    >> [['0_010', '1_111'], ['0_010', '1_101']]
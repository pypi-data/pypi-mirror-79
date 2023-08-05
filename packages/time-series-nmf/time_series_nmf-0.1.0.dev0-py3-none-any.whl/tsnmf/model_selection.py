# Functions for model selection

from scipy.cluster.hierarchy import linkage, cophenet


# from Nimfa package



def coph_cor(self, idx=None):
    """
    Compute cophenetic correlation coefficient of consensus matrix, generally obtained from multiple NMF runs. 
        
    The cophenetic correlation coefficient is measure which indicates the dispersion of the consensus matrix and is based 
    on the average of connectivity matrices. It measures the stability of the clusters obtained from NMF. 
    It is computed as the Pearson correlation of two distance matrices: the first is the distance between samples induced by the 
    consensus matrix; the second is the distance between samples induced by the linkage used in the reordering of the consensus 
    matrix [Brunet2004]_.
        
    Return real number. In a perfect consensus matrix, cophenetic correlation equals 1. When the entries in consensus matrix are
    scattered between 0 and 1, the cophenetic correlation is < 1. We observe how this coefficient changes as factorization rank 
    increases. We select the first rank, where the magnitude of the cophenetic correlation coefficient begins to fall [Brunet2004]_.
        
    :param idx: Used in the multiple NMF model. In factorizations following standard NMF model or nonsmooth NMF model
                    :param:`idx` is always None.
    :type idx: None or `str` with values 'coef' or 'coef1' (`int` value of 0 or 1, respectively) 
    """
    A = self.consensus(idx=idx)
    # upper diagonal elements of consensus
    avec = np.array([A[i, j] for i in range(A.shape[0] - 1)
                    for j in range(i + 1, A.shape[1])])
    # consensus entries are similarities, conversion to distances
    Y = 1 - avec
    Z = linkage(Y, method='average')
    # cophenetic correlation coefficient of a hierarchical clustering
    # defined by the linkage matrix Z and matrix Y from which Z was
    # generated
    return cophenet(Z, Y)[0]

from operator import eq
def elop(X, Y, op):
    #try:
    #    X[X == 0] = np.finfo(X.dtype).eps
    #    Y[Y == 0] = np.finfo(Y.dtype).eps
    #except ValueError:
    #    return op(np.mat(X), np.mat(Y))
    return(op(np.mat(X), np.mat(Y)))


def connectivity(model, X, H=None, idx=None):
    """
    Compute the connectivity matrix for the samples based on their mixture coefficients. 
        
    The connectivity matrix C is a symmetric matrix which shows the shared membership of the samples: entry C_ij is 1 iff sample i and 
    sample j belong to the same cluster, 0 otherwise. Sample assignment is determined by its largest metagene expression value. 
        
    Return connectivity matrix.
        
    :param idx: Used in the multiple NMF model. In factorizations following
        standard NMF model or nonsmooth NMF model ``idx`` is always None.
    :type idx: None or `str` with values 'coef' or 'coef1' (`int` value of 0 or 1, respectively) 
    """
    #X = model.X
    H = model.H
    idx = np.argmax(H, axis=0)
    mat1 = np.tile(idx, (X.shape[1], 1))
    mat2 = np.tile(np.reshape(idx.T,(len(idx),1)), (1, X.shape[1]))
    conn = elop(mat1, mat2, eq)
    #if sp.isspmatrix(conn):
    #    return conn.__class__(conn, dtype='d')
    #else:
    return np.mat(conn, dtype='d')

def coph_cor(X, model, n_runs = 1, parallel=False):
        """
        Compute cophenetic correlation coefficient of consensus matrix, generally obtained from multiple NMF runs. 
        
        The cophenetic correlation coefficient is measure which indicates the dispersion of the consensus matrix and is based 
        on the average of connectivity matrices. It measures the stability of the clusters obtained from NMF. 
        It is computed as the Pearson correlation of two distance matrices: the first is the distance between samples induced by the consensus matrix; the second is the distance between samples induced by the linkage used in the reordering of the consensus 
        matrix [Brunet2004]_.
        
        Return real number. In a perfect consensus matrix, cophenetic correlation equals 1. When the entries in consensus matrix are
        scattered between 0 and 1, the cophenetic correlation is < 1. We observe how this coefficient changes as factorization rank 
        increases. We select the first rank, where the magnitude of the cophenetic correlation coefficient begins to fall [Brunet2004]_.
        
        :param idx: Used in the multiple NMF model. In factorizations following standard NMF model or nonsmooth NMF model
                    :param:`idx` is always None.
        :type idx: None or `str` with values 'coef' or 'coef1' (`int` value of 0 or 1, respectively) 
        """
        A = consensus(n_runs, X, model, parallel = parallel)
        # upper diagonal elements of consensus
        avec = np.array([A[i, j] for i in range(A.shape[0] - 1)
                        for j in range(i + 1, A.shape[1])])
        # consensus entries are similarities, conversion to distances
        Y = 1 - avec
        Z = linkage(Y, method='average')
        # cophenetic correlation coefficient of a hierarchical clustering
        # defined by the linkage matrix Z and matrix Y from which Z was
        # generated
        return (cophenet(Z, Y)[0], cophenet(Z,Y)[1])
    
    def estimate_rank(ranks, X, model, n_runs=10, parallel=False):
    # run for different ranks
    c_dict = {}
    D_dict = {}
    for r in ranks:
        model.rank = r
        c, D = coph_cor(X=X, model=model, n_runs=n_runs, parallel=parallel)
        c_dict[r] = c
        D_dict[r] = D
    rank = max(c_dict.keys(), key=(lambda k: c_dict[k]))   
    return(rank, c_dict, D_dict)
    
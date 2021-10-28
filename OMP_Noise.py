import numpy as np
from numpy import linalg as LA
from scipy.sparse import rand
from scipy.spatial import distance
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


def omp(A, b, variance, *args):
    r = b
    cols = A.shape[1]
    rows = A.shape[0]
    if args == ():
        k = cols / 2
    else:
        k = args[0]
    A_reduced = np.empty((rows, 0))  # As Matrix
    X = np.zeros((cols, 1))
    s = []
    error_power = (LA.norm(r) ** 2) / rows
    while (error_power >= 1.15 * variance) and (k > 0):
        Arr = abs(np.matmul(A.T, r))
        next_col = np.where(Arr == np.amax(Arr))[0]
        s.append(next_col.tolist()[0])
        A_reduced = np.column_stack((A_reduced, A[:, next_col]))
        Xs = np.matmul((np.linalg.pinv(A_reduced)), b)
        X[s] = Xs
        b_hat = np.matmul(A, X)
        r = b - b_hat
        error_power = (LA.norm(r) ** 2) / rows
        k -= 1
    return X


if __name__ == '__main__':
    rows = 200
    cols = 500
    A = np.random.randn(rows, cols)
    for i in range(cols):
        A[:, i] = A[:, i] / LA.norm(A[:, i])

    k, abs_error = 3, []
    for counter in range(0, 50, 5):
        error = 0
        for idx in range(1000):
            X = rand(cols, 1,
                     density=k / cols).todense()
            b = np.matmul(A, X)
            SNR = counter
            variance = (LA.norm(b) ** 2 / rows) / (10 ** (SNR / 10))
            n = np.random.randn(rows, 1) * np.sqrt(variance)
            b_n = b + n
            X_hat = omp(A, b_n, variance, k)
            b_hat = np.matmul(A, X_hat)
            error += (LA.norm(b - b_hat) ** 2) / (1000 * rows)
        abs_error.append(error)
    plt.plot([idx for idx in range(0, 50, 5)], abs_error)
    plt.show()

import numpy as np
import scipy.sparse as sparse
import time

def ALS(ratingMat, userMatO, itemMatO, nonZeroItem, nonZeroUser, M, regular_v, regular_u):
    for i in xrange(0, ratingMat.shape[0]):
        Ii = nonZeroItem[2 * i + 1][0]
        if len(Ii) > 0:
            nui = len(Ii)
            Mi = itemMatO[Ii, :]
            Ri = ratingMat[i, Ii]
            Mi_T_Mi = np.dot(Mi.T, Mi)
            regu_eye = np.eye(M) * regular_u * nui
            userMatO[i, :] = np.squeeze(np.linalg.solve((Mi_T_Mi + regu_eye), np.dot(Ri, Mi)))

    for j in xrange(0, ratingMat.shape[1]):
        Ij = nonZeroUser[2 * j + 1][0]
        if len(Ij) > 0:
            nmj = len(Ij)
            Uj = userMatO[Ij, :]
            Rj = ratingMat[Ij, j]
            Uj_T_Uj = np.dot(Uj.T, Uj)
            regu_eye = np.eye(M) * regular_v * nmj
            itemMatO[j, :] = np.squeeze(np.linalg.solve((Uj_T_Uj + regu_eye), np.dot(Rj.T, Uj)))
    return userMatO, itemMatO

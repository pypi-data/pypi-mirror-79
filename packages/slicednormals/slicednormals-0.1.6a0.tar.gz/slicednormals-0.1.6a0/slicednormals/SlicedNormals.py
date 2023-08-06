import numpy as np
from itertools import combinations_with_replacement as cwr
from scipy.optimize import minimize as scimin
from scipy.stats import chi2 as chi2
from slicednormals import HyperEllipse as HE

class SNDist():
    "Ref: Improving the Uncertainty Quantifcation of Sliced Normal Distributions by Scaling the Covariance Matrix Colbert et al 2020"
    def __init__(self, Data, DoF):
        self.Data = Data
        self.DoF = DoF
        self.mu = None
        self.Sigma = None
    
    def SN_Phi(self, Data):
        # Unnormalised log-likelihood
        Z_Data = ZExpand(Data, self.DoF)
        return Phi(Z_Data, self.mu, self.Sigma)
    
class Basic_SN(SNDist):
    def __init__(self, Data, DoF):
        super().__init__(Data, DoF)
        self.Z_Data = ZExpand(self.Data, self.DoF)
        self.mu = np.mean(self.Z_Data,0)
        self.Sigma = Nearest_PSD(np.cov(self.Z_Data.T, ddof = 0))
    
class Scaled_SN(Basic_SN):
    def __init__(self, Data, DoF, No_Supp_Samples, Retain_Supp_Samples = False):
        super().__init__(Data, DoF)
        self.Hyper_Ellipse = HE.Hyper_Ellipse(Data = self.Data)
        self.Supp_Samples = self.Hyper_Ellipse.Sample(No_Supp_Samples)
        if Retain_Supp_Samples:
            self.Z_Supp_Samples = ZExpand(self.Supp_Samples, self.DoF)
            self.Z_Supp_Phi = -Phi(self.Z_Supp_Samples, self.mu, self.Sigma)
            self.Z_Supp_PhiSum = np.sum(np.exp(self.Z_Supp_Phi))
            self.Z_Data_PhiSum = np.sum(-Phi(self.Z_Data, self.mu, self.Sigma))
            objfun = lambda gamma: -((-np.shape(self.Data)[0] * np.log(np.sum(np.exp(self.Z_Supp_Phi * gamma)))) + gamma * self.Z_Data_PhiSum)
        else:
            Z_Supp_Samples = ZExpand(self.Supp_Samples, self.DoF)
            Z_Supp_Phi = -Phi(Z_Supp_Samples, self.mu, self.Sigma)
            Z_Data_PhiSum = np.sum(-Phi(self.Z_Data, self.mu, self.Sigma))
            objfun = lambda gamma: -((-np.shape(self.Data)[0] * np.log(np.sum(np.exp(Z_Supp_Phi * gamma)))) + gamma * Z_Data_PhiSum)
        self.gamma = scimin(objfun, 1e-9, bounds=((0, None),)).x
        self.Sigma = self.Sigma/self.gamma
        if Retain_Supp_Samples:
            self.Z_Supp_Phi = -Phi(self.Z_Supp_Samples, self.mu, self.Sigma)
            self.Z_Supp_PhiSum = np.sum(np.exp(self.Z_Supp_Phi))
            self.Z_Data_PhiSum = np.sum(-Phi(self.Z_Data, self.mu, self.Sigma))

def Phi(Data, mu, Sigma):
    # Unnormalised log-likelihood
    DMu = Data - mu
    return (np.sum(DMu.T*(np.linalg.solve(Sigma, DMu.T)),0)/2).T

def Nearest_PSD(Mat):
    try:
        np.linalg.cholesky(Mat)
        return Mat
    except np.linalg.LinAlgError:
        Symm = (Mat + Mat.T)/2
        [_, S, V] = np.linalg.svd(Symm)
        SymmPF = np.dot(V,np.dot(S,V.T))
        MatStar = (Mat + SymmPF)/2
        MatStar = (MatStar + MatStar.T)/2
        k = 0
        while True:
            try:
                np.linalg.cholesky(MatStar)
                break
            except np.linalg.LinAlgError:
                k += 1
                EMin = np.min(np.real(np.linalg.eig(MatStar)[0]))
                MatStar += (-EMin * k ** 2 + np.spacing(1)) * np.eye(np.shape(MatStar)[0])
        return MatStar

def ZExpand(P_Data, DoF = 1):
    Z_Data = P_Data
    Degree = 2
    while Degree <= DoF:
        if len(np.shape(P_Data)) > 1:
            Z_Data = np.hstack((Z_Data, np.vstack([[np.prod(a) for a in cwr(P_D, Degree)] for P_D in P_Data])))
        else:
            Z_Data = np.hstack((Z_Data, [np.prod(a) for a in cwr(P_Data, Degree)]))
        Degree += 1
    return Z_Data
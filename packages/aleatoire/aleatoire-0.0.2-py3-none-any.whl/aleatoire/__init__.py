from scipy.integrate import nquad
from scipy import optimize, special, stats, linalg
import numpy as np 
from aleatoire.moment import *
from aleatoire.transform import *
from aleatoire.form import *
from aleatoire.sensitivity import linearSensitivity
import aleatoire.numeric
import aleatoire.io

class rvSet(np.ndarray):
    def __new__(cls, rvars=None,data=None,Rxx=None,Sxx=None):
        if rvars is None: rvars = [None]
        if data is None: data = {'data':None}
        return np.asarray(rvars).view(cls)

    def __init__(self,rvars=None,data=None,Rxx=None,Sxx=None):
        if rvars is None:
            rvars = [None]
            self.__dict__ = data
            
        if data is None: 
            data = {'data':None}
            self.Rxx = Rxx
            self.Sxx = Sxx
            self.mean = np.array([x.mean() for x in rvars])
            self.std = np.array([x.std() for x in rvars])
        
        self.Dx = scipy.linalg.block_diag(*self.std)
        self.Dinv = np.linalg.inv(self.Dx)

        if hasattr(self,'Rxx') and not hasattr(self,'Sxx'):
            self.Sxx = self.Dx@(self.Rxx@self.Dx)
        if hasattr(self,'Sxx') and not hasattr(self,'Rxx'):
            self.Rxx = self.Dinv@self.Sxx@self.Dinv
        
        self.L = np.linalg.cholesky(self.Rxx)
        self.Linv = np.linalg.inv(self.L)
    
    def __len__(self):
        return len(self.mean)


    def x_to_u(self,X):
        Linv, Dinv = self.Linv, self.Dinv
        U = Linv@Dinv@(X - self.mean)
        return U
    
    def u_to_x(self,U):
        Dx, L = self.Dx,self.L
        X = self.mean + Dx@L@U
        return X

class rvFunction:
    def __init__(self,func_x, rvset=None,grad=None):
        
        self.func_x= func_x
        if grad is None and hasattr(func_x,'grad'):
            self.grad = func_x.grad
        else:
            self.grad = grad
        self.rvset = rvset
        
        if rvset is not None:
            X = rvset
            self.func_u = lambda u: func_x(X.u_to_x(u))
            self.func_u.grad = lambda u: self.grad(X.u_to_x(u)).T @ X.Jxu(u)


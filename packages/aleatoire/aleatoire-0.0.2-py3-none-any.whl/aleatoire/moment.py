import numpy as np
import scipy.linalg
from scipy.optimize import minimize
import scipy.optimize
# import jax

class smSet(np.ndarray):
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
        self._Jxu = self.Dx@self.L
    
    def __len__(self):
        return len(self.mean)

    def Jxu(self,u):
        return self._Jxu 
        
    def x_to_u(self,X):
        Linv, Dinv = self.Linv, self.Dinv
        U = Linv@Dinv@(X - self.mean)
        return U
    
    def u_to_x(self,U):
        Dx, L = self.Dx,self.L
        X = self.mean + Dx@L@U
        return X


class SecondMoment:
    """Collection of second order reliability methods"""
    def __init__(self, rvfunc):
        self.rvfunc = rvfunc
        self.func_x = rvfunc.func_x
        self.func_u = rvfunc.func_u
        
    def mcfosm(self):
        """Mean Centered First-Order Second Moment method (Ang and Cornell, 1974)"""
        g = self.rvfunc
        X = self.rvfunc.rvset
        
        mean = g.func_x(X.mean)
        var = g.grad(X.mean).T@X.Sxx@g.grad(X.mean)
        return mean/np.sqrt(var)
    
    def fosm(self):
        """First-Order, Second Moment method (Hasofer-Lind, 1974)"""
        G = self.func_u
        ndim = len(self.rvfunc.rvset)

        def f(u):
            return np.linalg.norm(u)
        
        con = scipy.optimize.NonlinearConstraint(G, 0, 0)
        
        sol = minimize(f,np.zeros(ndim),constraints=con)
        
        u = self.design_point_u = sol.x
        alpha = -G.grad(u)/np.linalg.norm(G.grad(u))
        self.alpha = alpha
        self.design_point_x = self.rvfunc.rvset.u_to_x(u)
        return alpha@u
    
    def gsm(self,X):
        """Generalized Second-Moment method (Ditlevsen 1979)"""
        pass
from scipy.integrate import nquad
from scipy.optimize import fsolve
from scipy import optimize, special, stats, linalg
import numpy as np

nataf_correlation = {
    'lognorm':{
        'lognorm': lambda rho,deli,delj: np.log(1+rho*deli*delj)/rho/np.sqrt(np.log(1+deli**2)*np.log(1+delj**2)),
        'gamma': lambda rho, delj, deli: 1.001 + 0.033*rho + 0.004*deli - 0.016*delj + 0.002*rho**2 + 0.223*deli**2 + 0.130*delj**2 + 0.029*delj*deli - 0.104*rho*deli - 0.119*rho*delj,
    },
    'gamma':{
        'lognorm': lambda rho,deli,delj: 1.001 + 0.033*rho + 0.004*deli - 0.016*delj + 0.002*rho**2 + 0.223*deli**2 + 0.130*delj**2 + 0.029*delj*deli - 0.104*rho*deli - 0.119*rho*delj,
        'gamma':   lambda rho,deli,delj: 1.002 + 0.022*rho - 0.012*(deli+delj)+0.001*rho**2 + 0.125*(deli**2 + delj**2)+0.014*deli*delj-0.077*rho*(deli+delj),
    },
    'gumbel':{
        'gamma': lambda rho,deli,delj: 1.031 + 0.052*rho + 0.011*deli-0.210*delj + 0.002*rho**2 + 0.220*deli**2 + 0.350*delj**2 + 0.009*deli*delj+0.005*rho*deli-0.174*rho*delj
    }
}

class mnSet(np.ndarray):
    """Multinormally distributed random variables"""
    def __new__(cls, rvars=None,data=None,Rxx=None,Sxx=None):
        if rvars is None: rvars = [None]
        if data is None: data = {'data':None}
        return np.asarray(rvars).view(cls)

    def __init__(self,rvars=None,data=None,Rxx=None,Sxx=None):
        if rvars is None:
            rvars = [None]*len(data['mean'])
            self.rvset = rvars
            self.__dict__ = data
            
        if data is None: 
            data = {'data':None}
            self.Rxx = Rxx
            self.Sxx = Sxx
            self.mean = np.array([x.mean() for x in rvars])
            self.std = np.array([x.std() for x in rvars])
            self.rvset = rvars 

        print('Rxx: ', self.Rxx)
        self.Dx = linalg.block_diag(*self.std)
        self.Dinv = np.linalg.inv(self.Dx)

        if hasattr(self,'Rxx') and not hasattr(self,'Sxx'):
            self.Sxx = self.Dx@(self.Rxx@self.Dx)
        if hasattr(self,'Sxx') and not hasattr(self,'Rxx'):
            self.Rxx = self.Dinv@self.Sxx@self.Dinv
        
        self.L = np.linalg.cholesky(self.Rxx)
        self.Linv = np.linalg.inv(self.L)
        self._Jxu = self.Dx@self.L

    def Jxu(self,u):
        return self._Jxu
    
    def Jux(self,x):
        return np.linalg.inv(self.Jxu)

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

class siSet(np.ndarray):
    """Statistically independent random variables"""
    def __new__(cls, rvset):
        return np.asarray(rvset).view(cls)

    def __init__(self, rvset):
        self.rvset = rvset
        n_dist = len(rvset)
        self.ndist = n_dist

        #  check if all distributions have finite moments
        for x in self.rvset:
            if (not((np.isfinite(x.mean()) and
                     np.isfinite(x.std())))):
                raise RuntimeError("The marginal distributions need to have "
                                   "finite mean and variance")


    def u_to_x(self,u):
        return np.array([X.ppf(stats.norm.cdf(u[i])) for i,X in enumerate(self.rvset)])
    
    def x_to_u(self,x):
        return np.array([stats.norm.ppf(X.cdf(x[i])) for i,X in enumerate(self.rvset)])
    
    def Jxu(self,u):
        X = self.rvset
        snorm = stats.norm.pdf
        d = np.identity(self.ndist)
        x = self.u_to_x(u)
        # return np.array ([[X[i].pdf(x[i])/snorm(u[i])*d[i,j] for i in range(self.ndist)] for j in range(self.ndist)])
        return np.array ([[snorm(u[i])/X[i].pdf(x[i])*(i==j) for i in range(self.ndist)] for j in range(self.ndist)])
    
    def Jux(self,x):
        u = self.x_to_u(x)
        Jux = np.linalg.inv(self.Jxu(u))
        return Jux

    # def Jux(self,x):
    #     z = self.x_to_z(x)
    #     u = self.x_to_u(x)
    #     snorm = stats.norm.pdf
    #     J = np.array ([[1/snorm(u[i])*(i==j)*X[i].pdf(x[i]) for i in range(self.ndist)] for j in range(self.ndist)])
    #     return self.invL0@J

    # def Jxu(self,u):
    #     return np.linalg.inv(self.Jux(self.u_to_x(u)))

    def jpdf(self,x,y):
        return 
    
class biMorgen(np.ndarray):
    """Morgenstern multivariate distribution"""
    def __new__(cls, rvset):
        return np.asarray(rvset).view(cls)
    
    def __init__(self, rvset):
        n = len(rvset)
        self.rvset = rvset
        self.correlations = rvset.Rxx
        self._alpha = np.array([[None for i in range(n)] for j in range(n)])
    

    def Qi(self,i):
        X = self.rvset[i]
        interval = X.interval(1)
        def f(x):
            return (x-X.mean())/X.std()*X.pdf(x)*X.cdf(x)
        return nquad(f,[interval])[0]
        
    def alpha(self,ij):
        Qi = self.Qi(ij[0])
        Qj = self.Qi(ij[1])
        return self.correlations[ij[0],ij[1]]/(4*Qi*Qj)
    
    def F2_1(self, x):
        X = self.rvset
        return X[1].cdf(x[1])*(1 + (1 - 2*X[0].cdf(x[0]))*(1 - X[1].cdf(x[1])))

    def f2_1 (self, x):
        X = self.rvset 
        return X[1].pdf(x[1])*(1 + (1 - 2*X[0].cdf(x[0]))*(1 - 2*X[1].cdf(x[1])))

    def u_to_x(self, u):
        X = self.rvset 
        x1 =  X[0].ppf(stats.norm.cdf(u[0]))

        def f(x2):
            return self.F2_1([x1,x2])-stats.norm.cdf(u[1], 0., 1.)

        x2 = fsolve(f,1.)[0]
        return np.array([x1,x2])

    def x_to_u(self,x):
        X = self.rvset 
        u1 = stats.norm.ppf(X[0].cdf(x[0]))
        u2 = stats.norm.ppf(self.F2_1(x), 0., 1.)
        return np.array([u1,u2])

    def Jux(self,x):
        u = self.x_to_u(x)
        X = self.rvset
        Jux = np.zeros((2,2))

        Jux[0,0] = X[0].pdf(x[0])/stats.norm.pdf(u[0])
        Jux[0,1] = 0.0
        Jux[1,0] = -2*X[0].pdf(x[0])*X[1].cdf(x[1])*(1 - X[1].cdf(x[1]))/stats.norm.pdf(u[1])
        Jux[1,1] = self.f2_1(x)/stats.norm.pdf(u[1])
        return Jux

    def Jxu(self,u):
        x = self.u_to_x(u)
        return np.linalg.inv(self.Jux(x))

 #   def jpdf(self,x):
 #       if len(x)>2:
 #           return 'Error: joint pdf only currrently supports 2 random variables'
       
 #       alpha12 = self.alpha([0,1])
 #       X = self.rvset
 #       # def A(x):
 #       #     return np.prod([rv.pdf(x[i]) for i,rv in enumerate(self.rvset)])
 #       # def B(x):
 #       #     X = self.rvset
 #       #     return 1 + sum(self.alpha([i,j])*(1-X[i].cdf(x[i]))*(1-X[j].cdf(x[j])) for )
 #       return X[0].pdf(x[0]) * X[1].pdf(x[1])*(1+alpha12*(1-2*X[0].cdf(x[0]))*(1-2*X[1].cdf(x[1])))

    def jpdf(self,x,y):
        alpha12 = self.alpha([0,1])
        X = self.rvset
        return X[0].pdf(x) * X[1].pdf(y)*(1 + alpha12*(1-2*X[0].cdf(x))*(1-2*X[1].cdf(y)))

class nataf(np.ndarray):
    """Nataf transformation (Liu and Der Kiureghian 1986)"""
    def __new__(cls, rvset, Rxx, C,names=None):
        return np.asarray(rvset).view(cls)

    def __init__(self, rvset, Rxx, C,names=None):
        self.rvset = rvset
        self.Rxx = Rxx
        self.C = C
        n_dist = len(rvset)
        self.ndist = n_dist

        self.Rzz = np.identity(n=n_dist)
        if self.ndist == 2:
            rho = self.Rxx[0,1]
            deli = self.rvset[0].std()/self.rvset[0].mean()
            delj = self.rvset[1].std()/self.rvset[1].mean()
            self.Rzz[0,1] = self.Rzz[1,0] = rho*self.C(deli,delj,rho)
        else:
            for i in range(self.ndist):
                for j in range(i+1,self.ndist):
                    # print(i,j)
                    if C[i,j] is not None:
                        rho = self.Rxx[i,j]
                        deli = self.rvset[i].std()/self.rvset[i].mean()
                        delj = self.rvset[j].std()/self.rvset[j].mean()
                        self.Rzz[i,j] = self.Rzz[j,i] = rho*self.C[i,j](deli,delj,rho)

        self.L0 = np.linalg.cholesky(self.Rzz)
        self.invL0 = np.linalg.inv(self.L0)

    def check_moments(self):
        dists = np.array(['X'+str(1+i) for i in range(self.ndist)])
        means = np.around([X.mean() for X in self.rvset],3)
        stdvs = np.around([X.std() for X in self.rvset],3)
        print('vars:',dists)
        print('mean:',means)
        print('stdv:',stdvs)

        print('L0 : \n',np.around(self.L0,3))
        print('Rzz: \n',np.around(self.Rzz,3))
        print('Jxu: \n',np.around(self.Jxu(np.zeros(self.ndist)),0))
        return

    def x_to_u(self,x):
        return self.z_to_u(self.x_to_z(x))

    def u_to_x(self,u):
        z = self.u_to_z(u)
        return self.z_to_x(z)

    def x_to_z(self,x):
        return np.array([stats.norm.ppf(X.cdf(x[i])) for i,X in enumerate(self.rvset)])
    
    def z_to_x(self,z):
        x = np.array([X.ppf(stats.norm.cdf(z[i])) for i,X in enumerate(self.rvset)])
        return x
    
    def z_to_u(self,z):
        return self.invL0@z

    def u_to_z(self,u):
        z = self.L0@u
        return z

    def Jxu(self,u):
        z = self.u_to_z(u)
        x = self.u_to_x(u)
        X = self.rvset
        snorm = stats.norm.pdf
        d = np.identity(self.ndist)
        J = np.array ([[snorm(z[i])*d[i,j]/X[i].pdf(x[i]) for i in range(self.ndist)] for j in range(self.ndist)])
        return J@self.L0
    
    def Jux(self,x):
        return np.linalg.inv(self.Jxu(self.x_to_u(x)))

    def jpdf(self,x,y):
        X = self.rvset
        zx,zy = self.x_to_z([x,y])
        
        pos = np.empty(zx.shape + (2,))
        pos[:, :, 0] = zx
        pos[:, :, 1] = zy
        
        mvn = stats.multivariate_normal.pdf(pos, np.zeros(2),cov=self.Rzz)
        return mvn*(X[0].pdf(x)/stats.norm.pdf(zx)) * X[1].pdf(y)/stats.norm.pdf(zy)
    
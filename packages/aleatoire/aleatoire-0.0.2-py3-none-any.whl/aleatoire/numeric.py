import numpy as np 
from scipy.integrate import solve_ivp
try: import jax
except: pass

def _armijo_haukaas_init(b0: float=0.2, b: float = 0.5, m: int =4, a: float=0.5):
    
    def _armijo_haukaas():
        pass 
    try: 
        _armijo_haukaas = jax.jit(_armijo_haukaas)
        print('Jit Successful')
    except: pass
    return _armijo_haukaas

def _merit_init():
    pass

class iHLRF:
    def __init__(self, f, gradf, u0, loss=None, 
                    tol1=1.0e-4, tol2=1.0e-4, maxiter=20, maxiter_step=10,
                    step_opt={'c':10.},**kwargs):
        self.u0 = u0
        self.f = f 
        self.gradf = gradf
        self.tol1 = tol1
        self.tol2 = tol2
        self.maxiter = maxiter
        self.maxiter_step = maxiter_step
        self.loss = loss
        self.c = step_opt['c']
        if loss is None: 
            self.loss = np.linalg.norm

        # self.init()

    def init(self,verbose=False):
        if verbose:
            print('\niHL-RF Algorithm (Zhang and Der Kiureghian 1995)***************',
                  '\nInitialize iHL-RF: \n',
                  'u0: ', np.around(self.u0.T,4), '\n')

        self.G0 = self.f(self.u0) # scale parameter
        if verbose: print('G0: ',np.around(self.G0,4),'\n')

        self.ui = self.u0[None,:].T

        self.Gi = self.G0
        if verbose: print('Gi: ', np.around(self.Gi,4), '\n',)

        self.GradGi = self.gradf(self.ui[:,0].T)
        # if verbose: print('GradGi: ', np.around(self.GradGi,4), '\n',)
        if verbose: print('GradGi: ', self.GradGi, '\n',)

        self.alphai = -(self.GradGi / np.linalg.norm(self.GradGi))[None,:]
        self.count = 0
        self.res1 = abs(self.Gi/self.G0)
        self.res2 = self.loss(self.ui - (self.alphai@self.ui)*self.alphai.T )

        if verbose:
            print(
                # '\niHL-RF Algorithm (Zhang and Der Kiureghian 1995)***************',
                #   '\nInitialize iHL-RF: \n',
                #   'u0: ', np.around(self.u0.T,4), '\n',
                #   'G0: ',np.around(self.G0,4),'\n'
                #   'ui: ', np.around(self.ui.T,4), '\n',
                #   'Gi: ', np.around(self.Gi,4), '\n',
                #   'GradGi: ', np.around(self.GradGi,4),'\n',
                  'alphai: ', np.around(self.alphai,4),'\n',
                  'res1: ' , np.around(self.res1,4),'\n',
                #   'res2: ' , np.around(self.res2,4),'\n',
                  'res2: ' , self.res2,'\n',)
    def merit():
        pass

    def incr(self,method='adk', verbose=False):
        if method == 'basic':
            self.ui1 = self.ui + self.lamda * self.di
            return self.ui1 
        # c = 10.0
        self.ci = self.loss(self.ui) / np.linalg.norm(self.GradGi) + self.c
        self.mi = 0.5*self.loss(self.ui)**2 + self.ci*abs(self.Gi)
        self.mi1 = 0.5*self.loss(self.ui1)**2 + self.ci*abs(self.Gi1)

        self.count_step = 0
        while (self.mi1 >= self.mi) :
            self.lamda = self.lamda/2
            if verbose: print('lamda:', self.lamda)
            self.ui1 = self.ui + self.lamda * self.di
            if verbose: print('ui1: ',self.ui1)
            self.Gi1 = self.f(self.ui1[:,0].T)
            self.mi1 = 0.5*np.linalg.norm(self.ui1)**2 + self.ci*abs(self.Gi1)
            self.count_step += 1
            if (self.count_step >= self.maxiter_step): break
        return self.ui1

    
    
    def dirn(self):
        self.di = (self.Gi/np.linalg.norm(self.GradGi) + self.alphai@self.ui)*self.alphai.T - self.ui
        return self.di

    def step(self,verbose=False,basic=False):
        # self.di = (self.Gi/np.linalg.norm(self.GradGi) + self.alphai@self.ui)*self.alphai.T - self.ui
        di = self.dirn()
        if verbose: print('di: ',self.di)

        self.lamda = 1.0
        # self.lamda = 0.05

        self.ui1 = self.ui + self.lamda * di
        if verbose: print('ui1: ',self.ui1,self.ui1[:,0].T)

        self.Gi1 = self.f(self.ui1[:,0].T)

        self.incr(basic)

        self.ui = self.ui1  
        self.Gi = self.f(self.ui[:,0].T)
        self.GradGi = self.gradf(self.ui[:,0].T)
        self.alphai = -(self.GradGi / np.linalg.norm(self.GradGi))[None,:]

        self.res1 = abs(self.Gi/self.G0)
        self.res2 = self.loss(self.ui - (self.alphai@self.ui)*self.alphai.T)
        self.count += 1


        if verbose: print('\niHL-RF step: {}'.format(self.count))

        if verbose:
            print('ui: ',       np.around(self.ui,4), '\n',
                  'Gi: ',       np.around(self.Gi,4), '\n',
                  'GradGi: ', np.around(self.GradGi,4),'\n',
                  'alphai: ', np.around(self.alphai,4),'\n',
                  'res1: ' , np.around(self.res1,4),'\n',
                  'res2: ' , np.around(self.res2,4),'\n',)
        return self.ui
    
    def run(self,verbose=False, steps=None):
        self.init(verbose=verbose)
        if steps is not None: self.maxiter = steps
        while not(self.res1 < self.tol1 and self.res2 < self.tol2):
            self.step(verbose=verbose)

            if (self.count > self.maxiter): break

        return self.ui


import scipy.stats 
import numpy as np
from alea.form import FORM
import scipy.special
from scipy.optimize import minimize
from functools import partial
import itertools
from ema.utilities.numerical import iHLRF


class Probability(float):
    def __new__(cls, value, method):
       return float.__new__(cls, value)

    def __init__(self, value, method):
       self.method = method

class Event:
    def __init__(self,tag,p=None,X=None,limit_func=None,limit_grad=None):
        self.tag = tag
        self.p = p
        self.X = X
        self.limit_func = limit_func
        self.limit_grad = limit_grad

    def Pr(self,X=None):
        if X is None: X = self.X
        if self.p is None:
            return FORM(X,self.limit_func,self.limit_grad).run().pf
        else:
            return self.p

class ParallelSI(list):
    def __new__(cls, value, set_type=None):
       return super().__new__(cls, value)

    def __init__(self, value, set_type=None):
        super().__init__(value)
        self.set_type = set_type

    def Pr(self,X=None):
        return np.prod([event.Pr(X) for event in self])


class SeriesSI(list):
    def __new__(cls, value, set_type=None):
       return super().__new__(cls, value)

    def __init__(self, value, set_type=None):
        super().__init__(value)
        self.set_type = set_type

    
    def Pr(self,p):
        if p is None:
            Events = self
            n = len(Events)
            indices = list(range(n))
            combos = [list(itertools.combinations(indices,r)) for r in range(1,n+1)]
            return sum(
                (-1)**(i) * sum(
                    np.prod([Events[j].Pr() for j in ci]) for ci in si
                ) for i,si in enumerate(combos)
            )
        

class System:
    def __init__(self,X=None, limit_funcs=None, grads=None,Events=None):
        if Events is not None:
            nfunc = len(Events)
            self.X = []
            [self.X.append(event.X) for event in Events]
            self.limit_funcs = [event.limit_func for event in Events]
            self.nfunc = nfunc
            self.grads = [event.limit_grad for event in Events]
        else:
            nfunc = len(limit_funcs)
            self.X = X
            self.limit_funcs = limit_funcs 
            self.nfunc = nfunc
            self.grads = grads 
        
        ndist = len(self.X)
        # FORM Variables
        self.event_form_results = np.empty((nfunc),dtype=object)
        self.B = np.empty((nfunc),dtype=float)
        self.R = np.empty((nfunc,nfunc),dtype=float)
        self.A = np.empty((nfunc,ndist),dtype=float)
        self.Pr_form = None

        self._Pr = None

    
    def func_ui(self,i):
        grad = self.grads[i]
        return lambda u: grad(self.X.u_to_x(u)).T @ self.X.Jxu(u)

    def grad_ui(self,i):
        grad = self.grads[i]
        return lambda u: grad(self.X.u_to_x(u)).T @ self.X.Jxu(u)

    ## Importance Measures
    def MI(self,component_index):
        """Marginal importance"""
        return self.BP(component_index)

    def BP(self,component_index):
        return 

    def RAW(self,component_index):
        pass
    
    def Pr(self,method=None):
        if self._Pr is not None: return self._Pr
        
        if method is None: method = 'form'

        if method == 'form':
            return self.Pr_form
            

    def Pfe(self, num_si_events, p1=None):
        """Probability of failure over lifetime for `num_si_events` statistically 
        independent expected events over the lifetime of the structure.
        """
        if p1 is None: p1 = self.Pr()
        ne = num_si_events
        return sum(-(-n/n)**n * p1**n * scipy.special.comb(ne,n) for n in range(1,ne+1))
    
    def event_form(self,verbose=False, sensitivity=False):
        rvset = self.X
        self.event_form_results = [
            FORM(rvset, func_x, grad_x, sensitivity=False).run()
        for func_x,grad_x in zip(self.limit_funcs,self.grads)]
    
    def print_event_form(self):
        for x,_ in enumerate(self.limit_funcs):
            self.event_form_results[x].print_analysis()
    

    def parallel_form(self,verbose=False,linearize=True,method='scipy',options=None,name=None):
        """Hohenbichler et al. (1987)"""
        self.event_form()
        nev = len(self.limit_funcs) # number of events
        G = [self.func_ui(i) for i in range(nev)]
        X = self.X
        nrv = len(X)

        # Define gradients
        grad_u = [self.grad_ui(i)  for i in range(nev)]
        
        # Define loss function
        def f(u): return scipy.linalg.norm(u)

        # Define constraints
        # con = [scipy.optimize.NonlinearConstraint(g, 0., 0.) for g in G]
        if linearize:
            def const_funcs(i):
                e = self.event_form_results[i]
                return lambda u: e.beta - e.alpha@u
        else: 
            const_funcs = self.func_ui


        con = [{'type':'ineq', 'fun': const_funcs(i), # The function defining the constraint.# 'jac' : , # The Jacobian of fun (only for SLSQP).
                } for i in range(nev)]
        
        if method == 'ihlrf':
            pass
        else:
            sol = minimize( f, np.zeros(nrv), constraints=con)
            self.sol = sol
            u = self.design_point_u = sol.x


        self.design_point_x = X.u_to_x(u)
        A = np.array([-grad_ui(u)/scipy.linalg.norm(grad_ui(u)) for grad_ui in grad_u])
        self.A = A
        self.R = self.A@self.A.T
        self.B = A@u
        
        self.Pr_form = scipy.stats.multivariate_normal.cdf(-self.B, cov=self.R, allow_singular=True)
        
        if verbose:
            if name is not None: print(name,'*'*(40-len(name)))
            print('x*: ',np.around(self.design_point_x,3))
            print('u*: ',np.around(self.design_point_u,3))
            print('B:  ',np.around(self.B,3))
            print('A: \n',np.around(self.A,4))
            print('R: \n',np.around(self.R,3))
            print('Pf1: ',np.around(self.Pr_form,4))
            print('\n\n')
        return self

    def series_form(self,verbose=False,name=None):
        """Hohenbichler et al. (1987)"""
        X = self.X

        for i,func in enumerate(self.limit_funcs): 
            self.event_form_results[i] = FORM(X,func,self.grads[i]).run()
            self.B[i] = self.event_form_results[i].beta
            self.A[i,:] = self.event_form_results[i].alpha
            self.design_point_u = self.event_form_results[i].design_point_u
            self.design_point_x = self.event_form_results[i].design_point_x
            self.R = self.A@self.A.T
            self.Pr_form = 1-scipy.stats.multivariate_normal(cov=self.R,allow_singular=True).cdf(self.B)
        
        if verbose:
            if name is not None: print(name,'*'*(40-len(name)))
            print('x*:  ',np.around(self.design_point_x,3))
            print('u*:  ',np.around(self.design_point_u,3))
            print('B:   ',np.around(self.B,3))
            print('A: \n',np.around(self.A,4))
            print('R: \n',np.around(self.R,3))
            print('Pf1: ',np.around(self.Pr_form,4))
            # print('\n')
        return self


class SeriesSys(System):
    def form(self,verbose=False):
        """Hohenbichler et al. (1987)"""
        X = self.X
        for i,func in enumerate(self.limit_funcs): 
            self.event_form_results[i] = FORM(X,func,self.grads[i]).run()
            self.B[i] = self.event_form_results[i].beta
            self.A[i,:] = self.event_form_results[i].alpha
            self.R = self.A@self.A.T
            self.Pr_form = 1-scipy.stats.multivariate_normal(cov=self.R).cdf(self.B)
        if verbose:
            print('B: \n',self.B)
            print('A: \n',self.A)
            print('R: \n',self.R)
            print('Pf1: \n',self.Pr_form)
        return self

class ParallelSys(System):

    pass

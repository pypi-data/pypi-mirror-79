import numpy as np
import scipy.linalg
import scipy.stats
from scipy.optimize import minimize
import scipy.optimize
#from ema.utilities.numerical import iHLRF
from .numeric import iHLRF

class FORM:
    """First order reliability analysis"""
    def __init__(self, rvset, func_x, grad_x, sensitivity=False):
        self._hasrun = False
        self.rvset = rvset
        self.func_x = func_x
        self.grad_x = grad_x
        X = rvset
        self.func_u = lambda u: func_x(X.u_to_x(u))
        self.grad_u = lambda u: grad_x(X.u_to_x(u)).T @ X.Jxu(u)
        self.sensitivity = sensitivity

    
    def run(self, optimizer='scipy',loss=None, gradf=None, verbose=False,options={}):
        
        if loss is None: 
            loss=np.linalg.norm
        else: 
            pass
        f = loss
        
        G = self.func_u
        grad_u = self.grad_u
        ndim = len(self.rvset.rvset)
        u0 = np.zeros(ndim)
        
        if callable(optimizer):
            state = optimizer(f, None, G, grad_u, u0, verbose=verbose,**options)
            u = self.design_point_u = state['ui'][0][:,0].T

        elif optimizer=='ihlrf':
            u = self.design_point_u = iHLRF(G,grad_u,u0,**options).run(verbose=verbose)[:,0].T
        else:
            if options == {}:
                options = {'maxiter':40,'tol':1e-3,'constr': {'tol':1e-3}}
            options['disp']=verbose
            ctol=options['constr']['tol']
            # con = scipy.optimize.NonlinearConstraint(G, -1/2*ctol, 1/2*ctol, jac=grad_u)
            con = scipy.optimize.NonlinearConstraint(G, 0., 0.)
            # sol = minimize(f,u0,jac=gradf, constraints=con,options=options)
            sol = minimize(f,u0, constraints=con, options=options)
            self.sol = sol
            if verbose: print(sol)
            u = self.design_point_u = sol.x

        alpha = -grad_u(u)/scipy.linalg.norm(grad_u(u))
        self.alpha = alpha
        self.design_point_x = self.rvset.u_to_x(u)
        self.beta = alpha@u
        self.pf = scipy.stats.norm.cdf(-self.beta)

        # Sensitivities
        if self.sensitivity:
            rvset=self.rvset
            n = len(rvset)
            Jxu = rvset.Jxu
            self.alpha = self.alpha
            u = self.design_point_u 
            x = self.design_point_x
            self.Mxl = x - Jxu(u)@u
            self.Sxlxl = Jxu(u)@Jxu(u).T
            # self.Dxl = np.array([[np.sqrt(self.Sxlxl[0,0]),0],[0.0, np.sqrt(self.Sxlxl[1,1])]])
            self.Dxl = np.array([[np.sqrt(self.Sxlxl[i,j])*(j==i) for i in range(n)] for j in range(n)])
            self.gamma = self.alpha@rvset.Jux(x)@self.Dxl/np.linalg.norm(self.alpha@rvset.Jux(x)@self.Dxl)
        
        self._hasrun = True
        return self

    def print_analysis(self,form=True,sensitivity=False):
        if not self._hasrun: self.run()

        if form:
            print('\n')
            print('FORM Results:')
            print('u*:    {}'.format(np.around(self.design_point_u,3)))
            print('x*:    {}'.format(np.around(self.design_point_x,3)))
            print('alpha: {}'.format(np.around(self.alpha,4)))
            print('beta:  {}'.format(np.around(self.beta,4)))
            print('pf1:   {}'.format(np.around(self.pf,6)))

        if sensitivity:
            if self.gamma is None: self.run(sensitivity=True)
            print('\n')
            print('Sensitivity:')
            print('alpha: {}'.format(np.around(self.alpha,4)))
            print('gamma: {}'.format(np.around(self.gamma,4)))
    

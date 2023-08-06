import numpy as np 
import scipy.stats 
from aleatoire.form import FORM 


class linearSensitivity:
    def __init__(self,rvset, func_x, grad_x):
        Jxu = rvset.Jxu
        form = FORM(rvset, func_x, grad_x)
        form.run()
        self.alpha = form.alpha
        u = form.design_point_u 
        x = form.design_point_x
        self.Mxl = x - Jxu(u)@u
        self.Sxlxl = Jxu(u)@Jxu(u).T
        self.Dxl = np.array([[np.sqrt(self.Sxlxl[0,0]),0],[0.0, np.sqrt(self.Sxlxl[1,1])]])
        # self.Dxl = np.array([self.Sxlxl[0,0], self.Sxlxl[1,1]])
        self.gamma = self.alpha@rvset.Jux(x)@self.Dxl/np.linalg.norm(self.alpha@rvset.Jux(x)@self.Dxl)


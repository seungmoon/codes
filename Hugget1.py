# -*- coding: utf-8 -*-
"""
Hugget Model


"""

import sys 
sys.path.insert(0,'../')

import numpy as np
from scipy.interpolate import RegularGridInterpolator, interp1d
from scipy import sparse as sp
import time
import matplotlib.pyplot as plt

class HuggetModel:
   ''' 
   A class for a simpel Hugget model with an idiosyncratic income shock 
   and one asset to save
   '''

   def __init__(self, BoroLmt, CRRA, DiscFac, Wage,
                 NumGridAsset, NumGridIncome,
                 tolerance, rMax, rMin,
                 aMax, aMin, GridIncome, MarkovMat):
       
       '''
       Make a new instance of a simple Hugget model
       
       Parameters
       ----------
       BoroLmt : float
           Borrowing limit
       CRRA : float
           Coefficient of relative risk aversion.
       DiscFac : float
           Intertemporal discount factor for future utility.        
       Wage : float
           Wage coefficient on the income shock
       NumGridAsset : float
           Number of points on the asset grid
       NumGridIncome : float
           Number of points on the income grid
       tolerance: float
           Numerical precision 
       rMax: float
           Maximum interest rate under consideration 
       rMin: float
           Minimum interest rate under iteration
       aMax: float
           Maximum level of asset  
       aMin: float
           Minimum interest rate under iteration
       GridIncome: np.array
           Grid for income shock
       MarkovMat: np.array
           Markov matrix for the idiosyncratic income shock
           
       Returns
       -------
       None
        '''
       
       self.BoroLmt = BoroLmt
       self.CRRA = CRRA 
       self.DiscFac =DiscFac
       self.Wage = Wage
       self.NumGridAsset = NumGridAsset
       self.NumGridIncome = NumGridIncome
       self.tolerance = tolerance
       self.rMax = rMax
       self.rMin = rMin
       self.aMax = aMax
       self.aMin = aMin
       self.GridIncome = GridIncome
       self.MarkovMat = MarkovMat
       self.GridAsset = np.linspace(self.BoroLmt, self.aMax, self.NumGridAsset)
       
         
   def IndSolve(self, rfree):
       '''
       Solve the individual agent's problem for next period asset(Aprime) 
       and consumption(C) for a given risk-free rate
       
       Parameters
       ----------
       rfree : float
           interest rate of a risk-free asset
       
       Returns
       -------
       Aprime : np.array
           policy function for the next period asset
       C : np.array
           policy function for the consumption
       '''
       GridAsset = self.GridAsset
       GridIncome = self.GridIncome
       meshs, mesha = np.meshgrid(GridIncome,GridAsset,indexing='ij')
       C = self.Wage*meshs + rfree*mesha
       mutil = lambda x : 1/x**(self.CRRA)
       invmutil = lambda x : 1/x**(1/self.CRRA)
              
       Cold = C.copy()
       dist = 9999
       Aprime = mesha.copy()
       
       while (dist > self.tolerance):
           mu = mutil(C)
           emu = self.MarkovMat.dot(mu)
           Cstar = invmutil(self.DiscFac * (1+rfree) * emu)
           Astar = (Cstar + mesha.copy() - self.Wage*meshs.copy())/(1+rfree)
           
           for s in range(0,self.NumGridIncome):
               Savingsfunc = interp1d(Astar[s,:], GridAsset, fill_value='extrapolate')
               Aprime[s] = Savingsfunc(GridAsset)
               Consumptionfunc = interp1d(Astar[s,:], Cstar[s,:], fill_value='extrapolate')
               C[s] = Consumptionfunc(GridAsset)
           
           BorrowConstrained = mesha <  np.tile(np.vstack(Astar[:,0]),(1,self.NumGridAsset))
           C[BorrowConstrained] = (1+rfree) * mesha[BorrowConstrained] + self.Wage*meshs[BorrowConstrained] - self.BoroLmt
           dista = abs(C-Cold)
           dist = dista.max()   
           Cold = C.copy()
                      
       Aprime[BorrowConstrained]=self.BoroLmt           
       return {'Aprime': Aprime, 'C': C}
       
       
   def transMat(self, Aprime):
       '''
       Construct a transition matrix for assets and incomes based on 
       the policy function Aprime and Markov matrix of income shock
       
       Parameters
       ----------
       Aprime : np.array
           policy function for the next period asset
       
       Returns
       -------
       Transition : sp.coo.coo_matrix
           transition matrix for assets and incomes
       
       '''
       GridAsset = self.GridAsset
       idx = np.digitize(Aprime, GridAsset)-1
       idx[Aprime <= GridAsset[0]] = 0
       idx[Aprime >= GridAsset[-1]] = self.NumGridAsset-2
       distance = Aprime - GridAsset[idx]
       weightright = np.minimum(distance/(GridAsset[idx+1]-GridAsset[idx]) ,1)
       weightleft = 1-weightright
       ind1, ind2 = np.meshgrid(range(0,self.NumGridIncome),range(0, self.NumGridAsset),indexing='ij')
       row = np.ravel_multi_index([ind1.flatten(order='F'),ind2.flatten(order='F')],(self.NumGridIncome,self.NumGridAsset),order='F')
       rowindex=[]
       colindex=[]
       value=[]

       for s in range(0,self.NumGridIncome):
           pi = np.tile(self.MarkovMat[:,s],(self.NumGridAsset,1))
           rowindex.append(row)
           col = np.ravel_multi_index([[s]*(self.NumGridAsset*self.NumGridIncome),idx.flatten(order='F')],
                                       (self.NumGridIncome,self.NumGridAsset),order='F')
           colindex.append(col)
           rowindex.append(row)
           col = np.ravel_multi_index([[s]*(self.NumGridAsset*self.NumGridIncome),idx.flatten(order='F')+1],
                                       (self.NumGridIncome,self.NumGridAsset),order='F')
           colindex.append(col)
           value.extend((pi.flatten()*weightleft.flatten(order='F'), pi.flatten()*weightright.flatten(order='F') )) 

       value=np.asarray(value)
       rowindex=np.asarray(rowindex)
       colindex=np.asarray(colindex)
       Transition = sp.coo_matrix((value.flatten(), (rowindex.flatten(), colindex.flatten())), shape=(self.NumGridIncome*self.NumGridAsset,self.NumGridIncome*self.NumGridAsset) )
       return Transition

   def unitEigen(self,Transition):
       '''
       Calculate the unit-eigenvector of the transition matrix 
       which is the stationary distribution of the asset
       
       Parameters
       ----------
       Transition : sp.coo.coo_matrix
           transition matrix for assets and incomes
       
       Returns
       -------
       distr : np.array
           stationary distribution of the asset
              
       '''
       eigen, distr = sp.linalg.eigs(Transition.transpose(), k=1, which='LM')
       distr = distr/distr.sum()
       distr = distr.reshape(self.NumGridIncome,self.NumGridAsset,order='F').copy()
       distr = distr.real
       return distr
            
   def ExcessA(self,Aprime,distr):
       '''
       Calculate excess demand for the asset
       
       Parameters
       ----------
       Aprime : np.array
           policy function for the next period asset
       distr : np.array
           stationary distribution of the asset
       
       Returns
       -------
       ExcessA : float
           excess demand for the asset
              
       '''
       Aprime = Aprime.flatten(order='F')
       ExcessA = (Aprime.transpose()).dot(distr.flatten(order='F'))
       return ExcessA
   
   def EquilSolve(self):
       '''
       Solve for the equilibrium interest rate using bisection method
       
       Parameters
       ----------
       None
       
       Returns
       -------
       r : float
           equilibrium risk-free interest rate
       Aprime : np.array
           policy function for the next period asset
       Transition : sp.coo.coo_matrix
           transition matrix for assets and incomes
       dist : np.array
           stationary distribution of the asset
       '''
       rmax = self.rMax
       rmin = self.rMin
       r = (self.rMax+self.rMin)/2
       init = 5
       
       while abs(init) > self.tolerance:
             Result = self.IndSolve(r)
             TRM = self.transMat(Result['Aprime'])
             distr = self.unitEigen(TRM)
             ExcessA = self.ExcessA(Result['Aprime'],distr)
             
             if ExcessA > 0:
                rmax = (r + rmax)/2
             else:
                rmin = (r + rmin)/2
             
             init = rmax-rmin   
             print 'Starting Iteration for r. Difference remaining:     ',  init
             
             r = (rmax + rmin)/2
                         
       return {'r': r, 'Aprime': Result['Aprime'], 'Transition': TRM, 'dist': distr  }

# -----------------------------------------------------------------------------
# --- Define all of the parameters for Hugget model ------------
# -----------------------------------------------------------------------------

BoroLmt = -2                        # Borrowing limit
CRRA = 2.0                          # Coefficient of relative risk aversion
DiscFac = 0.99                      # Intertemporal discount factor
Wage = 1                            # Wage multiplier

NumGridAsset = 100                  # Number of grid for asset
NumGridIncome = 5                   # Number of grid for income
tolerance = 10**(-10)               # Numerical precision
rMax = 1/DiscFac -1                 # Maximum interest rate under consideration (complete market rate)
rMin = -0.017                       # Minimum interest rate under consideration
aMin = BoroLmt                      # Borrowing constraint  
aMax = 10                           # upper bound for asset

GridIncome = np.array([0.6177, 0.8327, 1, 1.2009, 1.6188])     # income grid
MarkovMat = np.array([[0.7497,  0.2161, 0.0322, 0.002,  0],    # Markov matrix for idiosyncratic income shock
                   [0.2161,  0.4708, 0.2569, 0.0542, 0.002],
                   [0.0322,  0.2569, 0.4218, 0.2569, 0.0322],
                   [0.002,   0.0542, 0.2569, 0.4708, 0.2161],
                   [0,       0.002,  0.0322, 0.2161, 0.7497]])

# Make a dictionary to specify model parameters
hugget_param = { 'BoroLmt' : BoroLmt, 
                 'CRRA' : CRRA,
                 'DiscFac' : DiscFac,
                 'Wage' : Wage,
                 'NumGridAsset' : NumGridAsset,
                 'NumGridIncome' : NumGridIncome,
                 'tolerance' : tolerance,
                 'rMax' : rMax,
                 'rMin' : rMin,
                 'aMax' : aMax,
                 'aMin' : aMin,
                 'GridIncome' : GridIncome,
                 'MarkovMat' : MarkovMat}            
       

# Make an instance for Hugget model       
EX       = HuggetModel(**hugget_param)

# Solve the model for the equilibrium interest rate
start_time = time.clock()
resultr=EX.EquilSolve()
end_time = time.clock()
print 'Elapsed time is ',  (end_time-start_time), ' seconds.'
print(resultr['r'])

'''
# Solve the individual agent's problem with r = (rMax+rMin)/2
start_time = time.clock()
result1=EX.IndSolve((rMax+rMin)/2)
end_time = time.clock()
print 'Elapsed time is ',  (end_time-start_time), ' seconds.'
TRM=EX.transMat(result1['Aprime'])
print(result1['Aprime'])

'''

# plot the solution
plt.plot(EX.GridAsset,resultr['Aprime'][0,:],
         EX.GridAsset,resultr['Aprime'][1,:],
         EX.GridAsset,resultr['Aprime'][2,:],
         EX.GridAsset,resultr['Aprime'][3,:],
         EX.GridAsset,resultr['Aprime'][4,:])
plt.legend(['Income 1','Income 2','Income 3','Income 4','Income 5'])
plt.xlabel('a')
plt.ylabel('a prime')       
plt.title('Policy function for next period a')
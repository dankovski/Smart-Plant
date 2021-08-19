import skfuzzy
from skfuzzy import control as ctrl
import numpy as np

class controller_fuzzy:
    def calculate_output(self, desired_lux, actual_lux):
 
        e = desired_lux - actual_lux
        self.simulation.input['error'] = e
    
        e_d = e - self.previous_e
        self.simulation.input['error_delta'] = e_d
    
        self.sum_error = self.sum_error + e
        self.simulation.input['error_sum'] = self.sum_error
    
        self.previous_e = e
    
        self.simulation.compute()
        d_out = self.simulation.output['output']
        self.out = self.out + d_out

        if self.out >100:
            self.out=100
        if self.out < 0:
            self.out=0
        return self.out
        
    def reset(self):
        self.previous_e1 = 0
        self.sum_error = 0
        self.out = 0 
        self.previous_e2 = 0
        self.previous_e = 0
        self.out = 0
    
    def __init__(self):
        self.previous_e1 = 0
        self.sum_error = 0
        self.out = 0 
        self.previous_e2 = 0
        self.previous_e = 0
        self.out = 0
            
        self.error = ctrl.Antecedent(np.arange(-20, 20, 0.1), 'error')
        self.error_delta = ctrl.Antecedent(np.arange(-20, 20, 0.1), 'error_delta')
        self.error_sum = ctrl.Antecedent(np.arange(-32000, 32000, 0.1), 'error_sum')
        self.output = ctrl.Consequent(np.arange(-2.5, 2.5, 0.01), 'output')


        self.error['DU'] = skfuzzy.trapmf(self.error.universe, [-20, -20, -15, -10])
        self.error['ŚU'] = skfuzzy.trimf(self.error.universe, [-15, -10, -5])
        self.error['MU'] = skfuzzy.trimf(self.error.universe, [-10, -5, 0])
        self.error['Z'] = skfuzzy.trimf(self.error.universe, [-5, 0, 5])
        self.error['MD'] = skfuzzy.trimf(self.error.universe, [0, 5, 10])
        self.error['ŚD'] = skfuzzy.trimf(self.error.universe, [5, 10, 15])
        self.error['DD'] = skfuzzy.trapmf(self.error.universe, [10, 15, 20, 20])

        self.error_delta['DU'] = skfuzzy.trapmf(self.error_delta.universe, [-20, -20, -15, -10])
        self.error_delta['ŚU'] = skfuzzy.trimf(self.error_delta.universe, [-15, -10, -5])
        self.error_delta['MU'] = skfuzzy.trimf(self.error_delta.universe, [-10, -5, 0])
        self.error_delta['Z'] = skfuzzy.trimf(self.error_delta.universe, [-5, 0, 5])
        self.error_delta['MD'] = skfuzzy.trimf(self.error_delta.universe, [0, 5, 10])
        self.error_delta['ŚD'] = skfuzzy.trimf(self.error_delta.universe, [5, 10, 15])
        self.error_delta['DD'] = skfuzzy.trapmf(self.error_delta.universe, [10, 15, 20, 20])

        self.error_sum['DU'] = skfuzzy.trapmf(self.error_sum.universe, [-32000, -32000, -24000, -16000])
        self.error_sum['ŚU'] = skfuzzy.trimf(self.error_sum.universe, [-24000, -16000, -8000])
        self.error_sum['MU'] = skfuzzy.trimf(self.error_sum.universe, [-16000, -8000, 0])
        self.error_sum['Z'] = skfuzzy.trimf(self.error_sum.universe, [-8000, 0, 8000])
        self.error_sum['MD'] = skfuzzy.trimf(self.error_sum.universe, [0, 8000, 16000])
        self.error_sum['ŚD'] = skfuzzy.trimf(self.error_sum.universe, [8000, 16000, 24000])
        self.error_sum['DD'] = skfuzzy.trapmf(self.error_sum.universe, [16000, 24000, 32000, 32000])


        self.output['BDU'] = skfuzzy.trapmf(self.output.universe, [-2.5, -2.5, -2.0, -1.5])
        self.output['DU'] = skfuzzy.trimf(self.output.universe, [-2.0, -1.5, -1.0])
        self.output['ŚU'] = skfuzzy.trimf(self.output.universe, [-1.5, -1.0, -0.5])
        self.output['MU'] = skfuzzy.trimf(self.output.universe, [-1.0, -0.5, 0.0])
        self.output['Z'] = skfuzzy.trimf(self.output.universe, [-0.5, 0.0, 0.5])
        self.output['MD'] = skfuzzy.trimf(self.output.universe, [0.0, 0.5, 1.0])
        self.output['ŚD'] = skfuzzy.trimf(self.output.universe, [0.5, 1.0, 1.5])
        self.output['DD'] = skfuzzy.trimf(self.output.universe, [1.0, 1.5, 2.0])
        self.output['BDD'] = skfuzzy.trapmf(self.output.universe, [1.5, 2.0, 2.5, 2.5])

        rule0 = ctrl.Rule(antecedent=(
                
                #BDU
                ( (self.error_sum['DU'] | self.error_sum['ŚU'] | self.error_sum['MU'] | self.error_sum['Z']) & (self.error['MU'] & self.error_delta['DU']) |
                  (self.error['DU'] & self.error_delta['MU']) |(self.error['ŚU'] & self.error_delta['ŚU'])) | ( (self.error_sum['DU'] | self.error_sum['ŚU'] |
                 self.error_sum['MU'] | self.error_sum['Z'] | self.error_sum['MD']) & (self.error['DU'] & self.error_delta['ŚU']) | (self.error['ŚU'] &
                self.error_delta['DU'])) | ( (self.error_sum['DU'] | self.error_sum['ŚU'] | self.error_sum['MU'] | self.error_sum['Z'] | self.error_sum['MD'] |
                self.error_sum['ŚD']) & (self.error['DU'] & self.error_delta['DU'])) |        
                #DU
                ( (self.error_sum['MU'] | self.error_sum['ŚU'] | self.error_sum['DU']) & ( (self.error['DU'] & self.error_delta['Z']) |
                (self.error['ŚU'] & self.error_delta['MU']) | (self.error['MU'] & self.error_delta['ŚU']) | (self.error['Z'] & self.error_delta['DU'])
                )) |
                #ŚU
                ( (self.error_sum['ŚU'] | self.error_sum['DU'] ) & (
                (self.error['DU'] & self.error_delta['MD']) | (self.error['ŚU'] & self.error_delta['Z']) | (self.error['MU'] & self.error_delta['MU']) |
                (self.error['Z'] & self.error_delta['ŚU']) | (self.error['MD'] & self.error_delta['DU'])         
                )) |
                #MU
                ( self.error_sum['DU'] & (
                (self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] & self.error_delta['Z']) |        
                (self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU'])  
                ))
                   
        ), consequent=self.output['BDU'], label='rule BDU')

        rule1 = ctrl.Rule(antecedent=(
                
                #BDU
                ( (self.error_sum['MD']) & 
                (self.error['MU'] & self.error_delta['DU']) |  (self.error['DU'] & self.error_delta['MU']) |  (self.error['ŚU'] & self.error_delta['ŚU'])) |( (self.error_sum['ŚD'] ) &
                (self.error['DU'] & self.error_delta['ŚU']) |(self.error['ŚU'] & self.error_delta['DU'])) | ( (self.error_sum['DD']) &  (self.error['DU'] & self.error_delta['DU'])) |
                #DU
                ( self.error_sum['Z'] & (
                (self.error['DU']&self.error_delta['Z'])|(self.error['ŚU'] & self.error_delta['MU'])|(self.error['MU']&self.error_delta['ŚU']) |(self.error['Z'] & self.error_delta['DU']))) |
                #ŚU
                ( self.error_sum['MU'] & (
                (self.error['DU'] & self.error_delta['MD']) | (self.error['ŚU'] & self.error_delta['Z']) | (self.error['MU'] & self.error_delta['MU']) |
                (self.error['Z'] & self.error_delta['ŚU']) | (self.error['MD'] & self.error_delta['DU'])   ))|
                #MU
                ( self.error_sum['ŚU'] & (
                (self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] & self.error_delta['Z']) |        
                (self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU']) )) |     
                #Z
                ( self.error_sum['DU'] & ((self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) |
                (self.error['MU'] & self.error_delta['MD']) | (self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) |
                (self.error['ŚD'] & self.error_delta['ŚU']) |   (self.error['DD'] & self.error_delta['DU'])  ))           
        ), consequent=self.output['DU'], label='rule DU')

        rule2 = ctrl.Rule(antecedent=(
                #BDU
                ( (self.error_sum['ŚD']) & 
                (self.error['MU'] & self.error_delta['DU']) |        (self.error['DU'] & self.error_delta['MU']) |        (self.error['ŚU'] & self.error_delta['ŚU'])) |
                ( (self.error_sum['DD'] ) &         (self.error['DU'] & self.error_delta['ŚU']) |        (self.error['ŚU'] & self.error_delta['DU'])) |
                #DU
                ( self.error_sum['MD'] & (
                (self.error['DU'] & self.error_delta['Z']) | (self.error['ŚU'] & self.error_delta['MU']) | (self.error['MU'] & self.error_delta['ŚU']) |
                (self.error['Z'] & self.error_delta['DU'])
                )) |
                #ŚU
                ( self.error_sum['Z'] & (
                (self.error['DU'] & self.error_delta['MD']) | (self.error['ŚU'] & self.error_delta['Z']) | (self.error['MU'] & self.error_delta['MU']) |
                (self.error['Z'] & self.error_delta['ŚU']) | (self.error['MD'] & self.error_delta['DU'])        )) |     
                #MU
                ( self.error_sum['MU'] & (
                (self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] & self.error_delta['Z']) |        
                (self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU'])          )) |        
                #Z
                ( self.error_sum['ŚU'] & (        (self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) |
                (self.error['MU'] & self.error_delta['MD']) |        (self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) |
                (self.error['ŚD'] & self.error_delta['ŚU']) |        (self.error['DD'] & self.error_delta['DU'])         )) |
                #MD
                ( self.error_sum['DU'] & ( (self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD']) | (self.error['Z'] & self.error_delta['MD']) |
                (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) |     (self.error['DD'] & self.error_delta['ŚU'])      ))       
        ), consequent=self.output['ŚU'], label='rule ŚU')

        rule3 = ctrl.Rule(antecedent=(  
                #BDU
                ( (self.error_sum['DD']) & (self.error['MU'] & self.error_delta['DU']) | (self.error['DU'] & self.error_delta['MU']) | (self.error['ŚU'] & self.error_delta['ŚU'])) |
                #DU
                ( self.error_sum['ŚD'] & (        (self.error['DU'] & self.error_delta['Z']) | (self.error['ŚU'] & self.error_delta['MU']) |
                          (self.error['MU'] & self.error_delta['ŚU']) |        (self.error['Z'] & self.error_delta['DU'])        )) |
                #ŚU
                ( self.error_sum['MD'] & ((self.error['DU'] & self.error_delta['MD']) | (self.error['ŚU'] & self.error_delta['Z']) |
                (self.error['MU'] & self.error_delta['MU']) | (self.error['Z'] & self.error_delta['ŚU']) | (self.error['MD'] & self.error_delta['DU'])))|  
                #MU
                ( self.error_sum['Z'] & ((self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] & self.error_delta['Z']) |        
                (self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU'])   )) |        
                #Z
                ( self.error_sum['MU'] & ( (self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) | (self.error['MU'] &
                self.error_delta['MD']) |(self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) | (self.error['ŚD'] & self.error_delta['ŚU']) |
                (self.error['DD'] & self.error_delta['DU']) )) |
                #MD
                ( self.error_sum['ŚU'] & ( (self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD']) |(self.error['Z'] & self.error_delta['MD']) |
                 (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) | (self.error['DD'] & self.error_delta['ŚU'])  ))|  
                #ŚD
                ( self.error_sum['DU'] & ((self.error['MU'] & self.error_delta['DD']) |(self.error['Z'] & self.error_delta['ŚD']) | (self.error['MD'] & self.error_delta['MD']) |
                (self.error['ŚD'] & self.error_delta['Z']) |(self.error['DD'] & self.error_delta['MU']) ))    
        ), consequent=self.output['MU'], label='rule MU')

        rule4 = ctrl.Rule(antecedent=(     
                #DU
                ( self.error_sum['DD'] & ((self.error['DU'] & self.error_delta['Z']) | (self.error['ŚU'] & self.error_delta['MU']) | (self.error['MU'] &
                self.error_delta['ŚU']) | (self.error['Z'] & self.error_delta['DU'])  )) |
                #ŚU
                ( self.error_sum['ŚD'] & ( (self.error['DU'] & self.error_delta['MD']) | (self.error['ŚU'] & self.error_delta['Z']) | (self.error['MU'] &
                 self.error_delta['MU']) |  (self.error['Z'] & self.error_delta['ŚU']) | (self.error['MD'] & self.error_delta['DU'])    ))|
                #MU
                ( self.error_sum['MD'] & ((self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] & self.error_delta['Z']) |        
                (self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU'])    ))|
                #Z
                ( self.error_sum['Z'] & ((self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) | (self.error['MU'] & self.error_delta['MD']) |
                (self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) | (self.error['ŚD'] & self.error_delta['ŚU']) |
                (self.error['DD'] & self.error_delta['DU'])     ))|
                #MD
                ( self.error_sum['MU'] & ((self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD']) | (self.error['Z'] & self.error_delta['MD']) |
                (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) | (self.error['DD'] & self.error_delta['ŚU'])     ))|
                #ŚD
                ( self.error_sum['ŚU'] & ((self.error['MU'] & self.error_delta['DD']) | (self.error['Z'] & self.error_delta['ŚD']) | (self.error['MD'] & self.error_delta['MD']) |
                (self.error['ŚD'] & self.error_delta['Z']) |        (self.error['DD'] & self.error_delta['MU'])         )) |
                #DD
                ( self.error_sum['DU'] &( (self.error['Z'] & self.error_delta['DD']) | (self.error['MD'] & self.error_delta['ŚD']) |
                (self.error['ŚD'] & self.error_delta['MD']) |  (self.error['DD'] & self.error_delta['Z'])    ))
        ), consequent=self.output['Z'], label='rule Z')

        rule5 = ctrl.Rule(antecedent=( 
                #ŚU
                ( self.error_sum['DD'] & ((self.error['DU'] & self.error_delta['MD']) | (self.error['ŚU'] & self.error_delta['Z']) | (self.error['MU'] &
                self.error_delta['MU']) |  (self.error['Z'] & self.error_delta['ŚU']) | (self.error['MD'] & self.error_delta['DU']) ))|
                #MU
                ( self.error_sum['ŚD'] & (  (self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] &
                self.error_delta['Z']) |(self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU']) ))|
                #Z
                ( self.error_sum['MD'] & ((self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) | (self.error['MU'] & self.error_delta['MD']) |
                (self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) | (self.error['ŚD'] & self.error_delta['ŚU']) |
                (self.error['DD'] & self.error_delta['DU'])   ))|
                #MD
                ( self.error_sum['Z'] & (   (self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD']) |
                (self.error['Z'] & self.error_delta['MD']) | (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) |
                (self.error['DD'] & self.error_delta['ŚU'])       ))|
                #ŚD
                ( self.error_sum['MU'] & ((self.error['MU'] & self.error_delta['DD']) |(self.error['Z'] & self.error_delta['ŚD']) |
                (self.error['MD'] & self.error_delta['MD']) |(self.error['ŚD'] & self.error_delta['Z']) |(self.error['DD'] & self.error_delta['MU'])  )) |
                #DD
                ( self.error_sum['ŚU'] &((self.error['Z'] & self.error_delta['DD']) | (self.error['MD'] & self.error_delta['ŚD']) |
                (self.error['ŚD'] & self.error_delta['MD']) |(self.error['DD'] & self.error_delta['Z'])  ))|
                #BDD
                ( self.error_sum['DU'] & ((self.error['DD'] & self.error_delta['MD']) |(self.error['ŚD'] & self.error_delta['ŚD']) | (self.error['MD'] & self.error_delta['DD']) ))     
        ), consequent=self.output['MD'], label='rule MD')

        rule6 = ctrl.Rule(antecedent=(            
                #MU
                ( self.error_sum['DD'] & ( (self.error['DU'] & self.error_delta['ŚD']) | (self.error['ŚU'] & self.error_delta['MD']) | (self.error['MU'] & self.error_delta['Z']) |        
                (self.error['Z'] & self.error_delta['MU']) | (self.error['MD'] & self.error_delta['ŚU']) | (self.error['ŚD'] & self.error_delta['DU'])     ))|
                #Z
                ( self.error_sum['ŚD'] & ((self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) | (self.error['MU'] & self.error_delta['MD']) |
                (self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) | (self.error['ŚD'] & self.error_delta['ŚU']) | (self.error['DD'] & self.error_delta['DU'])   ))|
                #MD
                ( self.error_sum['MD'] & ( (self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD'])| (self.error['Z'] & self.error_delta['MD']) |
                (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) | (self.error['DD'] & self.error_delta['ŚU'])   ))|
                #ŚD
                ( self.error_sum['Z'] & ((self.error['MU'] & self.error_delta['DD']) | (self.error['Z'] & self.error_delta['ŚD']) | (self.error['MD'] & self.error_delta['MD']) |
                (self.error['ŚD'] & self.error_delta['Z']) |    (self.error['DD'] & self.error_delta['MU'])     )) |
                #DD
                ( self.error_sum['MU'] &( (self.error['Z'] & self.error_delta['DD']) | (self.error['MD'] & self.error_delta['ŚD']) | (self.error['ŚD'] &
                self.error_delta['MD']) |(self.error['DD'] & self.error_delta['Z'])    ))|
                #BDD
                ( self.error_sum['ŚU'] &( (self.error['ŚD'] & self.error_delta['ŚD']) | (self.error['DD'] & self.error_delta['MD']) | (self.error['MD'] & self.error_delta['DD'])  )) |
                ( self.error_sum['DU'] &( (self.error['DD'] & self.error_delta['ŚD']) | (self.error['ŚD'] & self.error_delta['DD']) ))
        ), consequent=self.output['ŚD'], label='rule ŚD')

        rule7 = ctrl.Rule(antecedent=(
                #Z
                ( self.error_sum['DD'] & ( (self.error['DU'] & self.error_delta['DD']) | (self.error['ŚU'] & self.error_delta['ŚD']) | (self.error['MU'] & self.error_delta['MD']) |
                (self.error['Z'] & self.error_delta['Z']) | (self.error['MD'] & self.error_delta['MU']) | (self.error['ŚD'] & self.error_delta['ŚU']) |(self.error['DD'] & self.error_delta['DU'])))|
                #MD
                ( self.error_sum['ŚD'] & ( (self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD']) | (self.error['Z'] & self.error_delta['MD']) |
                (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) |   (self.error['DD'] & self.error_delta['ŚU'])   ))|
                #ŚD
                ( self.error_sum['MD'] & ((self.error['MU'] & self.error_delta['DD']) | (self.error['Z'] & self.error_delta['ŚD']) |  (self.error['MD'] & self.error_delta['MD']) |
                (self.error['ŚD'] & self.error_delta['Z']) |  (self.error['DD'] & self.error_delta['MU'])     )) |  
                #DD
                ( self.error_sum['Z'] &((self.error['Z'] & self.error_delta['DD'])|(self.error['MD'] & self.error_delta['ŚD']) | (self.error['ŚD'] & self.error_delta['MD']) |
                (self.error['DD'] & self.error_delta['Z'])  ))| 
                #BDD
                ( self.error_sum['MU'] &(  (self.error['ŚD'] & self.error_delta['ŚD']) | (self.error['DD'] & self.error_delta['MD']) |  (self.error['MD'] & self.error_delta['DD'])  ))|
                ( self.error_sum['ŚU'] &(  (self.error['DD'] & self.error_delta['ŚD']) | (self.error['ŚD'] & self.error_delta['DD'])))|
                ( self.error_sum['DU'] &( (self.error['DD'] & self.error_delta['DD']) ))    
        ), consequent=self.output['DD'], label='rule DD')

        rule8 = ctrl.Rule(antecedent=(      
                #MD
                ( self.error_sum['DD'] & (  (self.error['ŚU'] & self.error_delta['DD']) | (self.error['MU'] & self.error_delta['ŚD']) | (self.error['Z'] & self.error_delta['MD']) |
                (self.error['MD'] & self.error_delta['Z']) | (self.error['ŚD'] & self.error_delta['MU']) |  (self.error['DD'] & self.error_delta['ŚU'])   ))|
                #ŚD
                ( (self.error_sum['ŚD'] | self.error_sum['DD'] ) & ( (self.error['MU'] & self.error_delta['DD']) | (self.error['Z'] & self.error_delta['ŚD']) |
                (self.error['MD'] & self.error_delta['MD']) | (self.error['ŚD'] & self.error_delta['Z']) | (self.error['DD'] & self.error_delta['MU']) )) |
                #DD
                ( (self.error_sum['MD'] | self.error_sum['ŚD'] | self.error_sum['DD']) &((self.error['Z'] & self.error_delta['DD']) |
                (self.error['MD'] & self.error_delta['ŚD']) |(self.error['ŚD'] & self.error_delta['MD']) | (self.error['DD'] & self.error_delta['Z'])  ))| 
                #BDD
                ( (self.error_sum['DD'] | self.error_sum['ŚD'] | self.error_sum['MD'] | self.error_sum['MU'] | self.error_sum['MU'] | self.error_sum['Z']  )&( (self.error['ŚD'] & self.error_delta['ŚD']) |
                (self.error['DD'] & self.error_delta['MD']) | (self.error['MD'] & self.error_delta['DD'])     ))|
                ( (self.error_sum['DD'] | self.error_sum['ŚD'] | self.error_sum['MD'] | self.error_sum['MU'] | self.error_sum['MU'] | self.error_sum['Z'] | self.error_sum['MD']) &(
                (self.error['DD'] & self.error_delta['ŚD']) |  (self.error['ŚD'] & self.error_delta['DD'])   ))|
                ( (self.error_sum['DD'] | self.error_sum['ŚD'] | self.error_sum['MD'] | self.error_sum['MU'] | self.error_sum['MU'] | self.error_sum['Z'] | self.error_sum['MD'] | self.error_sum['ŚD']) &(
                (self.error['DD'] & self.error_delta['DD']) ))    
        ), consequent=self.output['BDD'], label='rule BDD')

        system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
        self.simulation = ctrl.ControlSystemSimulation(system)


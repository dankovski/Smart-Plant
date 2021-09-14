
class pid_controller:
    def __init__(self):
        #default values
        self.kd = 0.01
        self.kp = 0.013
        self.ki = 0.04
        
        self.sum_e = 0
        self.previous_e = 0

    def reset(self):
                    #reading config
        try:
            with open('static/data/config.json','r') as file:
                config = json.load(file)
                file.close()
                self.kd = float(config[0]['kd'])
                self.kp = float(config[0]['kp'])
                self.ki = float(config[0]['ki'])
        except:
            print("Can't open config.json")
        
        
        self.sum_e = 0
        self.previous_e = 0


    def calculate_output(self,desired_lux, actual_lux, dt):
        e = desired_lux - actual_lux
        self.sum_e = self.sum_e + e
        P = self.kp * e
        I = self.ki * self.sum_e * dt
        D = self.kd * (e - self.previous_e) * dt
        self.previous_e = e
        
        
        #print("\n\nP"+str(P))
        #print("I"+str(I))
        #print("D"+str(D))
        #print("self.sum_e"+str(self.sum_e))
        #print("dt"+str(dt))
        
        PID = P + I + D
        
    
        if PID < 0.0:
            PID = 0.0
        if PID > 100.0:
            PID = 100.0
        return PID
    

from clickpirc.Motor import Motor

class MultipiRCControl:
    CAR_MOTOR_FRONTREAR=1
    CAR_MOTOR_REAR2WHEEL=2
    def __init__(self, CAR_MOTOR_MODE=CAR_MOTOR_REAR2WHEEL, M1_A=4, M1_B=17, M2_A=27, M2_B=22):
        
        self.CAR_MOTOR_MODE = CAR_MOTOR_MODE
        self.M1_A = M1_A;
        self.M1_B = M1_B;
        self.M2_A = M2_A;
        self.M2_B = M2_B;

        
        self.set2DCMotor()
        if self.CAR_MOTOR_MODE == self.CAR_MOTOR_REAR2WHEEL:
            self.SetDCMotorLRRCCar()
        elif self.CAR_MOTOR_MODE == self.CAR_MOTOR_FRONTREAR:
            self.SetDCMotorFRRCCar()
        else :
            print ("Mode Error")   

    def set2DCMotor(self):
        try:
            print ('set2DCMotor')
            self.motor1 = Motor(self.M1_A, self.M1_B)
            self.motor2 = Motor(self.M2_A, self.M2_B)
        except Exception as Err:
            print('%s' % Err)
    
        
    def SetDCMotorLRRCCar(self):    
        try:
            print ('SetDCMotorLRRCCar')
            self.set2DCMotor()
            self.CAR_MOTOR_MODE = self.CAR_MOTOR_REAR2WHEEL
        except Exception as Err:
            printf ('%s' % Err)
    def SetDCMotorFRRCCar(self):
        try:
            print('SetDCMotorFRRCCar')
            self.set2DCMotor()
            self.CAR_MOTOR_MODE = self.CAR_MOTOR_FRONTREAR
        except Exception as Err:
            printf('%s' % Err)

    def TurnLeft(self):
        try:
            print('TurnLeft')
            if self.CAR_MOTOR_MODE == self.CAR_MOTOR_REAR2WHEEL:
                self.motor1.runMotorDirectionCCW()
                self.motor2.runMotorDirectionCCW()
            elif self.CAR_MOTOR_MODE == self.CAR_MOTOR_FRONTREAR:
                self.motor1.runMotorDirectionCW()
        except Exception as Err:
            print('%s' % Err)
    def TurnRight(self):
        try:
            print('TurnRight')
            if self.CAR_MOTOR_MODE == self.CAR_MOTOR_REAR2WHEEL:
                self.motor1.runMotorDirectionCW()
                self.motor2.runMotorDirectionCW()
            elif self.CAR_MOTOR_MODE == self.CAR_MOTOR_FRONTREAR:
                self.motor1.runMotorDirectionCCW()
        except Exception as Err:
            print('%s' % Err)

    def MoveForward(self):
        try:
            print('MoveForward')
            if self.CAR_MOTOR_MODE == -1:
                print('MoveForward')
                self.SetDCMotorLRRCCar()
            if self.CAR_MOTOR_MODE == self.CAR_MOTOR_REAR2WHEEL:
                print('self.CAR_MOTOR_MODE == self.CAR_MOTOR_REAR2WHEEL')
                self.motor1.runMotorDirectionCW()
                self.motor2.runMotorDirectionCCW()
            elif self.CAR_MOTOR_MODE == self.CAR_MOTOR_FRONTREAR:
                print('self.CAR_MOTOR_MODE == self.CAR_MOTOR_FRONTREAR')
                self.motor2.runMotorDirectionCCW()
        except Exception as Err:
            print('%s' % Err)
    
    def MoveBackward(self):
        try:
            print('MoveBackward')
            if self.CAR_MOTOR_MODE == -1:
                self.SetDCMotorLRRCCar()
            if self.CAR_MOTOR_MODE == self.CAR_MOTOR_REAR2WHEEL:
                self.motor1.runMotorDirectionCCW()
                self.motor2.runMotorDirectionCW()
            elif self.CAR_MOTOR_MODE == self.CAR_MOTOR_FRONTREAR:
                self.motor2.runMotorDirectionCW()
        except Exception as Err:
            print('%s' % Err)
    
    def Stop(self):
        try:
            print('Stop')
            if self.CAR_MOTOR_MODE == -1:
                self.SetDCMotorLRRCCar()
            self.motor1.stopMotor()
            self.motor2.stopMotor()
        except Exception as Err:
            print('%s' % Err)
    

    def SyncAllMotor(self):
        self.motor1.syncMotorFromCommandStatus()
        self.motor2.syncMotorFromCommandStatus()
        
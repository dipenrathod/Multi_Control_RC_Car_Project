import sockjs.tornado
from clickpirc.rccontrol import MultipiRCControl

class RcSockjsConnection(sockjs.tornado.SockJSConnection):
    def on_open(self, request):
        print "sockjs: open"
        
        self.rccontrol = MultipiRCControl(MultipiRCControl.CAR_MOTOR_REAR2WHEEL)

    def on_message(self, rcvdata):
        print "data: %r" % (rcvdata,)
        
        data = rcvdata.encode("utf-8")
        print "data: %s" % (data,)
        if data == 'fw':
            print 'get Forward'
            self.rccontrol.MoveForward()
        if data == 'bw':
            print 'get Backward'
            self.rccontrol.MoveBackward()
        if data == 'lt':
            print 'get Left'
            self.rccontrol.TurnLeft()
        if data == 'rt':
            print 'get Right'
            self.rccontrol.TurnRight()
        if data == 'st':
            print 'get Stop'
            self.rccontrol.Stop()
        if data == 'fr':
            print 'change motor mode to CAR_MOTOR_FRONTREAR'
            self.rccontrol.SetDCMotorFRRCCar()
        if data == 'lr':  
            print 'change motor mode to CAR_MOTOR_REAR2WHEEL'
            self.rccontrol.SetDCMotorLRRCCar()

        self.rccontrol.SyncAllMotor()
        self.send(rcvdata)

    def on_close(self):
        print "sockjs: close"
        self.rccontrol.offRCCar()

    
def RcSockjsRouter(prefix):
    return sockjs.tornado.SockJSRouter(RcSockjsConnection, prefix).urls

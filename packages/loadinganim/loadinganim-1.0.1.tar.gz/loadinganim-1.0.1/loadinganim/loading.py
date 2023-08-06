from multiprocessing import Process
import time

def loadingAnim(message,animChars,animType):
    chars = animChars[animType]
    index=0
    while True:
        print(message+' '+chars[index],end='\r')
        index += 1
        index %= len(chars)
        time.sleep(0.25)

class LoadingAnim:
    def __init__(self,message: str = 'Loading',animType: int = 0):
        if(animType!=0 and animType!=1):
            animType = 0
        self.animType = animType
        self.message = message
        self.animChars=[['-','\\','|','/'],['.   ','..  ','... ','....','... ','..  ']]
        self.hasStarted = False
        self.loading = None

    def start(self):
        if(not self.hasStarted):
            self.hasStarted = True
            self.loading = Process(target=loadingAnim,args=(self.message,self.animChars,self.animType))
            try:
                self.loading.start()
            except KeyboardInterrupt:
                self.stop()
            
    
    def stop(self):
        if(self.hasStarted):
            self.loading.terminate()
            self.loading.join()
            print('Done'+' '*(max(0,(len(self.message)-2+self.animType*3))))
            self.hasStarted = False
            self.loading = None
    
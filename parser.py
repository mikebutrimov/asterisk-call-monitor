import sys

logfile = 'ariserver.log'
logs = {}

#class for log record 
#contains such very very usefull information as
# - from number
# - number, which was called
# - number, which was connected with
# - number of times such call does exist
# - maybe will be sutable for later use with different reports

class logRecord (object):
    def __init__(self,f,t,e):
        """
        f - from number
        t - to number
        e - end number
        """
        self.key = (f,t,e)
        self.f = f
        self.t = t
        self.e = e
        self.count = 1
    
    def inc(self):
        self.count += 1
     
    def getRecord(self):
        return [self.count, self.f, self.t, self.e]



#factory for create instances
def factory(f,t,e):
    if f and t and e:
        if (f,t,e) in logs:
            logs[(f,t,e)].inc()
        else:
            logs[(f,t,e)] = logRecord(f,t,e)



def feedLogs(logfile):
    with open(logfile, 'r') as f:
        for line in f:
            buf = line.split()
            if len(buf) == 4:
                d = buf[1].strip()
                if d == '>':
                    f = buf[0].strip()
                    t = buf[2].strip()
                    e = buf[3].strip()
                    factory(f,t,e)
            

def parseLogs(logs):
    for k,v in logs.items():
        print ('%s %s'%(v.count,v.getRecord()))





feedLogs(logfile)
parseLogs(logs)


#print len(logs)

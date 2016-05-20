#log module, supposed to act like an singleton
#some constants, like file io handlers

logfile = 'ariserver.log'
#Log records storage.
#it is a dict. Plan A is:
#before delete a device 
#ohh, when i write this comment, i suddenly
#realized that i don't need every single piece 
#of this sheeeeet.
#All i need is to dump a log record in the file
#when device is deleted from device storage
 

with open(logfile, 'a') as logFile:
    logFile.write('________________________________________\n')


def putRecord(logrecord):
    with open(logfile, 'a') as logFile:
        logFile.write('%s %s %s %s \n'%(logrecord))



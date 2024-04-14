from subprocess import Popen, PIPE, STDOUT
import time
import telnetlib
import serial

ser = serial.Serial("/dev/serial/port1", 115200)


# Telnetstuff
host = 'localhost'
port = 4444

tn = telnetlib.Telnet(host, port)

def tnwrite(cmd):
    tn.write(b""+cmd+"\n")

def tnread():
    return tn.read_very_eager()

# Commands for on off
cmdoff = f'sudo uhubctl -a off -p 1-5 -r 5'
cmdon = f'sudo uhubctl -a on -p 1-5'

# Uses uhubctl to reset the target
def sendUhubctlCmd(cmd):
    with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True) as process:
        # Wait for the command to complete and collect its output
        stdout, stderr = process.communicate()
        # Optionally, you can check the exit code and print the output
        if process.returncode == 0:
            print('Command succeeded:')
            print(stdout)
        else:
            print('Command failed:')
            print(stderr)

# Resets USB
def cycleUSB():
    sendUhubctlCmd(cmdoff)
    time.sleep(5)
    sendUhubctlCmd(cmdon)
    time.sleep(2)

def toggleReset():
    ser.write(b"2")
    time.sleep(2)

def startDev():
    ser.write(b"1")

def stopDev():
    ser.write(b"0")

def calcAddress(addr, val):
     return  hex(int(addr, 16) + int(val, 16))[2:].zfill(8)

def multAddPart(val, i):
    return hex(int(val, 16) * i)[2:].zfill(5)

def divHex(a, b):
    return int(int(a, 16) / int(b, 16))

def bcmd(c, a="", b=""):
    sp1 = "" if a == "" else " "
    sp2 = "" if b == "" else " "
    return c + sp1 + a + sp2 + b + ";"

def getAddressset(base):
    return [
        calcAddress(base,  '0x00'),
        calcAddress(base,  '0x04'),
        calcAddress(base,  '0x08'),
        calcAddress(base,  '0x0C'),
        calcAddress(base,  '0x10')
    ]

def makeNextCommands(addressset):
    return [
        bcmd('mww', '0x'+addressset[0], '0x20002104'),
        bcmd('mww', '0x'+addressset[1], '0x2208230C'),
        bcmd('mww', '0x'+addressset[2], '0x68006809'),
        bcmd('mww', '0x'+addressset[3], '0x68126818'),
        bcmd('mww', '0x'+addressset[4], '0xFFFFFFFF')
    ]

def sendCmd(cmd):
    tnwrite(cmd)

def prepCmds(c):
    cmds = [
        bcmd('mww', '0xe000ed08', '0x20000000'),
        bcmd('mww', '0x20000008', '0x20000021')
    ]
    for i in range(0, len(c)):
        cmds.append(c[i])
    cmds.append(bcmd('mww', '0xe000ed04', '0x80000000'))
    cmds.append(bcmd('halt'))
    cmds.append(bcmd('reg','r0'))
    cmds.append(bcmd('reg','r1'))
    cmds.append(bcmd('reg','r2'))
    cmds.append(bcmd('reg','r3'))
    return cmds
    
def extract():
    a = '0x20000000'
    b = '0x10'
    # 8192 *  16 Byte ( 4 Words == 8 Halfwords == 8 * 2 Byte == 16 Byte)
    # 131072Byte / 16Byte 
    # 128kb / 16kb per round
    cycles = divHex('0x20000', b)
    for i in range(1, cycles):
        c = multAddPart(b, i)
        d = calcAddress(a, c)
        f = getAddressset(d)
        g = makeNextCommands(f)
        h = prepCmds(g)
        for i in range(0, len(h)):
            sendCmd(h[i])
        print(tnread())
        #cycleUSB()
        toggleReset()
        
    
extract()

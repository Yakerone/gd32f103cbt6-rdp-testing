import sys

def clearFile(t):
    with open(t, "r") as fl:
        cntnt = fl.read()
        rows = cntnt.split("\n")
        if len(rows) > 1:
            octets = []
            for i in range(0, len(rows)):
                n = rows[i].split(" ")
                for j in range(0, len(n)):
                    octets.append(n[i])
            return octets
        else:
            return cntnt.split(" ")

def rev(bin):
    rT = ""
    for i in range(0, len(bin)):
        rT = bin[i] + rT
    return rT

def inv(bin):
    rT = ""
    for i in range(0, len(bin)):
        a = "0"
        if bin[i] == "0":
            a = "1"
        rT += a
    return rT

def h2hb(h):
    if h[1] == "x" or h[1] == "X":
        h = h[2:]
    r = ""
    for i in range(0, int(len(h)/2)):
        k = i * 2
        r += h[k:k+2]
        if i < int(len(h)/2) - 1:
            r += " "
    return r.split(" ")

def h2hhlfw(h):
    if h[1] == "x" or h[1] == "X":
        h = h[2:]
    r = ""
    for i in range(0, int(len(h)/4)):
        k = i * 4
        r += h[k:k+4]
        if i < int(len(h)/4) - 1:
            r += " "
    return r.split(" ")

def h2hw(h):
    if h[1] == "x" or h[1] == "X":
        h = h[2:]
    r = ""
    for i in range(0, int(len(h)/8)):
        k = i * 8
        r += h[k:k+8]
        if i < int(len(h)/8) - 1:
            r += " "
    return r.split(" ")

def hb2bin8(hb):
    r = ""
    for i in range(0, len(hb)):
        r += bin(int(hb[i], 16))[2:].zfill(8)
        if i < len(hb) - 1:
            r += " "
    return r.split()

def hhlfw2bin16(hb):
    r = ""
    for i in range(0, len(hb)):
        r += bin(int(hb[i], 16))[2:].zfill(16)
        if i < len(hb) - 1:
            r += " "
    return r.split()

def hw2bin32(hb):
    r = ""
    for i in range(0, len(hb)):
        r += bin(int(hb[i], 16))[2:].zfill(32)
        if i < len(hb) - 1:
            r += " "
    return r.split()

def revBinBytes(binbytes):
    rT = ""
    for i in range(0, len(binbytes)):
        rT += str(rev(binbytes[i]))
        if i < len(binbytes) - 1:
            rT += " "
    return rT.split(" ")

def invBinHlfw(binhlfw):
    rT = ""
    for i in range(0, len(binhlfw)):
        rT += switchHbInHhlfw(binhlfw[i])
        if i < len(binhlfw) - 1:
            rT += " "
    return rT.split(" ")

def bb2hb(bb):
    rT = ""
    for i in range(0, len(bb)):
        rT += hex(int(bb[i],2))[2:]
        if i < len(bb) - 1:
            rT += " "
    return rT.split(" ")

def hb2h(hb):
    rT = ""
    for i in range(0, len(hb)):
        rT += ""+hb[i]
    return rT

def hb2hInvW(hb):
    rT = ""
    for i in range(0, len(hb)):
        rT = ""+hb[i] + rT
    return rT

def switchHbInHhlfw(hhlfw):
    return  hhlfw[8:16:] + "" + hhlfw[0:8]

def xor(val):
    rT = ""
    l = int(val, 16) ^ int('FFFFFFFF',16)
    return hex(l)[2:]

def pf(octets):
    r = ""
    for i in range(0, len(octets)):
        #a = "0x1a2b3c4d"
        #a = "0x11223344"
        b = h2hb(octets[i])
        c = hb2bin8(b)
        d = revBinBytes(c)
        e = bb2hb(d)
        f = hb2h(e)
        g = h2hhlfw(f)
        h = hhlfw2bin16(g)
        ii = invBinHlfw(h)
        j = bb2hb(ii)
        p = hb2hInvW(j)
        s = hex(bin(int(p, 16))[2:].zfill(32))[2:]
        t = xor(s)
        r += t
        if i < len(octets) - 1:
            r += " "
    return r

a = sys.argv[1]
r = ""
if a != "":
    r = clearFile(a)
    print(pf(r)) 
  


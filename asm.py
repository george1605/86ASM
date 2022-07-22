import sys

if len(sys.argv) < 2:
    raise RuntimeError("Expected <filename>")

inp = open(sys.argv[1], "r")
outp = open("output.bin", "wb")
regs = {"EAX":0, "ECX":1, "EDX":2, "EBX":3, "ESP":4, "EBP":5}

def toBytes(str0, off):
    return bytes([int(str0) + off])

def toBytesOp(opcode, off):
    return bytes([int(regs[opcode]) + off])

def toBytesAddr(x):
    byt = []
    while x:
        byt.append(x % 256)
        x = x // 256
    return bytes(byt)

def lineasm(line : str):
    op = line.split()
    if op[0] == "MOV":
        y = toBytes(regs[op[1]], 0xb8)
        outp.write(y)
        outp.write(toBytes(op[2], 0))
    if op[0] == "RET":
        outp.write(bytes(0xc3))
    if op[0] == "XOR":
        if op[1] == "AL":
            outp.write(bytes([0x34]))
        else:
            outp.write(bytes([0x31]))
    if op[0] == "PUSH":
        if op[1] in regs:
            x = regs[op[1]]
            outp.write(bytes([0x50 + x]))
    if op[0] == "POP":
        if op[1] in regs:
            x = regs[op[1]]
            outp.write(bytes([0x58 + x]))
    if op[0] == "MEMW":
        outp.write(bytes([0xa3]))
        x = int(op[1], 16)
        outp.write(toBytesAddr(x))
        

lines = inp.readlines()
for line in lines:
    lineasm(line)
outp.close()

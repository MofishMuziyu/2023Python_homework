import numpy as np
icode = 0
ifun = 0
rA =  0
rB =  0
valC = 0
valP = 0
Register = [0]*15           ### 十五个寄存器
Opcode_trans = {            # ## opcode翻译指令
    "0": ["halt"],
    "1": ["nop"],
    "2": ["rrmovq", "cmovle", "cmovl", "cmove", "cmovne", "cmovge", "cmovg"],
    "3": ["irmovq"],
    "4": ["rmmovq"],
    "5": ["mrmovq"],
    "6": ["addq", "subq", "andq", "xorq"],
    "7": ["jmp", "jle", "jl", "je", "jne", "jg"],
    "8": ["call"],
    "9": ["ret"],
    "A": ["pushq"],
    "B": ["popq"]
}
op_length = {
    '00': 1,'10':1,'20':2,'21':2,'22':2,'23':2,'24':2,'25':2,'26':2,
    '30':10,'40':10,'50':10,
    '71':9,'80':9,
    '70':9,'72':9,'73':9,'74':9,'75':9,'76':9,
    '60':2,'61':2,'62':2,'63':2,
    '90':1,
    'A0':2,
    'B0':2
}

op_list = op_length.keys()
PC = 0                 # ## PC地址
IMem=['10']*1000000        # ##指令存储器
Mem = [0]*1000              # ##数据存储器
Stat = "AOK"       # ##Y86-64异常状态码（AOK，HLT，ADR，INS）
valA = 0           # # #寄存器A的值
valB = 0           # ##寄存器B的值
valE = 0           # ##ALU运算结果，写回值
valM = 0            # ##写回值
dstE = 0            # ##寄存器写回E
dstM = 0            # ##寄存器写回M

aluA = 0
aluB = 0

Cnd = 0             ###跳转指令码
CC = '000'             ###条件码
ZF = 0
SF = 0
OF = 0

file = 'toy3.coe'
instruction = ''
##特殊情况   pushq %rsp ; popq % {A040} {B040}


##解决方法   先压入栈里，再减8 ； 先弹出值给rsp，再加8；



#####数据读入与处理#####Xlinix coe#####
def data_process(file_path):   ##接口，从coe文件中读取并返回成每一条指令的机器码
    global op_list,op_length,Opcode_trans
    result = []
    ins_list=[]
    ins_string = ''
    file  = open(file_path,'r')
    initial_list  = file.readlines()
    initial_list=initial_list[2:]
    length = len(initial_list)
    for i in range(length):
        initial_list[i] = initial_list[i].strip('\n')
        ins_string += initial_list[i]
    #print(initial_list)
    #print(ins_string)
    result.append(ins_string)
    str_long  = len(ins_string)
    while(len(ins_string)):
        ins_list.append(ins_string[:2*op_length[ins_string[:2]]])
        ins_string = ins_string[2*op_length[ins_string[:2]]:]
    result.append(ins_list)

    return result

############初始化指令存储器#############
process_list = data_process(file)
string = process_list[0]
length = len(string)
# print(length)
for i in range (0,length-1,2):
    IMem[i//2] =  string[i:i+2]

# print(IMem)


# ######取址、译码、执行、访存、写回########
def fetch_immprocess():
    global IMem,valP
    result = []
    for i in range(8):
        result.append(IMem[valP + i])
    result.reverse()
    s = ''.join(result)
    s = int(s,16)

    valP = valP + 8
    return s

def fetch(): #没有输出，通过对全局变量的更改来进行操控,取值

    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF,instruction#引入所有全局变量
    icode = IMem[PC][0]
    ifun = IMem[PC][1]

    instruction = Opcode_trans[icode][int(ifun,16)]

    if icode == '2':
        rA = IMem[PC+1][0]
        rB = IMem[PC+1][1]
        valP = PC + 2
    elif icode == '3' and ifun =='0':
        rA = 'f'
        rB = IMem[PC+1][1]
        valP = PC + 2
        valC = fetch_immprocess()
    elif icode=='4' or icode =='5':
        rA = IMem[PC+1][0]
        rB = IMem[PC+1][1]
        valP = PC + 2
        valC = fetch_immprocess()
    elif icode =='6':
        rA = IMem[PC+1][0]
        rB = IMem[PC+1][1]
        valP = PC + 2
    elif icode=='8' or icode == '7':
        valP = PC + 1
        valC = fetch_immprocess()
    elif icode == 'A' or icode =='B':
        rA = IMem[PC+1][0]
        rB = 'f'
        valP = PC + 2
    elif icode == '0':
        Stat = 'HLT'
    else:
        valP = PC + 1

    if type(rA)!= int :
        rA = int(rA,16)
    if  type(rB) != int:
        rB = int(rB,16)
    return True

def decode():  ###解码，主要 用来 读寄存器文件以及读
    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF ,instruction # 引入所有全局变量
    if instruction=='call':
        valB = Register[4]
    elif instruction=='ret':
        valA = Register[4]
        valB = Register[4]
    elif instruction=='pushq':
        valA = Register[rA]
        valB = Register[4]
    elif instruction=='popq':
        valA = Register[rA]
        valB = Register[4]
    elif icode!= 7 and icode !=0 and icode!= 1:
        if rA  < 15:
            valA = Register[rA]
        if rB  < 15:
            valB = Register[rB]
    if instruction == 'halt':
        Stat = 'HLT'
    return True

def execuate():  ###执行
    globals()
    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF,instruction  # 引入所有全局变量
    if icode == '6':
        if instruction == 'addq':
            valE = valA + valB
        elif instruction == 'subq':
            valE = valB - valA
        elif instruction == 'andq':
            valE = valA & valB
        elif instruction == 'xorq':
            valE = valA ^valB
        ZF = 1 if valE == 0 else 0
        SF = 1 if valE < 0 else 0
        OF = ((valA<0) == (valB<0)) & ((valE<0) != (valA<0))
    if instruction == 'rrmovq':
        valE = valA
    elif instruction == 'irmovq':
        valE = valC + 0
    elif instruction == 'rmmovq':
        valE = valB + valC
    elif instruction == 'mrmovq':
        valE = valB + valC
    elif instruction == 'jmp':
        Cnd = 1
    elif instruction=='jle':
        Cnd = (SF^OF)|ZF
    elif instruction == 'je':
        Cnd = ZF
    elif instruction == 'jl':
        Cnd =SF^OF
    elif instruction == 'jne':
        Cnd = 1-ZF
    elif instruction =='jge':
        Cnd = ~(SF^OF)
    elif instruction == 'jg':
        Cnd = ~(SF^OF) & ~ZF
    elif instruction == 'call':
        valE = valB - 8
    elif instruction =='ret':
        valE = valB + 8

    return True

def fetch_mem():####访存阶段,只有写和读的问题，所以只涉及部分指令,pushq ，popq ,call,ret,rmmovq,mrmovq 的问题
    globals()
    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF ,instruction # 引入所有全局变量
    if instruction == 'rmmovq':
        Mem[valE] = valA
    elif instruction =='mrmovq':
        valM = Mem[valE]
    elif instruction == 'pushq':
        Mem[valE] = valA
    elif instruction == 'popq':
        valM = Mem[valA]
    elif instruction == 'call':
        Mem[valE] = valP
    elif instruction =='ret':
        valM = Mem[valE]
    return True

def write_back(): ###写回阶段，更新各寄存器的值
    globals()
    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF ,instruction # 引入所有全局变量
    if icode=='6':
        Register[rB] = valE
    if instruction=='rrmovq':
        Register[rB] = valE
    elif instruction=='irmovq':
        Register[rB] = valE
    elif instruction == 'mrmovq':
        Register[rA] = valM
    elif instruction == 'pushq':
        Register[4] = valE
    elif  instruction == 'popq':
        Register[4] = valE
        Register[rA] =valM
    elif  instruction =='call':
        Register[4] = valE
    elif instruction=='ret':
        Register[4] = valE

    return True

def refresh_PC():  # 更新PC的值，如果没有跳转条件就直接把valP赋给它就好了，如果有的话就把跳转的结果赋给PC
    globals()
    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF ,instruction # 引入所有全局变量
    if icode == '7':
        if Cnd ==1:
            PC = valC
        else:
            PC = valP
    if instruction=='ret':
        PC = valM
    elif instruction == 'call':
        PC = valC
    elif instruction=='jne' and Cnd == 1:
        PC = valC
    else:
        PC = valP

    return True

# 运行函数循环
def cycle():
    globals()

    global icode, ifun, rB, rA, valE, valC, valA, valB, valP, valM, Register, Opcode_trans, \
        op_list, PC, IMem, Mem, Stat, dstE, dstM, aluA, aluB, Cnd, CC, ZF, SF, OF ,instruction # 引入所有全局变量
    PC = PC % 1000
    while(True):
        if Stat == 'HLT':
            print("从1加到100的结果为",end="")
            print(Register[0])
            break
        # fetch()
        # decode()
        # execuate()
        # fetch_mem()
        # write_back()
        # refresh_PC()
        refresh_PC()
        write_back()
        fetch_mem()
        execuate()
        decode()
        fetch()



######主体运行部分#########
cycle()
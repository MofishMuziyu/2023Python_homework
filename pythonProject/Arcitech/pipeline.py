##第九组  李玉良 202102001025
##第九组  陈  爽 202103002004
##第九组  杨玉欣 202102001063

##测试指令集，1到100的累加
"""
irmovq 1 => reg[8]    PC:0
irmovq 1 => reg[6]    PC:10
irmovq 99 => reg[9]   PC:20
xorq 0 0 => 0   反正是将0号寄存器赋值为1  PC:30
addq reg[6] = reg[0] + reg[6]   PC:32
addq reg[8] = reg[6] + reg[8]   PC:34
subq reg[9] = reg[9] - reg[0]   PC:36
jne  0x20=32                    PC:38
halt                            PC:47

"""
##第七次作业，使用阻塞解决了写后读，如从1加到100的过程中，0号寄存器先写后读出现数据依赖，则此时，先阻塞到写回0号寄存器再重新读0号寄存器
## 对于分支指令，首先默认选择顺序执行，如果在执行阶段发现需要跳转，则刷新之前执行的错误的指令，并将需要跳转到的正确的指令赋值给F阶段

##对于结构依赖的判断：有存储器结构依赖和ALU运算单元的结构依赖，因为读写内存只在第四阶段，所以即使是两个相邻指令之间访问同一片内存单元也不会
##有存储器的结构依赖，对于ALU的结构依赖，采取增加ALU运算单元的方法来解决，模拟方法是增设一个ALU的空闲量（类似信号量的思想），同时将ALU部件的通过时间
##改为2delt ，每次通过ALU需要经过两个CLK，ALU空闲量一共有两个，每次有指令进入ALU部件空余量就减小一个，每次有指令从ALU流出就释放一个ALU空余量


##第八次作业，^-^
## 1.增加控制依赖判断：  在第七次作业中已完成
## 2.将控制条件的获得提前，提高性能，在第七次作业中已完成（将）执行阶段的结果进行判断是否跳转，如果需要跳转，则跳转到新的PC，同时刷新F阶段和D阶段的
## 错误流水。（如果是无条件跳转指令，则在D阶段之后就可以直接跳转，也已完成）


##使用Y86指令集
Opcode_trans = {            # ## opcode翻译指令
    "0": ["halt"],
    "1": ["nop"],
    "2": ["rrmovq", "cmovle", "cmovl", "cmove", "cmovne", "cmovge", "cmovg"],
    "3": ["irmovq"],
    "4": ["rmmovq"],
    "5": ["mrmovq"],
    "6": ["addq", "subq", "andq", "xorq","mul","div"],
    "7": ["jmp", "jle", "jl", "je", "jne", "jg"],
    "8": ["call"],
    "9": ["ret"],
    "a": ["pushq"],
    "b": ["popq"]
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
'''
args = {
stat = "AOK"       # ##Y86-64异常状态码（AOK，HLT，ADR，INS）
icode = 0
ifun = 0
instruction = ''
PC = 0
rA =  0
rB =  0
valC = 0           ## 附带的立即数
valP = 0

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
}
'''
Reg = [0]*16 ##5号寄存器是零寄存器？？
Imem = ['10']*1000 ##需要填充指令
Dmem = ['00']*65536

class pipeline():
    def __init__(self,Imem,Dmem,reg):
        ##取指，译码，执行，访存，写回    参数字典
        self.Imem = Imem
        self.Dmem = Dmem
        self.reg = reg
        self.ZF = 0
        self.SF = 0
        self.OF = 0
        self.ALU_left = 2
        dict_new = {}
        dict_new["icode"] = '0'
        dict_new["ifun"] = '0'
        dict_new["stat"] = "AOK"
        dict_new["PC"] = 0
        dict_new["instruction"] = ""
        dict_new["rA"] = 0
        dict_new["rB"] = 0
        dict_new["valC"] = 0
        dict_new["valP"] = 0
        dict_new["valA"] = 0
        dict_new["valB"] = 0
        dict_new["valE"] = 0
        dict_new["valM"] = 0
        dict_new["dstE"] = 0
        dict_new["dstM"] = 0
        dict_new["aluA"] = 0
        dict_new["aluB"] = 0
        dict_new["Cnd"] = 0
        dict_new["CC"] = '000'
        dict_new["ZF"] = 0
        dict_new["SF"] = 0
        dict_new["OF"] = 0

        self.argsF = dict_new.copy()
        self.argsD = dict_new.copy()
        self.argsE = dict_new.copy()
        self.argsM = dict_new.copy()
        self.argsW = dict_new.copy()


    # def args_init(self):
    #     self.argsF["icode"] = '0'
    #     self.argsF["ifun"] = '0'
    #     self.argsF["stat"] = "AOK"
    #     self.argsF["PC"] = 0
    #     self.argsF["instruction"] = ""
    #     self.argsF["rA"] = 0
    #     self.argsF["rB"] = 0
    #     self.argsF["valC"] = 0
    #     self.argsF["valP"] = 0
    #     self.argsF["valA"] = 0
    #     self.argsF["valB"] = 0
    #     self.argsF["valE"] = 0
    #     self.argsF["valM"] = 0
    #     self.argsF["dstE"] = 0
    #     self.argsF["dstM"] = 0
    #     self.argsF["aluA"] = 0
    #     self.argsF["aluB"] = 0
    #     self.argsF["Cnd"] = 0
    #     self.argsF["CC"] = '000'
    #     self.argsF["ZF"] = 0
    #     self.argsF["SF"] = 0
    #     self.argsF["OF"] = 0
    #     self.argsD = self.argsF
    #     self.argsE = self.argsF
    #     self.argsM = self.argsF
    #     self.argsW = self.argsF

    def predict_flush(self,number):
        dict_new ={}
        dict_new["icode"] = '0'
        dict_new["ifun"] = '0'
        dict_new["stat"] = "AOK"
        dict_new["PC"] = 0
        dict_new["instruction"] = ""
        dict_new["rA"] = 0
        dict_new["rB"] = 0
        dict_new["valC"] = 0
        dict_new["valP"] = 0
        dict_new["valA"] = 0
        dict_new["valB"] = 0
        dict_new["valE"] = 0
        dict_new["valM"] = 0
        dict_new["dstE"] = 0
        dict_new["dstM"] = 0
        dict_new["aluA"] = 0
        dict_new["aluB"] = 0
        dict_new["Cnd"] = 0
        dict_new["CC"] = '000'
        dict_new["ZF"] = 0
        dict_new["SF"] = 0
        dict_new["OF"] = 0

        if number==1:
            self.argsF = dict_new.copy()
        elif number==2:
            self.argsD = dict_new.copy()
        elif number==3:
            self.argsE = dict_new.copy()
        elif number == 4:
            self.argsM = dict_new.copy()
        elif number == 5:
            self.argsW = dict_new.copy()


    def fetch_imm(self,valP):##取立即数
        result = []
        for i in range(8):
            result.append(self.Imem[valP + i])
        result.reverse()
        s = ''.join(result)
        s = int(s, 16)
        ##valP = valP + 8
        return s
    def fetch_mem(self,addr,number):
        result_string = ""
        for i in range(number):
            result_string += self.Dmem[addr + i]
        result = int(result_string,16)
        return result
    def store_mem(self,addr,value):
        string = hex(value & 0xffffffff)[2:]
        string = "00000000" + string
        string = string[-8:]
        for i in range(4):
            self.Dmem[addr+i] = string[2*i:2*i+2]
        return True
    def __fetch__(self):
        PC = self.argsF["PC"]
        icode = self.Imem[PC][0]
        ifun = self.Imem[PC][1]
        instruction = Opcode_trans[icode][int(ifun, 16)]

        rA = self.argsF["rA"]
        rB = self.argsF["rB"]
        valP = self.argsF["valP"]
        valC = self.argsF["valC"]
        stat = self.argsF["stat"]

        if icode == '2':
            rA = self.Imem[PC + 1][0]
            rB = self.Imem[PC + 1][1]
            valP = PC + 2
        elif icode == '3' and ifun == '0':
            rA = 'f'
            rB = self.Imem[PC + 1][1]
            valP = PC + 2
            valC = self.fetch_imm(valP)
            valP =valP + 8
        elif icode == '4' or icode == '5':
            rA = self.Imem[PC + 1][0]
            rB = self.Imem[PC + 1][1]
            valP = PC + 2
            valC = self.fetch_imm(valP)
            valP = valP + 8
        elif icode == '6':
            rA = self.Imem[PC + 1][0]
            rB = self.Imem[PC + 1][1]
            valP = PC + 2
        elif icode == '8' or icode == '7':
            valP = PC + 1
            valC = self.fetch_imm(valP)
            valP = valP + 8
        elif icode == 'a' or icode == 'b':
            rA = self.Imem[PC + 1][0]
            rB = 'f'
            valP = PC + 2
        elif icode == '0':
            stat = 'HLT'
        else:
            valP = PC + 1

        if type(rA) != int:
            rA = int(rA, 16)
        if type(rB) != int:
            rB = int(rB, 16)
        self.argsF["rA"] = rA
        self.argsF["rB"] = rB
        self.argsF["stat"] = stat
        self.argsF["valP"] = valP
        self.argsF["valC"] = valC
        self.argsF["icode"] = icode
        self.argsF["ifun"] = ifun
        self.argsF["instruction"] = instruction

    def __decode__(self):
        instruction = self.argsD["instruction"]
        valA = self.argsD["valA"]
        valB = self.argsD["valB"]
        icode = self.argsD["icode"]
        ifun = self.argsD["ifun"]
        rA = self.argsD["rA"]
        rB = self.argsD["rB"]
        stat = self.argsD["stat"]

        if instruction == 'call':
            valB = self.reg[4]
        elif instruction == 'ret':
            valA = self.reg[4]
            valB = self.reg[4]
        elif instruction == 'pushq':
            valA = self.reg[rA]
            valB = self.reg[4]
        elif instruction == 'popq':
            valA = self.reg[rA]
            valB = self.reg[4]
        elif icode != '7' and icode != '0' and icode != '1':
            if rA < 15:
                valA = self.reg[rA]
            if rB < 15:
                valB = self.reg[rB]
        if instruction == 'halt':
            stat = 'HLT'
        self.argsD["instruction"] = instruction
        self.argsD["valA"] = valA
        self.argsD["valB"] = valB
        self.argsD["icode"] = icode
        self.argsD["ifun"] = ifun
        self.argsD["rA"] = rA
        self.argsD["rB"] = rB
        self.argsD["stat"] = stat
        return True

    def __execuate__(self): ##单dt的
        icode = self.argsE["icode"]
        valA = self.argsE["valA"]
        valB = self.argsE["valB"]
        instruction = self.argsE["instruction"]
        valE = self.argsE["valE"]
        ZF = self.ZF
        SF = self.SF
        OF = self.OF
        valC = self.argsE["valC"]
        Cnd = self.argsE["Cnd"]

        if icode == '6':
            if instruction == 'addq':
                valE = valA + valB

            elif instruction == 'subq':
                valE = valB - valA

            elif instruction == 'andq':
                valE = valA & valB

            elif instruction == 'xorq':
                valE = valA ^ valB +1  ##先修改之后再跑一遍是不是能行,可以，这里意思改为同或

            elif instruction == "mul":
                valE = valA * valB

            elif instruction == "div":
                valE = valA / valB

            self.ZF = 1 if valE == 0 else 0
            self.SF = 1 if valE < 0 else 0
            self.OF = ((valA < 0) == (valB < 0)) & ((valE < 0) != (valA < 0))
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
        elif instruction == 'jle':
            Cnd = (SF ^ OF) | ZF
        elif instruction == 'je':
            Cnd = ZF
        elif instruction == 'jl':
            Cnd = SF ^ OF
        elif instruction == 'jne':
            Cnd = 1 - ZF
        elif instruction == 'jge':
            Cnd = ~(SF ^ OF)
        elif instruction == 'jg':
            Cnd = ~(SF ^ OF) & ~ZF
        elif instruction == 'call':
            valE = valB - 4
        elif instruction == 'ret':
            valE = valB + 4
        elif instruction == 'push':
            valE = valB
        elif instruction == 'pop':
            valE = valB
        self.argsE["icode"] =icode
        self.argsE["valA"] = valA
        self.argsE["valB"] = valB
        self.argsE["instruction"] = instruction
        self.argsE["valE"] = valE
        self.argsE["ZF"] = ZF
        self.argsE["SF"] = SF
        self.argsE["OF"] = OF
        self.argsE["valC"] = valC
        self.argsE["Cnd"] = Cnd

    def __fetch_mem__(self):##Mem要改成字节寻址 32位
        instruction = self.argsM["instruction"]
        valA = self.argsM["valA"]
        valE = self.argsM["valE"]
        valP = self.argsM["valP"]
        valM = self.argsM["valM"]
        if instruction == 'rmmovq':
            self.store_mem(valE,valA)
            ##Mem[valE] = valA
        elif instruction == 'mrmovq':
            valM = self.fetch_mem(valE,4)
            ##valM = Mem[valE]
        elif instruction == 'pushq':
            self.store_mem(valE, valA)
            #Mem[valE] = valA
        elif instruction == 'popq':
            valM = self.fetch_mem(valE, 4)
            #valM = Mem[valA]
        elif instruction == 'call':
            self.store_mem(valE, valP)
            #Mem[valE] = valP
        elif instruction == 'ret':
            valM = self.fetch_mem(valE,4)
            #valM = Mem[valE]

        self.argsM["instruction"] = instruction
        self.argsM["valA"] = valA
        self.argsM["valE"] = valE
        self.argsM["valP"] = valP
        self.argsM["valM"] = valM

    def __write_back__(self):##包括写回寄存器和更新PC
        instruction = self.argsW["instruction"]
        PC = self.argsW["PC"]
        icode = self.argsW["icode"]
        ifun = self.argsW["ifun"]
        rA = self.argsW["rA"]
        rB = self.argsW["rB"]
        valE = self.argsW["valE"]
        valM = self.argsW["valM"]
        valC = self.argsW["valC"]
        valP = self.argsW["valP"]
        Cnd = self.argsW["Cnd"]


        if icode == '6':
            self.reg[rB] = valE
        if instruction == 'rrmovq':
            self.reg[rB] = valE
        elif instruction == 'irmovq':
            self.reg[rB] = valE
        elif instruction == 'mrmovq':
            self.reg[rA] = valM
        elif instruction == 'pushq':
            self.reg[4] = valE
        elif instruction == 'popq':
            self.reg[4] = valE
            self.reg[rA] = valM
        elif instruction == 'call':
            self.reg[4] = valE
        elif instruction == 'ret':
            self.reg[4] = valE

        ##彻底计算出PC的值，因为此时Cnd已经计算出了
        # if icode == '7':
        #     if Cnd == 1:
        #         PC = valC
        #     else:
        #         PC = valP
        # if instruction == 'ret':
        #     PC = valM
        # elif instruction == 'call':
        #     PC = valC
        # else:
        #     PC = valP

        self.argsW["instruction"] = instruction
        self.argsW["PC"] = PC
        self.argsW["icode"] = icode
        self.argsW["ifun"] = ifun
        self.argsW["rA"] = rA
        self.argsW["rB"] =rB
        self.argsW["valE"] = valE
        self.argsW["valM"] = valM
        self.argsW["valC"] =valC
        self.argsW["valP"] =valP
        self.argsW["Cnd"] =Cnd


    def CLK(self):

        ## 执行阶段之后会有跳转指令的结果，可以与D阶段的PC比较，如果不一致，则清空当前的FD,把
        ## 新的PC赋给F阶段重新执行
        newPC = self.argsF["valP"]  ##顺序执行的下一条指令地址,从E阶段的结果中判断是否需要PC变化，需要则暂停两下然后把新的PC赋给F
        ## 如果此时还没到E阶段，会无事发生，到了E阶段，如果符合跳转条件，那么需要将中间的FD都flush掉然后重新执行F,如果是需要valM的话就
        ## 需要再往后一个阶段
        ## 先判断是否跳转再判断阻塞，因为一旦跳转判断错误的话，阻塞也就没必要的了，指令都是假的
        flushe = 0
        flushm = 0
        if self.argsE["icode"] == "7" and self.argsE["Cnd"] == 1:
            flushe = 1
            newPC = self.argsE["valC"]
        elif self.argsE["instruction"] == "call":
            flushe = 1
            newPC = self.argsE["valC"]
        elif self.argsM["instruction"] == "ret":
            flushm = 1
            newPC = self.argsM["valM"]
        if flushe == 1:
            self.predict_flush(1)
            self.predict_flush(2)
        if flushm == 1:
            self.predict_flush(1)
            self.predict_flush(2)
            self.predict_flush(3)



        # F阶段结束之后就已知需要读的寄存器号，此时如果阶段的rArB或是存储器地址
        # 此时有三种情况的写后读：W阶段无所谓
        # D阶段已知要写，   F阶段下一步就要读 ： 此时F不能传到D，要阻塞到当前的D传送到W阶段且执行
        # E阶段要写的寄存器，F阶段下一步要读 ：同理D
        # M阶段要写的寄存器，F阶段下一步要读 ：只有pop会写寄存器A，
        clogd = 0
        cloge = 0
        clogm = 0
        rA = self.argsF["rA"]##要读的寄存器
        rB = self.argsF["rB"]##要读的寄存器
        ## D阶段和F阶段的数据依赖了
        if self.argsD["instruction"]=="rrmovq" and (self.argsD["rB"]==rA or self.argsD["rB"]==rB) :
            clogd = 1
        elif self.argsD["instruction"]=="irmovq" and (self.argsD["rB"]==rA or self.argsD["rB"]==rB) :
            clogd = 1
        elif self.argsD["instruction"]=="mrmovq" and (self.argsD["rA"]==rA or self.argsD["rA"]==rB) :
            clogd = 1
        elif self.argsD["icode"] == "6" and  (self.argsD["rB"] == rA or self.argsD["rB"]==rB) :
            clogd = 1
        elif self.argsD["icode"] == "2" and self.argsD["Cnd"] == 1 and (self.argsD["rB"] == rA or self.argsD["rB"]==rB):
            clogd = 1
        ## E阶段即将写入的寄存器与F阶段的冲突了
        if self.argsE["instruction"]=="rrmovq" and (self.argsE["rB"]==rA or self.argsE["rB"]==rB) :
            cloge = 1
        elif self.argsE["instruction"]=="irmovq" and (self.argsE["rB"]==rA or self.argsE["rB"]==rB) :
            cloge = 1
        elif self.argsE["instruction"]=="mrmovq" and (self.argsE["rA"]==rA or self.argsE["rA"]==rB) :
            cloge = 1
        elif self.argsE["icode"] == "6" and  (self.argsE["rB"] == rA or self.argsE["rB"]==rB) :
            cloge = 1
        elif self.argsE["icode"] == "2" and self.argsE["Cnd"] == 1 and (self.argsE["rB"] == rA or self.argsE["rB"]==rB):
            cloge = 1
        ## M阶段如果是pop或者push的时候再看是否有数据依赖
        if self.argsM["icode"] == "b" and (self.argsM["rA"]==rA or self.argsM["rA"]==rB):
            clogm = 1



        # ####内存的写后读，如果E阶段只有一个周期则不会存在该问题
        # addr = self.argsE["valE"]    ##要读的地址
        if clogd == 1: ##先分析D阶段会不会冲突
            self.argsT = self.argsW.copy()
            self.argsW = self.argsM.copy()
            self.argsM = self.argsE.copy()
            self.argsE = self.argsD.copy()
            self.predict_flush(2)

            self.__write_back__()
            self.__fetch_mem__()
            self.__execuate__()


            self.argsW = self.argsM.copy()
            self.argsM = self.argsE.copy()
            self.argsE = self.argsD.copy()
            self.__write_back__()
            self.__fetch_mem__()
            self.__execuate__()

            self.argsW = self.argsM.copy()
            self.argsM = self.argsE.copy()
            self.__write_back__()
            self.__fetch_mem__()
            self.__execuate__()
            cloge = 0
            clogm = 0


        if cloge == 1: ##手动把后面三个周期执行一下，前面不变
            self.argsT = self.argsW.copy()
            self.argsW = self.argsM.copy()
            self.argsM = self.argsE.copy()
            self.argsE = self.argsD.copy()
            self.predict_flush(2) ##D阶段被移走了，所以直接清空当前的D

            self.__write_back__()
            self.__fetch_mem__()
            self.__execuate__()


            self.argsW = self.argsM.copy()
            self.argsM = self.argsE.copy()
            self.argsE = self.argsD.copy()

            self.__write_back__() ## 至此已经写回了冲突的寄存器
            self.__fetch_mem__()
            self.__execuate__()
            clogm = 0

        if clogm == 1:
            self.argsT = self.argsW.copy()
            self.argsW = self.argsM.copy()
            self.argsM = self.argsE.copy()
            self.argsE = self.argsD.copy()
            self.predict_flush(2) ##D阶段被移走了，所以直接清空当前的D

            self.__write_back__()
            self.__fetch_mem__()
            self.__execuate__()


        self.argsT = self.argsW.copy()
        self.argsW = self.argsM.copy()
        if self.argsE["icode"] == '6':
            self.argsM = self.argsE.copy()
            if self.ALU_left<2:
                self.ALU_left += 1
        else:##其他情况的E阶段正常向M阶段流
            self.argsM = self.argsE.copy()
        if self.argsD["icode"] == '6' : ##步入执行阶段占用一个ALU资源
            if self.ALU_left > 0:##如果有剩余的ALU
                self.argsE = self.argsD.copy()
                self.ALU_left -= 1
                self.argsD = self.argsF.copy()
                if self.argsF["stat"] != "HLT":
                    self.predict_flush(1)
                    self.argsF["PC"] = newPC
            ##如果没有剩余的ALU，则什么也不做，暂停后面的流水


        else:##不是ALU运算指令的话正常执行

            self.argsE = self.argsD.copy()
            self.argsD = self.argsF.copy()

            if self.argsF["stat"] != "HLT":
                self.predict_flush(1)
                self.argsF["PC"] = newPC


    def cycle(self):
        ##先init  args
        i = 0
        while self.argsW["stat"] != "HLT":
            self.__write_back__()
            self.__fetch_mem__()
            self.__execuate__()
            self.__decode__()
            self.__fetch__()
            self.CLK() ##是一拍，交换数据，阻塞以及分支预测失败后的清理，结构依赖怎么做？？
            i+=1
            if i==595:
                continue
        Reg = self.reg
        return Reg

## 6109 从九号寄存器减去0号寄存器的值，作为累加一次的值
Imem0=[
    30,"f8","01",00,00,00,00,00,00,00,
    30,"f6","01",00,00,00,00,00,00,00,
    30,"f9",63,00,00,00,00,00,00,00,
    63,00,
    60,"06",
    60,68,
    61,"09",
    74,20,
    00,00,00,00,00,00,00,00
]
##测试指令集包括
"""
irmovq 1 => reg[8]    PC:0
irmovq 1 => reg[6]    PC:10
irmovq 99 => reg[9]   PC:20
xorq 0 0 => 0   反正是将0号寄存器赋值为1  PC:30
addq reg[6] = reg[0] + reg[6]   PC:32
addq reg[8] = reg[6] + reg[8]   PC:34
subq reg[9] = reg[9] - reg[0]   PC:36
jne  0x20=32                    PC:38
halt                            PC:47

"""
##从1加到100
for i in range(len(Imem0)):
    Imem[i]=str(Imem0[i])
    Imem[i] = ("00" + Imem[i])[-2:]
pipeline0=pipeline(Imem,Dmem,Reg)

reg_result = pipeline0.cycle()
print(reg_result) ##计算出的寄存器结果


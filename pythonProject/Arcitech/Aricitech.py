###  编码指令集 ###
"""
halt 结束标识
nop  空指令
整数运算 ： add,sub,mul,divint
浮点运算 ： addf,subf,mulf,divf       未完成
条件分支 ： jle,jl,je,jge,jg          需要pop和push
无条件分支： jr                       需要pop和push
读写指令： laodm,loadi,store
数据传送指令，mem to reg, imm to reg,reg to mem，reg to reg
逻辑运算： and,or,xor,not             reg op reg , reg op imm
左移右移（右移的逻辑与算术）： sal,sar,shr  移位
函数调用与返回： call,return           pop and push


所以需要定义的微操作有：  均已完成
寄存器加， 移位， 逻辑运算（与非和非），取反
压栈弹栈，读写内存，加载立即数

作业5： 完成了微操作的Python描述，因为后续要对所有指令编码，设计指令格式，形成
三级流水线，故不再使用Python为每个指令单独描述，在此仅描述一下大概组成，不必再编码指令单独的函数：
add(reg+reg),sub(add+取反),mul(add+sub+移位)，divint(add,sub,移位)
浮点运算暂未做
条件分支（条件码寄存器，对PC程序计数器的修改）
无条件分支（PC寄存器）
读写指令（作为微操作已实现）
逻辑运算（与，非微操作已实现）
左移右移（作为微操作实现）
函数调用和返回（利用pop，push保存PC和必要寄存器，再利用jr跳转，返回时同理，微操作已实现）
"""
###9.25寄存器编码
'''
r0 恒0寄存器
r1 rax 存储函数返回值
r2 rbx 通用
r3 rcx 通用
r4 PSW  Cin， Overflow， Zero， Negative, Signal, State
    0x00000abc: a=>进位溢出 ， b=>正负零  ,c=>状态码
r5 logic
r6 
r7 
r8 rsp栈指针寄存器,指向当前的栈顶
r9  通用寄存器10-15，
A   函数调用
B
C
D
E
F
'''
logic_reg = 5
##9.17需要描述的内容：
## 寄存器16个32位寄存器
## 存储器 32位寻址 32位数据
## 存储器取数到寄存器     load
## 基于寄存器的加法
## 寄存器结果送到存储器   store

##BCD存储需要考虑的问题：
#1.符号位如何存储
#2.终止符号在哪里
#3.一个地址对应一个字节，那么最小应该是8位对齐

##解决方法：将符号位放在最后一位作为结束标志，同时读取的时候，不足八位在
##后面补全一，符号位仍然在最后。 + 号“1100”  - 号“1010”
rsp = 8
##主存内容是一个地址一个字节的数据
dict_bin ={
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}
####定义一些辅助函数#####

class Architech:  ###定义了微操作和一些
    def __init__(self,dmem,imem,reg,PC,PSW,stat):###PSW 012
        self.mem = dmem
        self.reg = reg
        self.imem = imem
        self.PC = PC
        self.PSW = PSW
        self.stat = stat
    def __transfer__(self,hex_string):###十六进制补码字符串转整数数字
        result_int = self.__sign_hex__(hex_string)
        return result_int
    def __transfer_bcd__(self,bcdstring):###这两个函数主要是为了取出的数据都是整数形式
        signal = bcdstring[-1]
        result = int(bcdstring[:-1])
        if signal == 'c':
            result = ~result + 1
        return  result
    def __sign_hex__(self,hex_string):###把十六进制补码表示的字符串转化成整数
        global dict_bin
        bins = dict_bin[hex_string[0]] ##首字母的二进制表示
        binstring = ''
        result = 0
        for i in hex_string:
            binstring += dict_bin[i]
        length = len(binstring)
        if bins[0] == '1':
            binstring = binstring.replace('0','2')
            binstring = binstring.replace('1','0')
            binstring = binstring.replace('2','1')
            result = int(binstring,2)
            result += 1
        elif bins[0]== '0':
            result = int(binstring,2)
        return result
    def __hex_sign__(self,number):##整数转化为十六进制字符串
        string = hex(number & 0xffffffff)[2:]
        return string

    def __addreg__(self,reg_source,reg_des): ##基于寄存器的加法，两个寄存器内的整数可直接加
        if reg_source< 0 or reg_source> 15 or reg_des < 0 or reg_des >15 :
            print("ERROR！寄存器范围溢出！\n")
            return
        self.reg[reg_des] += self.reg[reg_source]
    def __load_imm__(self,reg_number,imm):
        self.reg[reg_number] = imm
    def __store__(self,reg_number,addr): ##寄存器结果送到存储器中的一片连续内存
        if reg_number< 0 or reg_number >15:
            print("ERROR！寄存器范围溢出！\n")
            return
        high = (addr & 0xffff0000) //0x10000
        low  = addr & 0x0000ffff
        hex_data = self.reg[reg_number]
        hex_string = hex(hex_data & 0xffffffff)
        length = len(hex_string)
        mem_list = []
        if length%2 ==1:
            hex_string = '0' + hex_string
            length += 1
        for i in range(0,length,2):
            mem_list.append(hex_string[i:i+2])
        mem_len=len(mem_list)
        row = 0
        col = 0
        while col < mem_len:
            self.mem[high+row][low+col] = mem_list[col]
            col+=1
            if (col+low)>=65536:
                low-=65536
                row+=1
####################  ##第三次作业2&3，新增按不同字节数访问主存###################
    def __fetch_le32__(self, reg_number, addr, number):  ##number代表单次访问字节数,最大支持4字节即32位
        if number > 4 or number < 0:
            print("主存读取格式错误")
            return
        high = (addr & 0xffff0000) // 0x10000
        low = addr & 0x0000ffff
        i = 0
        j = 0
        result_string = ''
        while i < number:
            temp_str = self.mem[high + j][low + i]
            i = i + 1
            if (i + low) >= 65536:
                low = low - 65536
                j += 1
            result_string += temp_str
        hex_result = self.__transfer__(result_string)
        self.reg[reg_number] = hex_result  ##将访存结果写回寄存器，并返回访存值
        return hex_result
    def __fetch_64__(self, reg_number1, reg_number2, addr, number):  ##number >4 小于等于8 64位需要2个reg
        if number > 8 or number < 4:
            print("主存读取格式错误")
            return
        high = (addr & 0xffff0000) // 0x10000
        low = addr & 0x0000ffff
        i = 0
        j = 0
        result_string1 = ''
        result_string2 = ''
        while i < number:
            temp_str = self.mem[high + j][low + i]
            i = i + 1
            if (i + low) >= 65536:
                low = low - 65536
                j += 1

            if i <= 4:
                result_string1 += temp_str
            elif i <= 8:
                result_string2 += temp_str
        hex_result1 = self.__transfer__(result_string1)
        hex_result2 = self.__transfer__(result_string2)
        self.reg[reg_number1] = hex_result1
        self.reg[reg_number2] = hex_result2
        return hex_result1,hex_result2
    def __fetch__bcd__(self, reg_number, addr):  ###最后补位的'f'不会加进去，始终以符号结尾
        flag = 1
        high = (addr & 0xffff0000) // 0x10000
        low = addr & 0x0000ffff
        result_string = ''
        i = 0
        j = 0  ##第i行 第j列
        while flag:
            byte = self.mem[high + i][low + j]
            byte1 = byte[0]
            byte2 = byte[1]
            if byte2 == 'f':
                result_string = byte1 + result_string
                flag = 0
            elif byte2 == 'a' or byte2 == 'c':
                result_string = result_string + byte1
                result_string = byte2 + result_string
                flag = 0
            else:
                result_string = result_string + byte1
                result_string = result_string + byte2
            j += 1
            if (j + low) >= 65536:
                low = low - 65536
                i += 1
        hex_result = self.__transfer_bcd__(result_string)
        self.reg[reg_number] = hex_result
        return hex_result
#################逻辑运算微操作##########################尚未修改条件寄存器
    def __logic_andbit__(self,reg_des,reg_sour):
        logic_result = self.reg[reg_des] & self.reg[reg_sour]
        self.reg[logic_reg] = logic_result
        return logic_result
    def __logic_reversed__(self, reg_number):  ##将寄存器内容取反，十六进制数,按位取反
        data = self.reg[reg_number]
        result = hex(~data)
        self.reg[reg_number] = result
        return result
    def __logic_and__(self,reg_1,reg_2):
        result = bool(self.reg[reg_1] and self.reg[reg_2])
        self.reg[logic_reg] = result
        return result
    def __logic_or__(self,reg_1,reg_2):
        result = bool(self.reg[reg_1] or self.reg[reg_2])
        self.reg[logic_reg] = result
        return result
    def __logic_not__(self,reg_1):
        result = not self.reg[reg_1]
        self.reg[logic_reg] = result
        return result
##################移位微操作#####################需要移位寄存器，暂且用一个通用寄存器
    def __sal__(self,reg_des,sh_bit):#逻辑左移，左移位数
        if sh_bit >= 32:
            self.reg[reg_des] = 0
            return
        elif sh_bit < 0:
            return
        sh_rice = 2**sh_bit
        self.reg[reg_des] *= sh_rice
        return
    def __sar__(self,reg_des,sh_bit):#逻辑右移
        if sh_bit >= 32:
            self.reg[reg_des] = 0
            return
        elif sh_bit < 0:
            return
        sh_rice = 2**sh_bit
        self.reg[reg_des] //= sh_rice
        return
    def __shr__(self,reg_des,sh_bit):#算术右移
        negative = 0
        if hex(self.reg[reg_des])[0]=='-':
            negative = 1

        if sh_bit >= 32:
            self.reg[reg_des] = 0
            return
        elif sh_bit < 0:
            return
        sh_rice = 2**sh_bit
        self.reg[reg_des] //= sh_rice
        if negative==1:
            data = 0xffffffff
            data = data>>(32-sh_bit)<<(32-sh_bit)
            self.reg[reg_des] = self.reg[reg_des] | data
        return
################压栈与弹栈的微操作################需要栈基址寄存器，同时在内存中划分出栈区
    def __push__(self,reg_number):##要压入栈中的内容  寄存器与恢复点,压入之后地址加8
        self.__store__(reg_number, self.reg[rsp])
        addr = self.reg[rsp]
        high = (addr & 0xffff0000) // 0x10000
        low = addr & 0x0000ffff
        low += 8
        while low>=65536:
            low-=65536
            high+=1
        addrnew = high<<16 | low
        self.reg[rsp] = addrnew
    def __pop__(self,reg_number):
        addr = self.reg[rsp]
        high = (addr & 0xffff0000) // 0x10000
        low = addr & 0x0000ffff
        low -= 8
        while low < 0:
            low += 65536
            high -= 1
        addrnew = high << 16 | low
        self.reg[rsp] = addrnew
        self.__fetch_le32__(reg_number,self.reg[rsp],4)
    # def __test1__(self,regload1,regload2_des,addr1,addr2,addr3): ##测试一下9.17作业内容
    #
    #     print("加载操作进行前，第%d个寄存器的值为:%d"%(regload1,self.reg[regload1]))
    #     self.__load__(regload1,addr1)
    #     print("加载操作进行后，第%d个寄存器的值为:%d"%(regload1, self.reg[regload1]))
    #     print("加载操作进行前，第%d个寄存器的值为:%d"%(regload2_des, self.reg[regload2_des]))
    #     self.__load__(regload2_des,addr2)
    #     print("加载操作进行前，第%d个寄存器的值为:%d"%(regload2_des, self.reg[regload2_des]))
    #     self.__addreg__(regload1,regload2_des)##加载两个寄存器，基于寄存器相加
    #     print("基于寄存器相加之后，目的寄存器%d的值为:%d"%(regload2_des,self.reg[regload2_des]))
    #     high = (addr3 & 0xffff0000) //0x10000
    #     low  = addr3 & 0x0000ffff
    #     print("写回操作前，{:#x}的值为%d".format(addr3)%(self.mem[high][low]))
    #     self.__store__(regload2_des,addr3)
    #     print("写回操作后，{:#x}的值为%d".format(addr3)%self.mem[high][low])
    def __test2__(self):
        T = "ffffff"
        op = self.__sign_hex__(T)
        print(op)
        print("666")
        return
##测试部分
# numberlist = [[1]*65536]*65536
icode = 0
ifun = 0
stat = 'AOK'
reg = [0]*16      ##采用十六进制的数作为内容，总共16个register，每个最大32位
reg[0] = 0
dmem = [['00']*65536]*65536 ##32位寻址分成两步寻址，高16位，低16位。否则数组太长，
imem = [['00']*65536]*65536 ##
PSW = -1 ##012小于等于大于零 -1未初始化
PC = 0
isc_base = 0
logic_r = 5
opcode_trans = {
    '0': ["halt"],
    '1': ["nop"],
    '2': ["rrmov"],
    '3': ["loadi"],
    '4': ["loadm"],
    '5': ["store"],
    '6': ["add","sub","mul","divint","and","or","xor","not"],
    '7': ["jr","jmp","jmpr"],
    '8': ["jne","jle","jl","je","jg","jge"],
    '9': ["sal","sar","shr"],
    'a': ["pop","push"],
    'b': ["call"],
    'c': ["return"],
}
opcode_len = {
    '00': 1,'10':1,'20':2,
    '30':6,'40':6,'50':6,
    '60':2,'61':2,'62':2,'63':2,'64':2,'65':2,'66':2,'67':2,
    '70':2,'71':9,'72':2,
    '80':2,'81':2,'82':2,'83':2,'84':2,'85':2,
    '90':2,'91':2,'92':2,
    'a0':2,'a1':2,
    'b0':2,
    'c0':1
}
#mem和reg作为公有的，
def fetch_decode(architech):
    # 输入是PC的值，取出连续的一群指令，断开成指令集，返回需要访问的地址和寄存器号，以及指令类型
    # 以供执行阶段和信号选择，以及传递给第三级流水的部分也要给第二级，第二级再传递给第三级
    # print(art.mem[0][0])
    stat = "AOK"
    PC = architech.PC
    high = (PC & 0xffff0000) // 0x10000
    low = PC & 0x0000ffff
    opcode = architech.imem[high][low]
    length = opcode_len[opcode]
    nextPC = PC + length
    row = 0
    col = 0
    instructions = ""
    while col<length:
        instructions += architech.imem[high+row][low+col]
        col+=1
        if (col+low)>=65536:
            low-=65536
            row += 1
    icode = instructions[0]
    ifun = instructions[1]
    Instr = opcode_trans[instructions[0]]
    rA = '0'
    rB = '0'
    imm = 0
    addr = 0
    if icode=='0':
        stat = "HAT"
        architech.stat = stat
    elif icode == '1':
        rA = 0
        rB = 0
    elif icode == '2':
        rA = instructions[2]
        rB = instructions[3]
    elif icode=='3':
        rA = instructions[2]
        rB = '0'
        imm = architech.__sign_hex__(instructions[4:])
    elif icode=='4':
        rA = instructions[2]
        rB = instructions[3]
        addr = architech.__sign_hex__(instructions[4:])
    elif icode == '5':
        rA = instructions[2]
        rB = instructions[3]
        addr = architech.__sign_hex__(instructions[4:])
    elif icode == '6':
        rA = instructions[2]
        rB = instructions[3]
        if ifun == '7':
            rB = '0'
    elif icode =='7':
        if ifun == '0' or ifun == '2':
            rA = instructions[2]
            rB = '0'
        elif ifun == '1':
            rA = '0'
            rB = '0'
            addr = architech.__sign_hex__(instructions[2:])
    elif icode == '8':
        rA = instructions[2]
        rB = '0'
    elif icode == '9':
        rA = instructions[2]
        rB = instructions[3]
    elif icode == 'a' or icode =='b':
        rA = instructions[2]
        rB = '0'
    else:
        rA = '0'
        rB = '0'
    rA = int(rA,16)
    rB = int(rB,16)

    return  architech,Instr,rA,rB,addr,imm,nextPC,stat,instructions


def mem_mux(tuple):
    architech = tuple[0]
    Instr = tuple[1]
    rA = tuple[2]
    rB = tuple[3]
    addr = tuple[4]
    imm = tuple[5]
    nextPC = tuple[6]
    stat = tuple[7]
    instructions = tuple[8]

    icode = instructions[0]
    ifun = instructions[0]
    regdata1 = 0
    regdata2 = 0
    BranchPC = nextPC
    if icode in "2689ab":
        regdata1 = architech.reg[rA]
        regdata2 = architech.reg[rB]
    elif icode == '3':
        regdata1 = architech.reg[rA]
        regdata2 = 0
    elif icode in "45":
        regdata1 = architech.reg[rA]
        addr += architech.reg[rB]
    elif icode == '7':
        if ifun == '0':
            regdata1 = architech.reg[0]
            BranchPC = regdata1
            regdata2 = 0
        elif ifun == '1':
            BranchPC = addr
        elif ifun == '2':
            addr = architech.__fetch_le32__(15,architech.reg[rA],4)

    return architech, Instr, rA, rB, regdata1, regdata2, addr, imm, nextPC, BranchPC, stat, instructions


def exec_write(tuple):
    architech, Instr, rA, rB, regdata1, regdata2, addr, imm, nextPC, BranchPC, stat, instructions = tuple
    icode = instructions[0]
    ifun = instructions[1]

    if icode=='1':
        architech.PC = nextPC
        return  architech
    elif icode == '2':
        architech.reg[rA] = regdata2
    elif icode == '3':
        architech.reg[rA] = imm
    elif icode =='4':
        architech.__store__(rA,addr)
    elif icode =='5':
        architech.__fetch_le32__(rA,addr,4)
    elif icode =='6':
        if ifun == '0':
            architech.reg[rA] = regdata1 + regdata2
            if architech.reg[rA] >0:
                architech.PSW = 2
            elif architech.reg[rA]==0:
                architech.PSW = 1
            else:
                architech.PSW = 0
        elif ifun == '1':
            architech.reg[rA] = regdata1 - regdata2
            if architech.reg[rA] >0:
                architech.PSW = 2
            elif architech.reg[rA]==0:
                architech.PSW = 1
            else:
                architech.PSW = 0
        elif ifun == '2':
            architech.reg[rA] = regdata1 * regdata2
            if architech.reg[rA] > 0:
                architech.PSW = 2
            elif architech.reg[rA] == 0:
                architech.PSW = 1
            else:
                architech.PSW = 0
        elif ifun == '3':
            architech.reg[rA] = regdata1 // regdata2
            if architech.reg[rA] > 0:
                architech.PSW = 2
            elif architech.reg[rA] == 0:
                architech.PSW = 1
            else:
                architech.PSW = 0
        elif ifun == '4':
            architech.__logic_and__(rA,rB)
        elif ifun == '5':
            architech.__logic_or__(rA,rB)
        elif ifun== '6':
            fa = bool(not regdata1)
            a  = bool(regdata1)
            fb = bool(not regdata2)
            b  = bool(regdata2)
            logic = (fb and a) or (fa and b)
            architech.reg[logic_reg] = logic
        elif ifun== '7':
            architech.__logic_not__(rA)
    elif icode == '7':
        if ifun == '0':
            architech.PC = regdata1
        elif ifun == '1':
            architech.PC = addr
        elif ifun == '2':
            architech.PC = addr
    elif icode == '8':
        if ifun =='0':
            if architech.PSW!=1:
                architech.PC = BranchPC
        elif ifun == '1':
            if architech.PSW==0 or architech.PSW==1:
                architech.PC = BranchPC
        elif ifun == '2':
            if architech.PSW==0:
                architech.PC = BranchPC
        elif ifun == '3':
            if architech.PSW == 1:
                architech.PC = BranchPC
        elif ifun == '4':
            if architech>PSW == 2:
                architech.PC = BranchPC
        elif ifun =='5':
            if architech.PSW==1 or architech.PSW==2:
                architech.PC = BranchPC
    elif icode == '9':
        if ifun == '0':
            architech.__sal__(rA,regdata2)
        elif ifun == '1':
            architech.__sar__(rA,regdata2)
        elif ifun == '2':
            architech.__shr__(rA,regdata2)
    elif icode == 'a':
        if ifun == '0':
            architech.__push__(rA)
        elif ifun  == '1':
            architech.__pop__(rA)
    elif icode =='b':
        architech.reg[10] = architech.PC
        architech.__push__(10)
        architech.PC = regdata1
    elif icode == 'c':
        architech.__pop__(10)
        architech.PC = architech.reg[10]
    if icode not in "78bc":
        architech.PC = nextPC
    return   architech

string = "30200000008f5030000000ff622320634020000000ff"
length = len(string)
for i in range(0,length,2):
    j = i//2
    imem[0][j] = string[i:i+2]

data = "0000009f"
dmem[0][255]="00"
dmem[0][256]="00"
dmem[0][257]="00"
dmem[0][258]="9f"
architech = Architech(dmem,imem,reg,PC,PSW,stat)
architech.__init__(dmem,imem,reg,PC,PSW,stat)


while architech.stat=="AOK":
    tuple1 = fetch_decode(architech)
    tuple2 = mem_mux(tuple1)
    architech = exec_write(tuple2)
print(architech.reg)
print(architech.mem[0][255:258])
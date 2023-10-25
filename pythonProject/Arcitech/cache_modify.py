##编程实现cache
## 要求: 描述cache的结构和行为
## 结构：tag和数据分离
## 行为：读写访问过程
## 输入&输出
import numpy as np
class memory():
    def __init__(self,mem):
        self.mem = mem

    def __write_mem__(self,addr_mem,data):
        self.mem[addr_mem] = data

    def __read_mem__(self,addr_mem):

        return self.mem[addr_mem]
##data 数据区
##tag 标志区
## tag和data 都有一个组号，该组号下
##假设cachce是32位寻址的
class cache():
    def __init__(self,tag,data,blocks,volum,connect_number):##,index,offset
        self.tag = tag
        self.data = data
        self.blocks = blocks
        self.volum = volum
        self.index = self.volum//(self.blocks * connect_number)  ##总的组数量
        self.offset = np.log2(self.blocks)

        self.con_num = connect_number
        # self.offset = offset
        # self.index = index
    def read_tag(self,addr):
        offset = self.offset                ## 块偏移
        index = addr>>offset % self.index   ## 组号
        index_num = np.log2(self.index)     ## 组大小
        tag =  addr>>(offset+index_num)     ## tag
        tags_list = self.tag[index]         ## tag组
        hit = 0                            ## 标识是否命中
        for i in range(self.con_num):
            if self.tag[index][i]["tag"] == tag and self.tag[index][i]["valid"]==1:
                hit = 1
                break
        if hit == 1:
            return True
        else:
            return False


    def read_data(self,addr):
        offset = self.offset  ## 块偏移
        index = addr >> offset % self.index  ## 组号
        index_num = np.log2(self.index)  ## 组大小
        tag = addr >> (offset + index_num)  ## tag
        datas_list = self.data[index]  ## data组

        offset = self.offset  ## 块偏移
        index = addr >> offset % self.index  ## 组号
        index_num = np.log2(self.index)  ## 组大小
        tag = addr >> (offset + index_num)  ## tag
        tags_list = self.tag[index]  ## tag组

        for i in range(self.con_num):
            if self.read_tag(addr) == True and self.tag[index][i]["tag"] == tag:
                return self.data["index"]
        return

def write(self,addr,data):
    return
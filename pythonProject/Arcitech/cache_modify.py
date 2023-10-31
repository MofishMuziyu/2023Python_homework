##编程实现cache
## 要求: 描述cache的结构和行为
## 结构：tag和数据分离
## 行为：读写访问过程
## 输入&输出
import numpy as np

cache_mem = []
def __write_mem__(addr_mem,data):
    cache_mem[addr_mem] = data

def __read_mem__(addr_mem):

   return cache_mem[addr_mem]
##data 数据区
##tag 标志区
## tag和data 都有一个组号
##假设cachce是32位的
class cache():
    def __init__(self,tag,data,blocks,volum,connect_number):##,index,offset
        self.tag = tag
        self.data = data
        self.blocks = blocks
        self.volum = volum

        self.write_buffer = np.zeros(1)
        self.index = self.volum//(self.blocks * connect_number)  ##总的组数量
        self.offset = np.log2(self.blocks)

        self.con_num = connect_number ##组相连的组数
        # self.offset = offset
        # self.index = index
    def read_tag(self,addr):###命中会返回TRUE，不命中返回false
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


        tags_list = self.tag[index]  ## tag组

        miss = 1
        reload = 0
        for i in range(self.con_num):
            if self.read_tag(addr) == True and self.tag[index][i]["tag"] == tag:
                miss = 0
                return self.data["index"][i]##返回该组中的第i项的数据
        if miss == 1:##cache未命中
            for i in range(self.con_num):
                if self.tag[index][i]["valid"] == 0:
                    self.data[index][i] = __read_mem__(addr)
                    self.tag[index][i]["tag"] = tag
                    self.tag[index][i]["valid"] = 1
                    reload = 1
                    return self.data[index][i]

        if reload == 0:
            number = np.random.randint(0, self.con_num)
            if self.tag[index][number]["dirty"] == 1:
                ##需要写回到mem里面再覆盖
                new_addr = self.tag[index][number]<<(offset + index_num) + self.index + self.offset
                new_data = self.data[index][number]
                self.data[index][number] = __read_mem__(addr)
                self.tag[index][number]["valid"] = 1
                self.tag[index][number]["tag"] = tag
                self.tag[index][number]["dirty"] = 1
                return new_addr,new_data,self.data[index][number]
            else:##如果未被修改，直接覆盖就好
                self.data[index][number] = __read_mem__(addr)
                self.tag[index][number]["valid"] = 1
                self.tag[index][number]["tag"] = tag
                self.tag[index][number]["dirty"] = 1

        return None


    def write(self,addr,data):
        offset = self.offset  ## 块偏移
        index = addr >> offset % self.index  ## 组号
        index_num = np.log2(self.index)  ## 组大小
        tag = addr >> (offset + index_num)  ## tag

        written = 0
        has_write = 0
        for i in range(self.con_num):
            if self.tag[index][i]["valid"] == 1 and self.tag[index][i]["tag"] == tag:##之前写过这个地址的数据
                has_write = 1
                write_index = i
        if has_write == 1:##如果已经存在于cache中，则直接往cache里写
            self.data[index][write_index] = data
            return None


        for i in range(self.con_num):
            if self.tag[index][i]["valid"] == 0 :##该组内有空位
                self.data[index][i] = data
                self.tag[index][i]["valid"] = 1
                self.tag[index][i]["tag"] = tag
                self.tag[index][i]["dirty"] = 1
                written = 1
                return None
        if written == 0: ##如果该组内的所有的data都满了的话，无法写入  先采用随机替换的方法
            number = np.random.randint(0,self.con_num)
            if self.tag[index][number]["dirty"] == 1:
                ##需要写回到mem里面
                new_addr = self.tag[index][number] << (offset + index_num) + self.index + self.offset
                new_data = self.data[index][number]
                self.data[index][number] = data
                self.tag[index][number]["valid"] = 1
                self.tag[index][number]["tag"] = tag
                self.tag[index][number]["dirty"] = 1
                return new_addr, new_data
                ##直接返回数据和地址，表示该要写回到mem里

            else:##如果未被修改，直接覆盖就好
                self.data[index][number] = data
                self.tag[index][number]["valid"] = 1
                self.tag[index][number]["tag"] = tag
                self.tag[index][number]["dirty"] = 1

        return None


class write_buffer():
    def __init__(self):
        self.bufferlen = 0
        self.buffer = []
        self.maxbuffer = 2**8
    def push_buffer(self,addr,data):
        self.buffer.append((addr,data))
        self.bufferlen += 1
        return None

    def pop_buffer(self):
        addr,data = self.buffer.pop()
        self.bufferlen -= 1
        return addr,data

    def out_buffer_check(self):
        flag = 0
        if self.bufferlen >= self.maxbuffer:
            while self.bufferlen>=0:
                addr,data = self.pop_buffer()
                __write_mem__(addr,data)

        return  None


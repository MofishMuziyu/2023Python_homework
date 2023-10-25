def josephus(n,k,m):
    #n代表总人数，k代表报数的数字,m代表剩下的人数
    List = list(range(1,n+1))
    index = 0
    go = []
    while List:
        temp = List.pop(0)
        index += 1
        if index == k:
            go.append(temp)
            index = 0
            continue
        List.append(temp)
        if len(List)==m:
            print(List)
            return go
            break

if __name__ == '__main__':
    print("剩下的人的序号为：")
    remian = josephus(30,9,15)
    print("下船的人的序号为：")
    print(remian)
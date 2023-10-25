def cube(n):
    result = 0
    for i in range(1,n):
        result += i*i*i
    return result

def bubble_sort(A):
    length = len(A)
    for i in range(length-1):
        for j in range(i,length):
            if A[i]>A[j]:
                tmp = A[i]
                A[i] = A[j]
                A[j] = tmp

##h1
n = eval(input("请输入立方和的累加整数："))
print("计算结果为：")
print(cube(n+1))

##h2
A = [5,2,4,3,6,1]
bubble_sort(A)
print("冒泡排序结果为：")
print(A)



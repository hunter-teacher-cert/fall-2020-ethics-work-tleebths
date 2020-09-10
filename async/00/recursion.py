def factorial(x: int):
    if x<2:
        return 1
    else:
        return x * factorial(x-1)
    
def fibonacci(n: int):
    if n<=1:
        return 0
    elif n==2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
def fib(n: int, solved: list):
    length = len(solved)
    
    if n<=length:
        return solved[n-1]
    else:
        solved.append(solved[-1] + solved[-2])
        return fib(n, solved)
    
"""
m and n should not be negative
A(m, n) =   
                  n+1   if  m = 0
            A(m−1, 1)   if  m > 0  and  n = 0
    A(m−1, A(m, n−1))   if  m > 0  and  n > 0
table of values to check ans: https://helloacm.com/ackermann-function/
"""
def ack(m: int, n: int, solved: list):
    if m<0 or n<0:
        print("Invalid parameters:", m, n)
        return -123456789
    
    if m==0:
        solved[m][n] = n+1
        return n+1
    
    # m>0
    if n==0:
        if solved[m][n]==None:
            solved[m][n] = ack(m-1, 1, solved)

        return solved[m][n]
    
    # n>1
    if solved[m][n]==None:
        solved[m][n] = ack(m-1, ack(m, n-1, solved), solved)
    
    return solved[m][n]

def ackermann(m: int, n: int):
    solved = []
    for i in range(100):
        solved.append([None]*100)
    
    return ack(m, n, solved)

#print(factorial(5))
#print(fibonacci("a"))
#print(fib(50,[0,1]))
print(ackermann(0,0), ackermann(0,1), ackermann(0,2), ackermann(0,3))
print(ackermann(1,0), ackermann(1,1), ackermann(1,2), ackermann(1,3))
print(ackermann(2,0), ackermann(2,1), ackermann(2,2), ackermann(2,3))
print(ackermann(3,0), ackermann(3,1), ackermann(3,2), ackermann(3,3))

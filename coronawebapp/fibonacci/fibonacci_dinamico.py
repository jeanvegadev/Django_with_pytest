


def fibonacci_dynamic(n: int) -> int:
    fib_list = [0,1]
    for i in range(1, n):
        fib_list.append(fib_list[i]+fib_list[i-1])
    return fib_list[n]
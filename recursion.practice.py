def factorial(n):
    if n ==0:
        return 1
    else:
        return n * factorial(n-1)

def sum_list(numbers):
    if len(numbers) ==0:
        return 0
    else:
        return numbers[0] + sum_list(numbers[1:])

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


print(fibonacci(5))
    

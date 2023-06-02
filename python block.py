from math import sqrt
#1 task
def is_prime(number):
    return False if False in (False for i in range(2, (number // 2) + 1) if number % i == 0) else True

#2 task
def square(square_side):
    return (square_side * 4, square_side ** 2, square_side * sqrt(2))

#3 task
def bank(a, years):
    return [a := sum([a, a * 0.1]) for year in range(years)][-1]

print(bank(100, 1))
    
    

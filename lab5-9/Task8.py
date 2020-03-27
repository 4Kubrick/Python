#!Zaimplementuj dekorator, który zliczy i wypisze na standardowe wyjście liczbę wywołań danej funkcji,
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        return func(*args, **kwargs)
    wrapper.num_calls = 0
    return wrapper

@count_calls
def f():
    print("My name is Vlad!")

def main():
    i = 1
    while i <= 6:
        f()
        i += 1

    print(f"Call {f.num_calls}")

if __name__ == '__main__':
    main()
#!Zaimplementuj dekorator, który wypisze nazwę i argumenty wywołanej funkcji.

from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        print('Ta funkcja jest dekoratorem')
        return func(*arg,**kwargs)
    return wrapper

@my_decorator
def f():
    print('Hello world')

def main():
    print(f.__name__)
    f()
if __name__ == '__main__':
    main()
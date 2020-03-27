#!Napisz funkcję, która przefiltruje listę liczb całkowitych w celu znalezienia liczb
#!pierwszych. Wykorzystaj w tym celu:
#!a. funkcje map i filter
#!b. list comprehension

from random import randrange

def main():
    my_list = []
    for i in range(20):
        n = randrange(1, 300)
        my_list.append(n)
        
    print(my_list)
    print(list(filter(lambda arg: czy_pierwsza(arg), my_list)))
    print([el for el in my_list if czy_pierwsza(el)])

def czy_pierwsza(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False
    
    pierw = int(n**0.5) + 1
    for dzielnik in range(3, pierw, 2):
        if n % dzielnik == 0:
            return False
    return True

if __name__ == '__main__':
    main()

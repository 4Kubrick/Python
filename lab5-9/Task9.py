#!Napisz program, który zliczy wszystkie wyrazy w danym pliku oraz wypisze wynik na standardowe wyjście.
def main():
    with open('text.txt','r',encoding='UTF-8') as fd:
        print("Liczba wyrazow w pliku wynosi: " + str(len(fd.read().split())))

if __name__ == '__main__':
    main()
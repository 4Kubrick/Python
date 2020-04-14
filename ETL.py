from argparse import ArgumentParser
from sqlite3 import connect
import time

tracks_table_stmt = """
    CREATE TABLE IF NOT EXISTS tracks(
        ExecutionID VARCHAR(50) PRIMARY KEY,
        SongID VARCHAR(50),
        Singer VARCHAR(50),
        Title VARCHAR(50)
    )"""

listening_table_stmt = """
    CREATE TABLE IF NOT EXISTS listenings(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID VARCHAR(50),
        SongID VARCHAR(50),
        ListneningDate VARCHAR(50)
    )"""

insert_tracks_stmt = 'INSERT INTO tracks(ExecutionID, SongID, Singer, Title) VALUES(?, ?, ?, ?)'

insert_listenings_stmt = 'INSERT INTO listenings(UserID, SongID,  ListneningDate) VALUES(?,?,?)'


def parse_tracks_date(show_str, db_path):
    buff_size = 1000000
    path = input(show_str)

    print("\nPobieranie danych...\n")

    timer = time.time()

    with open(path, 'r', encoding='ISO-8859-1') as file_data:
        tmp_lines = file_data.readlines(buff_size)
        while tmp_lines:
            process_tracks([line for line in tmp_lines], db_path)
            tmp_lines = file_data.readlines(buff_size)

    print("\nCzas przetwarzania: %.3f sec" % (time.time() - timer))


def process_tracks(data, db_path):
    list_tracks = []

    for line in data:
        fields = line.replace('\n', '').split('<SEP>')
        field1 = fields[0]
        field2 = fields[1]
        field3 = fields[2]
        field4 = fields[3]
        list_tracks.append((field1, field2, field3, field4))

    with connect(db_path) as db_connector:
        db_connector.execute(tracks_table_stmt)
        db_cursor = db_connector.cursor()
        db_cursor.executemany(insert_tracks_stmt, list_tracks)


def parse_listners_date(show_str, db_path):
    buff_size = 1000000
    path = input(show_str)

    print("\nPobieranie danych...\n")

    timer = time.time()

    with open(path, 'r', encoding='ISO-8859-1') as file_data:
        tmp_lines = file_data.readlines(buff_size)

        while tmp_lines:
            list_tracks = []

            for line in [line for line in tmp_lines]:
                fields = line.replace('\n', '').split('<SEP>')
                field1 = fields[0]
                field2 = fields[1]
                field3 = fields[2]
                list_tracks.append((field1, field2, field3))

            with connect(db_path) as db_connector:
                db_connector.execute(listening_table_stmt)
                db_cursor = db_connector.cursor()
                db_cursor.executemany(insert_listenings_stmt, list_tracks)

            tmp_lines = file_data.readlines(buff_size)

    print("\nCzas przetwarzania: %.3f sec" % (time.time() - timer))


def select_data(path):
    select = True
    while select:
        try:
            print("\n1. 5 najpopularniejszych utworów\n2. Najpopularniejszy artysta\n3. Wyjdź")
            choose2 = input("Podaj liczbę >>")

            if choose2 == "1":
                with connect(path) as db_connector:
                    db_cursor = db_connector.cursor()

                    timer = time.time()

                    print("5 najpopularniejszych utworów:")

                    print("\nZaczekaj chwilę...\n")

                    for entry in db_cursor.execute("""
                                    SELECT tracks.Title, COUNT(listenings.SongID)
                                    FROM listenings 
                                    INNER JOIN tracks 
                                    ON tracks.SongID = listenings.SongID 
                                    GROUP BY listenings.SongID 
                                    ORDER BY COUNT(listenings.SongID) DESC LIMIT 5;"""):
                        print(entry)
                    print("\nCzas przetworzania: %.3f sec" % (time.time() - timer))
            elif choose2 == "2":
                with connect(path) as db_connector:
                    db_cursor = db_connector.cursor()

                    timer = time.time()

                    print("Artysta z największą liczbą odsłuchań:")

                    print("\nZaczekaj chwilę...\n")

                    for entry in db_cursor.execute("""
                                           SELECT tracks.Singer, COUNT(listenings.SongID) AS SongCount
                                           FROM listenings
                                           INNER JOIN tracks 
                                           ON listenings.SongID = tracks.SongID       
                                           GROUP BY tracks.Singer
                                           ORDER BY SongCount DESC LIMIT 1;
                                           """):
                        print(entry)
                    print("\nCzas przetworzania: %.3f sec" % (time.time() - timer))

            elif choose2 == "3":
                select = False
            else:
                print("\nPodany nieprawidłowy znak\n")
        except:
            print("Blad przetwarzania:")
            select = False


def main():
    parser = ArgumentParser(description='This is an example of sql API')
    parser.add_argument('--path', dest='path', type=str, required=True)
    args = parser.parse_args()
    path = args.path
    # db_path = "DataBase.db"

    con_prog = True
    while con_prog:
        print("\n1. Zaladuj dane\n2. Przetworz dane\n3. Wyjdź")
        choose = input("Podaj liczbę >>")

        if choose == "1":
            parse = True

            while parse:
                try:
                    print("\n1. Pobierz utwory\n2. Pobierz odsluchiwania\n3. Wyjdź")
                    choose2 = input("Podaj liczbe >>")

                    if choose2 == "1":
                        parse_tracks_date('Podaj ścieżku do pliku z utworami >', path)
                    elif choose2 == "2":
                        parse_listners_date('Podaj ścieżku do pliku z odsluchaniami >', path)
                    elif choose2 == "3":
                        parse = False
                    else:
                        print("\nPodany nieprawidłowy znak\n")
                except:
                    print("Blad: prawdopodobnie dane juz sa")

        elif choose == "2":
            select_data(path)
        elif choose == "3":
            con_prog = False
        else:
            print("Podany nieprawidłowy znak")


if __name__ == '__main__':
    main()

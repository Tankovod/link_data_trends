import math
import os
import threading
from time import sleep
from subprocess import check_output, CalledProcessError
from colorama import init
from queue import Queue
from src.database_func import pg_insert_curr_datetime, pg_insert_trends, pg_insert_objects

init()


def read_hosts_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    if text:
        text = [[i for i in row.split(' ') if i] for row in text.split('\n') if '#' not in row and row]

    return text


def is_ping(host: list[str], qu: Queue):
    response = ''
    try:
        response = check_output(['ping', '-n', '1', host[0]])
    except CalledProcessError:
        pass
    if response and 'TTL' not in response.decode(encoding='cp1251'):
        response = ''
    table_view = '\033[32m' + host[1] + '\033[0m' if response else '\033[31m' + host[1] + '\033[0m'
    ping = True if response else False
    result = [host[1], host[0], ping, table_view]
    qu.put(result)


def show_table(table, limiter: int, preview=False):
    if not preview:
        table = [i.strip() + (25 - len(i.strip())) * ' ' for i in table if i]
        table.sort(key=lambda x: x[5:])
    else:
        table = [i.strip() + (18 - len(i.strip())) * ' ' for i in table if i]
        table.sort()
    length = math.ceil(len(table) / limiter)
    table_ = []
    for i in range(limiter):
        table_.append(table[length * i: length * (i + 1)])
    os.system('cls')

    for i in range(length):
        def print_rows(indent: int = 0):
            if indent != 0:
                try:
                    print(*[j[i] for j in table_[:indent]], '\n')
                except IndexError:
                    indent -= 1
                    print_rows(indent)
            else:
                print(*[j[i] for j in table_], '\n')
        try:
            print_rows(indent=0)
        except IndexError:
            print_rows(indent=-1)
    sleep(5)


def main():
    clear = os.system('cls')
    while ...:
        hosts = read_hosts_file('h.txt')
        if not clear:
            show_table([i[1] for i in hosts], limiter=10, preview=True)
            clear = 1
        q = Queue()
        threads = []
        for num in range(len(hosts)):
            threads.append(threading.Thread(target=is_ping, args=(hosts[num], q)))
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        data = [q.get() for i in range(len(hosts))]

        pg_insert_objects([(i[0], i[1]) for i in data])
        curr_datetime_id = pg_insert_curr_datetime()
        pg_insert_trends(data=data, curr_datetime_id=curr_datetime_id)

        table_views = [i[3] for i in data]

        show_table(table_views, limiter=10)


if __name__ == '__main__':
    main()

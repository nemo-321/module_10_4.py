#  Импортируем библиотеки:
from queue import Queue
from random import randint
from threading import Thread
from time import sleep


# Создаём класс Table, который представляет стол в кафе.
# Инициализируем стол с параметрами number (номер стола) и guest (гость, который за столом, по умолчанию None).
class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


# Класс Guest (наследуется от Thread):
# Каждый объект этого класса представляет гостя, который является потоком.
# При инициализации задаём имя гостя и переопределяем метод run, который заставляет поток "спать" от 3 до 10 секунд.
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


# Создаем класс Cafe, который принимает переменное количество объектов Table.
# Инициализируем очередь для хранения гостей и список столов.

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    #  Метод guest_arrival:
    #  Этот метод принимает переменное количество гостей и пытается посадить их за стол.
    #  Если стол свободен, гость занимает его, и поток запускается. Если нет, гость добавляется в очередь.
    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    break
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    #  Метод discuss_guests:
    # Метод обслуживает гостей, которые уже сидят за столами.Он проверяет, покинул ли гость стол,
    # и если стол становится свободным, проверяет очередь и пересаживает следующих гостей.
    # Использует задержку, чтобы избежать быстрого цикла.
    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        new_guest.start()
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                    sleep(1)

# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()











from abc import ABC, abstractmethod


class Storage(ABC):
    """Это абстрактный класс типа Хранилище"""

    @abstractmethod
    def add(self, name, qnt):
        pass

    @abstractmethod
    def remove(self, name, qnt):
        pass

    @abstractmethod
    def _get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def _get_unique_items_count(self):
        pass


class Store(Storage):
    """Это склады"""

    def __init__(self, items: dict, capacity=100):
        self.__items = items
        self.__capacity = capacity

    def __str__(self):
        info = "\n"
        for key, value in self.__items.items():
            info += f"{key}: {value}\n"
        return info

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, qnt):
        self.__capacity = qnt

    def add(self, name, qnt):
        """Увеличивает запас items"""
        if self._get_free_space() >= qnt:
            if name in self.__items.keys():
                self.__items[name] += qnt
                print("Товар добавлен\n")
                return True
            else:
                self.__items[name] = qnt
                print("Товар добавлен\n")
                return True
        else:
            if isinstance(self, Store):
                print("На складе отсутствует свободное место для хранения")
            else:
                print("В магазине отсутствует свободное место для хранения")
            return False

    def remove(self, name, qnt):
        """Уменьшает запас items"""
        if name in self.__items:
            if self.__items[name] >= qnt:
                self.__items[name] -= qnt
                return True
            else:
                if isinstance(self, Shop):
                    print(f"В магазине  запрашиваемой позиции '{name}' всего {self.__items[name]} штук")
                else:
                    print(f"На складе запрашиваемой позиции '{name}' всего {self.__items[name]} штук")
                return False
        else:
            if isinstance(self, Shop):
                print(f"В магазине запрашиваемая позиция '{name}' отсутствует.")
            else:
                print(f"На складе запрашиваемая позиция '{name}' отсутствует.")
            return False

    def _get_free_space(self):
        """Возвращает количество свободных мест"""
        occupied_qnt = 0
        for values in self.__items.values():
            occupied_qnt += values
        return self.__capacity - occupied_qnt

    @property
    def get_items(self):
        """Возвращает содержание склада в словаре {товар: количество}"""
        return self.__items

    def _get_unique_items_count(self):
        """Возвращает количество уникальных товаров"""
        return len(self.__items.keys())


class Shop(Store):
    """Это магазины"""

    def __init__(self, items: dict, capacity=20):
        super().__init__(items, capacity)

    def add(self, name, qnt):
        if self._get_unique_items_count() < 5:
            super().add(name, qnt)
            return True
        else:
            print(f"В магазине нет свободного места или находится {self._get_unique_items_count()} уникальных товаров")
            return False


class Request:
    def __init__(self, request_str):
        request_list = request_str.split()
        action_type = request_list[0]
        self.__qnt = int(request_list[1])
        self.__item = request_list[2]
        if action_type == "Забрать":
            self.__from = request_list[4]
            self.__to = None
        elif action_type == "Привезти":
            self.__from = None
            self.__to = request_list[4]
        elif action_type == "Доставить":
            self.__from = request_list[4]
            self.__to = request_list[6]

    def move(self):
        if self.__to and self.__from:
            if eval(self.__from).remove(self.__item, self.__qnt):
                eval(self.__to).add(self.__item, self.__qnt)
        elif self.__to:
            eval(self.__to).add(self.__item, self.__qnt)
        elif self.__from:
            eval(self.__from).remove(self.__item, self.__qnt)


# Заполняем товарами два склада и один магазин
store_1 = Store(items={'Мясо': 1, "Кинза": 2, "Раки": 15})
store_2 = Store(items={'Мясо': 12, "Кинза": 8, "Чипсики": 5})
shop_1 = Shop(items={'Мясо': 1, "Кинза": 8, "Раки": 5})

# Выполнение программы
while True:
    print("\nНа данный момент имеется:")
    print(f"Склад_#1: {store_1}")
    print(f"Склад_#2: {store_2}")
    print(f"Магазин_#1: {shop_1}")
    user_wishes = input("Напиши, что хочется тебе. Например:\n"
                        "- Забрать 2 Кинза из store_1\n"
                        "- Привезти 5 Масло в shop_1\n"
                        "- Доставить 1 Морковь из store_2 в shop_1\n")

    if user_wishes.lower() in ["стоп", "stop"]:
        break
    else:
        try:
            req = Request(user_wishes)
            req.move()
        except Exception as e:
            print(f"Ошибка {e}. Но всё будет отлично.")

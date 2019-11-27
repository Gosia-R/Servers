#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List
from abc import ABC, abstractmethod
from re import fullmatch, match

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i
    #  jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów typu
#  `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze, (2) możliwość
#  odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę
#  wyników wyszukiwania, (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów
#  spełniających kryterium wyszukiwania

class Server(ABC):


    @abstractmethod
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pass


class ListServer(Server):
    def __init__(self, list_of_products: List[Product],*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_max_returned_entries = 4
        self.products = list_of_products[:]

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        regex_string = r'^[a-zA-z]{' + str(n_letters) + r'}\d{2,3}'
        products_found = []
        for product in self.products:
            product_found = fullmatch(regex_string, product.name)
            if product_found is not None:
                products_found.append(product)
        try:
            if len(products_found) > self.n_max_returned_entries:
                products_found = []
                raise TooManyProductsFoundError

            else:
                products_found.sort(key=lambda product: product.price)
        except TooManyProductsFoundError:
            print('Too many products found')
        return products_found


class MapServer(Server):
    def __init__(self, list_of_products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_max_returned_entries = 4
        self.products = {product.name: product for product in list_of_products}

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        products_found = []
        regex_string = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}'
        for product in self.products.keys():
            product_found = fullmatch(regex_string, product)
            if product_found is not None:
                products_found.append(self.products[product])
        try:
            if len(products_found) > self.n_max_returned_entries:
                products_found = []
                raise TooManyProductsFoundError
            else:
                products_found.sort(key=lambda product: product.price)
        except TooManyProductsFoundError:
            pass
        return products_found


class Client:

    def __init__(self, server: Server):
        self.server = server

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        products_found = self.server.get_entries(n_letters)
        if products_found:
            total_price = sum(product.price for product in products_found)
        else:
            total_price = None
        return total_price


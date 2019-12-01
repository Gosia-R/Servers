import unittest
from collections import Counter

from servers import Server, ListServer, Product, Client, MapServer,TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))
            
    def test_raising_an_exception(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('PP236', 4), Product('PP237', 1),
                    Product('PP238', 3)]
        with self.assertRaises(TooManyProductsFoundError):
            for server_type in server_types:
                server = server_type(products)
                entries = server.get_entries(2)



class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
      
    def test_total_price_for_no_match_found_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(0, client.get_total_price(3))

    def test_total_price_for_too_many_entries_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('PP236', 4), Product('PP237', 1), Product('PP238', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()

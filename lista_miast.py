# -*- coding: utf-8
miasta = [ {'id': 0, 'nazwa': 'Warszawa', 'h': 52.259, 'w': 21.020 },
{'id': 1, 'nazwa': u'Łódź', 'h': 51.770, 'w': 19.459},
{'id': 2, 'nazwa': u'Wrocław', 'h': 51.110, 'w': 17.030},
{'id': 3, 'nazwa': u'Poznań', 'h': 52.399, 'w': 16.900},
{'id': 4, 'nazwa': u'Gdańsk', 'h': 54.360, 'w': 18.639},
{'id': 5, 'nazwa': u'Szczecin', 'h': 53.430, 'w': 14.529},
{'id': 6, 'nazwa': u'Bydgoszcz', 'h': 53.120, 'w': 18.010},
{'id': 7, 'nazwa': u'Lublin', 'h': 51.240, 'w': 22.570},
{'id': 8, 'nazwa': u'Białystok', 'h': 53.139, 'w': 23.159},
{'id': 9, 'nazwa': 'Radom', 'h': 51.399, 'w': 21.159},
{'id': 10, 'nazwa': u'Kraków', 'h': 50.06, 'w': 19.959 } ]

sciezki = [ {'od': 0, 'do': 1, 'dlugosc': 130 },   #Warszawa - Łódź
{'od': 2, 'do': 3, 'dlugosc': 157 },   # Wrocław - Poznań
{'od': 2, 'do': 10, 'dlugosc': 256 },  # Wrocław - Kraków
{'od': 7, 'do': 10, 'dlugosc': 247 },  # Lublin - Kraków
{'od': 0, 'do': 9, 'dlugosc': 100 },   # Warszawa - Radom
{'od': 0, 'do': 7, 'dlugosc': 166 },   # Warszawa - Lublin
{'od': 0, 'do': 6, 'dlugosc': 245 },   # Warszawa - Bydgoszcz
{'od': 3, 'do': 6, 'dlugosc': 117 },   # Poznań - Bydgoszcz
{'od': 0, 'do': 3, 'dlugosc': 303 },   # Warszawa - Poznań
{'od': 9, 'do': 10, 'dlugosc': 186 },  # Radom - Kraków
{'od': 3, 'do': 5, 'dlugosc': 212 },   # Szczecin - Poznań
{'od': 4, 'do': 5, 'dlugosc': 312 },   # Gdańsk - Szczecin
{'od': 6, 'do': 8, 'dlugosc': 375 },   # Bydgoszcz - Białystok
{'od': 0, 'do': 8, 'dlugosc': 192 },   # Warszawa - Białystok
{'od': 4, 'do': 6, 'dlugosc': 155 },   # Gdańsk - Bydgoszcz
{'od': 1, 'do': 2, 'dlugosc': 134 } ]  # Łódź - Wrocław

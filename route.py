# -*- coding: utf-8
from flask import Flask, request, redirect
from werkzeug.debug import DebuggedApplication
from heapq import heappush, heappop
from lista_miast import miasta, sciezki
from collections import OrderedDict
import json

nieskonczonosc = float('inf')
startowe = 0
docelowe = 0

app = Flask(__name__)
app.secret_key = 'R*9#(@)!??}saza!-'
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


# Niektore metody route powinny udostępniac zasoby tylko za pomocą 'post', używam get, żeby użytkownik mógł mieć łatwiejszy dostęp przez przeglądarkę

# Najpierw nalezy ustawic wezel startowy i docelowy

@app.route('/<od>/<do>/', methods=['POST', 'GET'])
def generate_route(od, do):
    return dijkstry(int(od), int(do))


@app.route( '/mapa/', methods=['GET'])
def mapa():
    mapa = 'https://maps.googleapis.com/maps/api/staticmap?center=Poland&size=640x640&maptype=roadmap&markers=color:purple'
    for miasto in miasta:
        for k, v in miasto.iteritems():
            if k == 'h':
                mapa += '|' + str(v) + ','
            elif k == 'w':
                mapa += str(v)
    mapa += '&key=..'
    return mapa


@app.route( '/mapa/<od>/<do>/', methods=['POST', 'GET'])
def mapa_trasa(od, do):
    mapa = 'https://maps.googleapis.com/maps/api/staticmap?center=Poland&size=640x640&maptype=roadmap&markers=color:purple'
    for miasto in miasta:
        for k, v in miasto.iteritems():
            if k == 'h':
                mapa += '|' + str(v) + ','
            elif k == 'w':
                mapa += str(v)
    trasa = json.loads(dijkstry(int(od), int(do)))
    mapa += '&path=color:red|weight:7'
    trasa.__delitem__('dlugosc')
    trasa_ord = OrderedDict(sorted(trasa.items()))
    # potrzebujemy wsporzednych, nie id
    for index in trasa_ord:
        mapa += '|' + str(miasta[int(trasa[index])]['h']) + ','
        mapa += str(miasta[int(trasa[index])]['w'])
    mapa += '&key=...'
    return mapa


@app.route( '/newnode/<h>/<w>/<nazwa>', methods=['GET'])
def note(h, w, nazwa):
    miasta.append({'nazwa': nazwa, 'h': h, 'w': w, 'id': len(miasta)})
    return json.dumps(miasta)


@app.route( '/cities/', methods=['GET'])
def zwroc_miasta():
    return json.dumps(miasta)


@app.route( '/city/<id>', methods=['GET'])
def zwroc_miasto(id):
    id = int(id)
    if id < 0 or id > len(miasta):
        return 404, "W bazie nie ma miasta o takim id"
    return json.dumps(miasta[id])


@app.route( '/newroute/<od>/<do>/<dlugosc>', methods=['GET'])
def nowa_sciezka(od, do, dlugosc):
    nowa = {'od': int(od), 'do': int(do), 'dlugosc': int(dlugosc)}
    if nowa not in sciezki:
        sciezki.append(nowa)
    return json.dumps(sciezki)


@app.route( '/routes/', methods=['GET'])
def zwroc_trasy():
    return json.dumps(sciezki)


def wylicz_odleglosc(start, koniec):
    for sciezka in sciezki:
        if (sciezka['od'] == start and sciezka['do'] == koniec) or (sciezka['od'] == koniec and sciezka['do'] == start):
            return sciezka['dlugosc']
    return nieskonczonosc


def generuj_trase_json(d, poprzednicy, startowe, docelowe):
    trasa = {}
    trasa_tab = []
    poprzednik = poprzednicy[docelowe]
    print "poprzednicy-----------------"
    print poprzednicy
    while poprzednik != None:
        trasa_tab.append(poprzednik)  # dostajemy poprzednikow, ale od konca
        poprzednik = poprzednicy[poprzednik]

    i = len(trasa_tab) - 1  # odwracamy tablice
    j = 1
    while i >= 0:
        trasa.update({j: trasa_tab[i]})
        i -= 1
        j += 1
    result = {'0': startowe, 'dlugosc': d[docelowe]}
    result.update(trasa)
    result.update({j: docelowe})
    return json.dumps(result)


def znajdz_sasiadow(id):
    sasiedzi_w = []
    for sciezka in sciezki:  # szukam sasiadow
        if sciezka['od'] == id:
            sasiedzi_w.append(sciezka['do'])  # wrzucam id
        if sciezka['do'] == id:
            sasiedzi_w.append(sciezka['od'])
    return sasiedzi_w


def generuj_tablice_wierzcholkow(startowe, poprzednicy):
    d = []  # tablica odleglosci wierzcholkow od zrodla
    for miasto in miasta:
        d.append(None)
        poprzednicy.append(None)
    for sciezka in sciezki:  # sprawdzam polaczenia pomiedzy zrodlem a sasiadami
        if sciezka['od'] == startowe:
            d[sciezka['do']] = sciezka['dlugosc']
        if sciezka['do'] == startowe:
            d[sciezka['od']] = sciezka['dlugosc']
    for miasto in miasta:
        if d[miasto['id']] == None:  # dalsze miasta
            d[miasto['id']] = nieskonczonosc
        if miasto['id'] == startowe:
            d[startowe] = 0
    return d


def dijkstry(startowe, docelowe):
    poprzednicy = []
    d = generuj_tablice_wierzcholkow(startowe, poprzednicy)  # odleglosci od zrodla
    q = []  # tworzenie kolejki priorytetowej, priorytet to odleglosc od zrodla
    index = 0
    for odleglosc in d:
        heappush(q, (odleglosc, index))
        index += 1
    print q

    while len(q) != 0:
        u = heappop(q)  # krotka ( odleglosc, index )
        sasiedzi_u = znajdz_sasiadow(u[1])
        for sasiad in sasiedzi_u:
            if d[sasiad] > d[u[1]] + wylicz_odleglosc(sasiad, u[1]):
                d[sasiad] = d[u[1]] + wylicz_odleglosc(sasiad, u[1])
                poprzednicy[sasiad] = u[1]
    print "-----------------------------------------------------"
    print d
    print poprzednicy
    return generuj_trase_json(d, poprzednicy, startowe, docelowe)


if __name__ == '__main__':
    app.run()

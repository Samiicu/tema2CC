import json
import re
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from random import randint

from cerberus import *

from test import do_update


class RestHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                gasite = []
                pathRoute = self.path.split('/')[1:]

                # aici vin requesturile get

                if len(pathRoute) == 1 and pathRoute[0] == 'sub-meniuri':
                    # inseamna ca rute e de genul  localhost/resurse deci o sa ii returnez la fraier toate resursele
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(sub_meniuri).encode())
                    return
                elif len(pathRoute) == 2 and pathRoute[0] == 'sub-meniuri':
                    try:
                        if re.match("(\d{2,3})", pathRoute[1]).group(1):
                            for sub_meniu in sub_meniuri:
                                if int(sub_meniu["id"]) == int(pathRoute[1]):
                                    self.send_response(200)
                                    self.end_headers()
                                    self.wfile.write(json.dumps(sub_meniu).encode())
                                    return

                            self.send_response(404)
                            self.end_headers()
                            return
                    except:
                        pass
                    gasite = []

                    for sub_meniu in sub_meniuri:
                        if sub_meniu["denumire"] == pathRoute[1]:
                            for resursa in date_meniu:
                                if resursa["id_sub-meniu"] == int(sub_meniu["id"]):
                                    gasite.append(resursa)
                            if len(gasite) == 0:
                                self.send_response(204)
                                self.end_headers()
                                return
                            else:
                                self.send_response(200)
                                self.end_headers()
                                self.wfile.write(json.dumps(gasite).encode())
                                return
                        else:
                            self.send_response(404)
                            self.end_headers()
                            return

                if len(pathRoute) == 1 and pathRoute[0] == 'meniu':
                    # inseamna ca rute e de genul  localhost/resurse deci o sa ii returnez la fraier toate resursele
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(date_meniu).encode())
                    return
                elif len(pathRoute) == 2 and pathRoute[0] == 'meniu':
                    try:
                        if re.match("(\d{7,10})", pathRoute[1]).group(1):
                            for resursa in date_meniu:
                                if int(pathRoute[1]) == int(resursa['id']):
                                    self.send_response(200)
                                    self.end_headers()
                                    self.wfile.write(json.dumps(resursa).encode())
                                    return
                            self.send_response(404)
                            self.end_headers()
                            return

                    except:
                        pass;
                    gasite = []
                    # ruta are doi parametrii, presupun ca al doilea e id-ul , de genul localhost/resurse/12312321321(asta e id)
                    # ii returnez la fraier resursa cu id-ul cerut

                    for sub_meniu in sub_meniuri:
                        if sub_meniu["denumire"] == pathRoute[1]:
                            for resursa in date_meniu:
                                if resursa["id_sub-meniu"] == int(sub_meniu["id"]):
                                    gasite.append(resursa)
                            if len(gasite) == 0:
                                self.send_response(204)
                                self.end_headers()
                                return
                            else:
                                self.send_response(200)
                                self.end_headers()
                                self.wfile.write(json.dumps(gasite).encode())
                                return

                    self.send_response(404)
                    self.end_headers()
                    return
                    # return
                elif len(pathRoute) == 3 and pathRoute[0] == 'meniu':
                    gasite = []
                    for sub_meniu in sub_meniuri:
                        if sub_meniu["denumire"] == pathRoute[1]:
                            for resursa in date_meniu:
                                if resursa["id_sub-meniu"] == int(sub_meniu["id"]):
                                    if resursa['denumire'] == pathRoute[2]:
                                        gasite.append(resursa)

                            if len(gasite) == 0:
                                self.send_response(404)
                                self.end_headers()
                                return
                            else:
                                self.send_response(200)
                                self.end_headers()
                                self.wfile.write(json.dumps(gasite).encode())
                                return

                    self.send_response(400)
                    self.end_headers()
                    return

                self.send_response(400)
                self.end_headers()
                return
            except:
                self.send_response(500)
                self.end_headers()
                return

        def do_POST(self):
            try:
                try:
                    inputData = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                except:
                    self.send_response(415)
                    self.end_headers()
                    return
                pathRoute = self.path.split('/')[1:]

                if len(pathRoute) == 1 and pathRoute[0] == 'meniu':
                    if validator_meniu.validate(inputData) is False:
                        self.send_response(422)
                        self.end_headers()
                        return
                    for sub_meniu in sub_meniuri:
                        if int(sub_meniu["id"]) == int(inputData['id_sub-meniu']):
                            resursaNoua = {'id': genID(7, date_meniu), "id_sub-meniu": inputData['id_sub-meniu'],
                                           'denumire': inputData['denumire'], 'cantitate': inputData['cantitate'],
                                           'pret': inputData['pret'], 'continut': inputData['continut']}
                            date_meniu.append(resursaNoua)
                            self.send_response(201)
                            self.end_headers()
                            self.wfile.write(
                                json.dumps("http://localhost:8000" + self.path + "/" + str(resursaNoua["id"])).encode())
                            do_update(date_meniu, "date_meniu.json")
                            return

                    self.send_response(409)
                    self.end_headers()
                    return
                elif len(pathRoute) == 1 and pathRoute[0] == 'sub-meniuri':
                    if validator_sub_meniu.validate(inputData) is False:
                        self.send_response(422)
                        self.end_headers()
                        return

                    resursaNoua = {'id': genID(2, sub_meniuri), 'denumire': inputData['denumire']}
                    sub_meniuri.append(resursaNoua)
                    self.send_response(201)
                    self.end_headers()
                    self.wfile.write(
                        json.dumps("http://localhost:8000" + self.path + "/" + str(resursaNoua["id"])).encode())
                    do_update(sub_meniuri, "sub_meniuri.json")
                    return

                # input data o pui in postman din body si setezi sa fie json
                if len(pathRoute) == 2 and pathRoute[0] == 'meniu':
                    if validator_meniu  .validate(inputData) is False:
                        self.send_response(422)
                        self.end_headers()
                        return
                    for sub_meniu in sub_meniuri:
                        if int(sub_meniu["id"]) == int(inputData['id_sub-meniu']):
                            for resursa in date_meniu:
                                if int(resursa['id']) == int(pathRoute[1]):
                                    self.send_response(409)
                                    self.end_headers()
                                    return
                            resursaNoua = {'id': int(pathRoute[1]), "id_sub-meniu": inputData['id_sub-meniu'],
                                           'denumire': inputData['denumire'], 'cantitate': inputData['cantitate'],
                                           'pret': inputData['pret'], 'continut': inputData['continut']}
                            date_meniu.append(resursaNoua)
                            self.send_response(201)
                            self.end_headers()
                            self.wfile.write(json.dumps(resursaNoua).encode())
                            do_update(date_meniu, "date_meniu.json")
                            return

                    self.send_response(409)
                    self.end_headers()
                    return
                elif len(pathRoute) == 2 and pathRoute[0] == 'sub-meniuri':
                    if validator_sub_meniu.validate(inputData) is False:
                        self.send_response(422)
                        self.end_headers()
                        return
                    for sub_meniu in sub_meniuri:
                        if int(sub_meniu["id"]) == int(pathRoute[1]) or inputData['denumire'] == sub_meniu[
                            "denumire"]:
                            self.send_response(409)
                            self.end_headers()
                            return
                    resursaNoua = {'id': int(pathRoute[1]), 'denumire': inputData['denumire']}
                    sub_meniuri.append(resursaNoua)
                    self.send_response(201)
                    self.end_headers()
                    self.wfile.write(json.dumps(resursaNoua).encode())
                    do_update(sub_meniuri, "sub_meniuri.json")
                    return

                # ruta a fost naspa deci ii returnez la fraier 400
                self.send_response(400)
                self.end_headers()
                return
            except:
                self.send_response(500)
                self.end_headers()
                return

        def do_PUT(self):
            try:

                # aici vin requesturi de tip put, adica de update
                try:
                    inputData = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                except:
                    self.send_response(415)
                    self.end_headers()
                    return
                pathRoute = self.path.split('/')[1:]
                if len(pathRoute) == 1 and (pathRoute[0] == 'meniu' or pathRoute[0] == 'sub-meniuri'):
                    self.send_response(405)
                    self.end_headers()
                    return
                if len(pathRoute) == 2 and pathRoute[0] == 'meniu':
                    if validator_meniu.validate(inputData) is False:
                        self.send_response(422)
                        self.end_headers()
                        return
                    for sub_meniu in sub_meniuri:
                        if int(sub_meniu["id"]) == int(inputData['id_sub-meniu']):
                            for i in range(0, len(date_meniu)):
                                if int(date_meniu[i]['id']) == int(pathRoute[1]):
                                    resursaUpdate = {'id': int(pathRoute[1]), "id_sub-meniu": inputData['id_sub-meniu'],
                                                     'denumire': inputData['denumire'], 'cantitate': inputData['cantitate'],
                                                     'pret': inputData['pret'], 'continut': inputData['continut']}
                                    date_meniu[i] = resursaUpdate
                                    self.send_response(200)
                                    self.end_headers()
                                    self.wfile.write(json.dumps(date_meniu[i]).encode())
                                    do_update(date_meniu, "date_meniu.json")
                                    return
                            self.send_response(404)
                            self.end_headers()
                            return

                    self.send_response(409)
                    self.end_headers()
                    return
                elif len(pathRoute) == 2 and pathRoute[0] == 'sub-meniuri':
                    if validator_sub_meniu.validate(inputData) is False:
                        self.send_response(422)
                        self.end_headers()
                        return

                    for i in range(0, len(sub_meniuri)):
                        if int(sub_meniuri[i]['id']) == int(pathRoute[1]):
                            resursaUpdate = {'id': int(pathRoute[1]), 'denumire': inputData['denumire']}
                            sub_meniuri[i] = resursaUpdate
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(json.dumps(sub_meniuri[i]).encode())
                            do_update(sub_meniuri, "sub_meniuri.json")
                            return
                    self.send_response(404)
                    self.end_headers()
                    return

                self.send_response(400)
                self.end_headers()
                return
            except Exception as e:
                print e
                self.send_response(500)
                self.end_headers()
                return

        def do_DELETE(self):
            try:

                # aici vin requesturi de delete
                pathRoute = self.path.split('/')[1:]
                if len(pathRoute) == 1 and (pathRoute[0] == 'meniu' or pathRoute[0] == 'sub-meniuri'):
                    self.send_response(405)
                    self.end_headers()
                    return

                if len(pathRoute) == 2 and pathRoute[0] == 'meniu':
                    for i in range(0, len(date_meniu)):
                        if date_meniu[i]['id'] == int(pathRoute[1]):
                            date_meniu.pop(i)
                            self.send_response(200)
                            self.end_headers()
                            do_update(date_meniu, "date_meniu.json")
                            return
                    self.send_response(404)
                    self.end_headers()
                    return
                elif len(pathRoute) == 2 and pathRoute[0] == 'sub-meniuri':
                    for i in range(0, len(sub_meniuri)):
                        if sub_meniuri[i]['id'] == int(pathRoute[1]):
                            sub_meniuri.pop(i)
                            self.send_response(200)
                            self.end_headers()
                            do_update(sub_meniuri, "sub_meniuri.json")
                            return
                    self.send_response(404)
                    self.end_headers()
                    return

                # ruta a fost naspa deci ii returnez la fraier 400
                self.send_response(400)
                self.end_headers()
                return
            except:
                self.send_response(500)
                self.end_headers()
                return


def genID(n, res):
    global id
    unic = False
    while unic is False:
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        id = randint(range_start, range_end)
        unic = True
        for resursa in res:
            if resursa['id'] == id:
                unic = False
    return id


with open('sub_meniuri.json') as f:
    sub_meniuri = json.load(f)

with open('date_meniu.json') as f:
    data = json.load(f)
date_meniu = data

schema_meniu = {'id_sub-meniu': {'type': 'integer'}, "continut": {'type': ['string', 'list']},
                "cantitate": {'type': 'string'}, "denumire": {'type': 'string'}, "pret": {'type': 'string'},
                "id": {'type': 'integer'}}
schema_sub_meniu = {"id": {'type': 'integer'}, "denumire": {'type': 'string'}}
validator_meniu = Validator(schema_meniu)
validator_sub_meniu = Validator(schema_sub_meniu)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


httpd = ThreadedHTTPServer(('0.0.0.0', 8000), RestHTTPRequestHandler)
httpd.serve_forever()

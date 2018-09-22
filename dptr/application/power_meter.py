#!/usr/bin/env python3
import socketserver, sys, os
import struct
import logging
import threading
import argparse
import socket
from urllib import request
from threading import Thread

sys.path.append(os.path.abspath(os.path.join("..", "..")))
from common.Def import *

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, required=True, help="translator will be running on which port")
parser.add_argument("--web_addr", required=True, help="web address")
parser.add_argument("--web_port", required=True, help="web port")
args = parser.parse_args()

HOST_ADDR = ""
HOST_PORT = args.port
WEB_ADDR = args.web_addr
WEB_PORT = args.web_port

dev_id_map = {}

class service(socketserver.BaseRequestHandler):

    def handle(self):

        def __prepare_report(data):
            #8B devid 8B usage#
            dev_id, usage = struct.unpack("=Qd", data)
            #client address
            addr, port = self.client_address
            return dev_id, usage, addr, port

        def __rx_data_from_webserver(appsock, dev_id):
            url = "http://{}:{}/recv?id={}".format(WEB_ADDR, WEB_PORT, hex(dev_id))
            with request.urlopen(url) as f:
                response = f.read().decode("utf-8")
                if response == "start":
                    ret = struct.pack("!B", 1)
                else:
                    ret = struct.pack("!B", 0)
                appsock.sendall(ret)


        def __rx_thr_main(appsock, dev_id):
            while True:
                try:
                    __rx_data_from_webserver(appsock, dev_id)
                except:
                    logging.debug("recv from webserver timeout!")

        def __tx_data_to_webserver(appsock):
            data = appsock.recv(16) #8B devid and 8B usage
            dev_id, usage, addr, port= __prepare_report(data)

            if dev_id not in dev_id_map:
                #luanch a thread
                dev_id_map[dev_id] = True
                threading.Thread(target = __rx_thr_main, args=(appsock, dev_id)).start()

            url = "http://{}:{}/send?id={}&addr={}:{}&data={:.4f}".format(WEB_ADDR, WEB_PORT, hex(dev_id), addr, port, usage)
            with request.urlopen(url) as f:
                logging.debug("report date to server: {}".format(url))


        logging.info("accept a connection from a device")

        while True:
            try:
                __tx_data_to_webserver(self.request)
            except Exception as e:
                print(e)
                break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    ThreadedTCPServer.allow_reuse_addr = True
    server = ThreadedTCPServer((HOST_ADDR, HOST_PORT), service)
    server.serve_forever()

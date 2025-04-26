import os
from threading import Thread
import sqlite3 as sq


def state(sock, plc):
    if plc.is_started:
        sock.send('is started')
    else:
        sock.send('not started')


def counter(sock, plc):
    sock.send(str(len(os.listdir('C:/PycharmProjects/Machine_vision/web_interface/static/data'))))


def check_error(sock, plc):
    if plc.error_camera is True:
        sock.send('camera error')


def starting(sock, plc):
    if plc.is_started is False:
        th = Thread(target=plc.monitoring, name="Monitoring")
        th.start()


def stoped(sock, plc):
    if plc.is_started is True:
        plc.stop_monitoring()


ADMIN_SOCKET_COMMANDS = {
    'Get count': counter,
    'is started': state,
    'check error': check_error,
    'Start': starting,
    'Stop': stoped
}


def choice_setpoint():
    select_list = [0.5, 0.6, 0.7, 0.8, 0.9]
    with sq.connect("C:/PycharmProjects/Machine_vision/data_base/trash_pallets.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT setpoint FROM config""")
        setpoint = cur.fetchone()
    index = select_list.index(float(setpoint[0]))
    return [select_list, index]


def change_setpoint(value):
    with sq.connect("C:/PycharmProjects/Machine_vision/data_base/trash_pallets.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE config SET setpoint = ?""", (value,))
        con.commit()


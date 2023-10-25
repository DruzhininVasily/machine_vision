import snap7
from snap7 import types as tp
import time
import threading
from photo_handling import get_photo

lock = threading.Lock()


class PlcClient(snap7.client.Client):

    def __init__(self, ip, rack, slot):
        self.is_started = False
        self.flag = False
        self.data_area = None
        super().__init__()
        self.connect(ip, rack, slot)

    def monitoring(self):
        self.is_started = True
        while self.is_started is True:
            th = threading.Thread(target=get_photo, name='get photo')
            lock.acquire()
            try:
                self.data_area = self.read_area(tp.Areas['MK'], 0, 6304, 1)
                val = snap7.util.get_bool(self.data_area, 0, 0)
            except RuntimeError:
                self.is_started = False
                print("Ошибка соединения с PLC. Перезапустите приложение")
            finally:
                lock.release()
            if val is True and self.flag is False:
                th.start()
                self.flag = True
            elif val is False:
                self.flag = False
            time.sleep(1)

    def stop_monitoring(self):
        lock.acquire()
        try:
            self.is_started = False
        finally:
            lock.release()

    def blocking_pallet(self):
        lock.acquire()
        try:
            snap7.util.set_bool(self.data_area,0, 1, True)
            self.write_area(tp.Areas['MK'], 0, 6304, self.data_area)
        finally:
            lock.release()

    def submit_button(self):
        lock.acquire()
        try:
            snap7.util.set_bool(self.data_area, 0, 1, False)
            self.write_area(tp.Areas['MK'], 0, 6304, self.data_area)
        finally:
            lock.release()








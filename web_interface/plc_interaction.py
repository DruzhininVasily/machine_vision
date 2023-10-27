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
        self.data_in = None
        self.data_out = None
        self.data_pallet = None
        super().__init__()
        self.connect(ip, rack, slot)
        self.pallet_is_blocking = False

    def monitoring(self):
        # Маркер мониторинга
        self.is_started = True
        # Включение режима с камерой
        self.data_out = self.read_area(tp.Areas['MK'], 0, 6305, 1)
        snap7.util.set_bool(self.data_out, 0, 3, False)
        self.write_area(tp.Areas['MK'], 0, 6305, self.data_out)
        # Мониторинг состояния датчика
        while self.is_started is True:
            lock.acquire()
            try:
                self.data_in = self.read_area(tp.Areas['MK'], 0, 6304, 1)
                # self.data_in = self.read_area(tp.Areas['MK'], 0, 6305, 1)
                val = snap7.util.get_bool(self.data_in, 0, 0)
                # val = snap7.util.get_bool(self.data_in, 0, 4)
                self.data_pallet = self.read_area(tp.Areas['MK'], 0, 6102, 2)
                self.data_pallet = snap7.util.get_word(self.data_pallet, 0)
            except RuntimeError:
                self.is_started = False
                print("Ошибка соединения с PLC. Перезапустите приложение")
            finally:
                lock.release()
            th = threading.Thread(target=get_photo, name='get photo', args=(self.data_pallet, self,))
            if val is True and self.flag is False:
                th.start()
                self.flag = True
            elif val is False:
                self.flag = False
                # Возврат значений в default
                lock.acquire()
                try:
                    self.set_default()
                finally:
                    lock.release()
            time.sleep(1)

    def stop_monitoring(self):
        lock.acquire()
        try:
            self.is_started = False
        finally:
            lock.release()
        lock.acquire()
        try:
            self.data_out = self.read_area(tp.Areas['MK'], 0, 6305, 1)
            snap7.util.set_bool(self.data_out, 0, 3, True)
            self.write_area(tp.Areas['MK'], 0, 6305, self.data_out)
        finally:
            lock.release()
        lock.acquire()
        try:
            self.set_default()
        finally:
            lock.release()

    # Подтверждение завершения съёмки кадра
    def camera_shot(self):
        lock.acquire()
        try:
            self.data_out = self.read_area(tp.Areas['MK'], 0, 6305, 1)
            snap7.util.set_bool(self.data_out, 0, 1, True)
            self.write_area(tp.Areas['MK'], 0, 6305, self.data_out)
        finally:
            lock.release()

    def blocking_pallet(self):
        lock.acquire()
        try:
            snap7.util.set_bool(self.data_out,0, 0, False)
            self.write_area(tp.Areas['MK'], 0, 6305, self.data_out)
        finally:
            lock.release()
        lock.acquire()
        try:
            self.pallet_is_blocking = True
        finally:
            lock.release()

    def submit_button(self):
        lock.acquire()
        try:
            snap7.util.set_bool(self.data_out, 0, 2, True)
            self.write_area(tp.Areas['MK'], 0, 6305, self.data_out)
        finally:
            lock.release()
        lock.acquire()
        try:
            self.pallet_is_blocking = False
        finally:
            lock.release()

    # Возврат значений в default
    def set_default(self):
        self.data_out = self.read_area(tp.Areas['MK'], 0, 6305, 1)
        snap7.util.set_bool(self.data_out, 0, 0, True)
        snap7.util.set_bool(self.data_out, 0, 1, False)
        snap7.util.set_bool(self.data_out, 0, 2, False)
        self.write_area(tp.Areas['MK'], 0, 6305, self.data_out)








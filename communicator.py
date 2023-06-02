import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.defines as cst
import time
import threading

class ModbusModule:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.master = modbus_tcp.TcpMaster(host=self.ip, port=self.port)
        self.master.set_timeout(5.0)
        self.lock = threading.Lock()
        self.readData = []
        self.writeData = []
        self.output = []

    def work_thread(self, address, length, interval=0.05):
        while True:
            # self.read(address, length)
            # self.readCoil(address, length)# read Q (usually a switch or a button)
            ans = []
            # hongwai diangan huoer
            # wendu / 2048 * 100
            # wendu2 / 32768 * 100, pwm0 (motor) pwm1(fan) pwm2(heater)
            self.readDiscrete(address, length)# read I (usually a light for notification)) 
            ans.extend(self.readData[0:3])# %IX0.0-0.2
            # self.readAnalog(address, 10)
            # ans.append(self.readData[0])
            self.readAnalogOutput(address, 20)
            ans.extend(self.readData[8:18])# %MQW8-18
            # self.readCoil(address, length)
            # ans.extend(self.readData)
            self.output = ans            
            time.sleep(interval)
  
    def start(self, address, length, interval=0.1):
        self.thread = threading.Thread(target=self.work_thread, args=(address, length, interval), daemon=True)
        self.thread.start()

    def get_data(self):
        return self.output

    def read(self, address, length):
        self.lock.acquire()
        try:
            self.readData = self.master.execute(1, cst.READ_HOLDING_REGISTERS, address, length)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
    
    def write(self, address, value):
        self.lock.acquire()
        try:
            self.master.execute(1, cst.WRITE_SINGLE_REGISTER, address, output_value=value)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def writeMultiple(self, address, length, values):
        self.lock.acquire()
        try:
            self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, address, length, output_value=values)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def readCoil(self, address, length):
        self.lock.acquire()
        try:
            self.readData = self.master.execute(1, cst.READ_COILS, address, length)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
    
    def writeCoil(self, address, value):
        self.lock.acquire()
        try:
            self.master.execute(1, cst.WRITE_SINGLE_COIL, address, output_value=value)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def writeMultipleCoil(self, address, values):
        self.lock.acquire()
        try:
            self.master.execute(1, cst.WRITE_MULTIPLE_COILS, address, output_value=values)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
    
    def readDiscrete(self, address, length):
        self.lock.acquire()
        try:
            self.readData = self.master.execute(1, cst.READ_DISCRETE_INPUTS, address, length)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()

    def readAnalog(self, address, length):
        self.lock.acquire()
        try:
            #data is udint
            self.readData = self.master.execute(1, cst.READ_INPUT_REGISTERS, address, length)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
    def readAnalogOutput(self, address, length):
        self.lock.acquire()
        try:
            self.readData = self.master.execute(1, cst.READ_HOLDING_REGISTERS, address, length)
        except Exception as e:
            print(e)
        finally:
            self.lock.release()
            
def show(data):
    # n_r n_y n_g jia yi w_g w_y w_r
    if len(data) >= 8:
        print(f"n_r:{data[0]} n_y:{data[1]} n_g:{data[2]} jia:{data[3]} yi:{data[4]} w_g:{data[5]} w_y:{data[6]} w_r:{data[7]}")

if __name__ == "__main__":
    modbus = ModbusModule("192.168.1.1", 502)
    modbus.start(0, 10)
    while True:
        # show(modbus.get_data())
        print(modbus.get_data())
        time.sleep(1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import random
import threading
import time

import DHT11
import MAX30102


class DataFlow:
    def __init__(self, dht11: str, max30102: str):
        self.temperature = [(0, 36.5)]
        self.humidity = [(0, 10)]
        self.heart_rate = [(0, 60)]
        self.dht11 = dht11
        self.max30102 = max30102
        self.stop = False
        self.__max_buffer = 20
        self.hr_max = 255

    def buffer_limit(self, buffer):
        if len(buffer) > self.__max_buffer:
            buffer = buffer[len(buffer) - self.__max_buffer:]
        return buffer

    def stop(self):
        self.stop = True


def read_dht11(data_flow: DataFlow):
    dht11_gpio_pins = data_flow.dht11
    dht11_gpio_pins = dht11_gpio_pins.split(',')
    dht11_gpio_pins = [int(x) for x in dht11_gpio_pins]
    time_index = 1
    while not data_flow.stop:
        # logging.info('__read_dht11 index ' + str(time_index))
        global_dht11_index = random.randint(0, 1)
        # humidity, temperature = (random.randint(22, 30), random.randint(30, 35))
        humidity, temperature = DHT11.read_temperature_and_humidity(dht11_gpio_pins, global_dht11_index)
        data_flow.temperature.append((time_index, temperature))
        data_flow.humidity.append((time_index, humidity))
        data_flow.temperature = data_flow.buffer_limit(data_flow.temperature)
        data_flow.humidity = data_flow.buffer_limit(data_flow.humidity)
        time.sleep(1)
        time_index += 1


def read_max30102(data_flow: DataFlow):
    max30102_gpio_pin = int(data_flow.max30102)
    time_index = 1
    while not data_flow.stop:
        time.sleep(1.0)
        # logging.info('__read_max30102 index ' + str(time_index))
        # heart_rate = random.randint(50, 100)
        heart_rate = MAX30102.read_heart_rate(max30102_gpio_pin, 100)
        if len(data_flow.heart_rate) > 0 and heart_rate > 200 and data_flow.heart_rate[-1] < 100:
            continue
        if heart_rate < data_flow.hr_max:
            data_flow.heart_rate.append((time_index, heart_rate))
            data_flow.heart_rate = data_flow.buffer_limit(data_flow.heart_rate)
        time_index += 1


def start(dht11: str, max30102: str):
    data_flow = DataFlow(dht11, max30102)
    threading_list = list()
    dht11_th = threading.Thread(target=read_dht11, args=(data_flow,), name='dht11 thread')
    threading_list.append(dht11_th)
    dht11_th.setDaemon(True)
    dht11_th.start()
    tmp = threading.Thread(target=read_max30102, args=(data_flow,), name='max30102 thread')
    threading_list.append(tmp)
    tmp.setDaemon(True)
    tmp.start()
    return data_flow


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(filename)s[line:%(lineno)d] - %(funcName)s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    data_flow = start('37', '7')
    time.sleep(10)
    print('heart_rate')
    print(data_flow.heart_rate)
    print('temperature')
    print(data_flow.temperature)
    print('humidity')
    print(data_flow.humidity)


if __name__ == '__main__':
    main()

import logging
import time
from optparse import OptionParser

import matplotlib.pyplot as plt

import DataFlow
import RELAY
import SmartConfig


class SmartClothes:
    def __init__(self, dht11, max30102, relay):
        self.__statuses = list()
        self.__statuses.append(SmartConfig.Status.COLD)
        self.__dataflow = DataFlow.start(dht11, max30102)
        self.__relay = relay
        self.__is_smooth = True
        self.__open_relay_interval = 10
        RELAY.set_value(self.__relay, SmartConfig.Status.CLOSE)
        logging.info('SmartClothes init success')
        plt.ion()
        plt.figure(1)

    @staticmethod
    def __parse_x_y(buffer):
        x = [x[0] for x in buffer]
        y = [x[1] for x in buffer]
        return x, y

    @staticmethod
    def __smooth(buffer):
        tmp = list()
        for right in range(0, len(buffer)):
            left = max(0, right - 4)
            mean = 0
            while left <= right:
                mean += buffer[left]
                left += 1
            left = max(0, right - 4)
            mean /= (right - left + 1)
            tmp.append(mean)
        return tmp

    def __temperature(self):
        x, y = self.__parse_x_y(self.__dataflow.temperature)
        y = self.__smooth(y)
        return x, y

    def __humidity(self):
        x, y = self.__parse_x_y(self.__dataflow.humidity)
        y = self.__smooth(y)
        return x, y

    def __heart_rate(self):
        x, y = self.__parse_x_y(self.__dataflow.heart_rate)
        y = self.__smooth(y)
        return x, y

    def __query_status(self):
        # view == 'humidity':
        status = SmartConfig.Status.UNKNOWN
        # 通过humidity判断状态
        if self.__humidity()[1][-1] < SmartConfig.Humidity.down_threshold:
            status = SmartConfig.Status.COLD
        elif self.__humidity()[1][-1] > SmartConfig.Humidity.up_threshold:
            status = SmartConfig.Status.HOT
        if status == SmartConfig.Status.UNKNOWN:
            # 通过temperature判断状态
            if self.__temperature()[1][-1] < SmartConfig.Temperature.down_threshold:
                status = SmartConfig.Status.COLD
            elif self.__temperature()[1][-1] > SmartConfig.Temperature.up_threshold:
                status = SmartConfig.Status.HOT
        # 验证状态
        if status == SmartConfig.Status.COLD and self.__heart_rate()[1][-1] > 200:
            status = SmartConfig.Status.UNKNOWN
        return status

    def __should_open_relay(self, status):
        if status == SmartConfig.Status.HOT:
            max_index = len(self.__statuses)
            for index in range(max(max_index - self.__open_relay_interval, 0), max_index):
                if self.__statuses[index] == SmartConfig.Status.HOT:
                    return False
            return True
        return False

    def __open_relay(self):
        RELAY.set_value(self.__relay, SmartConfig.Status.OPEN)
        time.sleep(SmartConfig.TIMEINTERVAL)
        RELAY.set_value(self.__relay, SmartConfig.Status.CLOSE)

    def __draw(self):
        plt.clf()
        # plt.xlim、plt.ylim 设置横纵坐标轴范围
        # plt.xlabel、plt.ylabel 设置坐标轴名称
        # plt.xticks、plt.yticks 设置坐标轴刻度
        #  axes.set_* 同上
        plt.subplot(411)
        temprature_x, temprature_y = self.__temperature()
        plt.plot(temprature_x, temprature_y, color='r')
        plt.xticks(range(temprature_x[0], temprature_x[-1] + 1, 1))
        plt.yticks(range(0, 45, 5))
        plt.ylabel('temperature')
        plt.subplot(412)
        humidity_x, humidity_y = self.__humidity()
        plt.plot(humidity_x, humidity_y, color='y')
        plt.xticks(range(humidity_x[0], humidity_x[-1] + 1, 1))
        plt.yticks(range(0, 120, 10))
        plt.ylabel('humidity')
        plt.subplot(413)
        heart_rate_x, heart_rate_y = self.__heart_rate()
        plt.plot(heart_rate_x, heart_rate_y, color='g')
        plt.xticks(range(heart_rate_x[0], heart_rate_x[-1] + 1, 1))
        plt.yticks(range(0, 220, 20))
        plt.ylabel('heart_rate')
        plt.subplot(414)
        plt.axis('off')
        plt.text(0, 0, "temperature:" + str(temprature_y[-1]))
        plt.text(0.35, 0, "humidity:" + str(humidity_y[-1]))
        plt.text(0.7, 0, "heart_rate:" + str(heart_rate_y[-1]))
        if self.__statuses[-1] == SmartConfig.Status.HOT:
            plt.text(0.35, 0.3, "Status:" + "hot")
        else:
            plt.text(0.35, 0.3, "Status:" + "cold")
        plt.pause(0.5)

    def run(self):
        time.sleep(1)
        while True:
            time.sleep(2)
            cur_status = self.__query_status()
            if cur_status == SmartConfig.Status.UNKNOWN:
                continue
            if self.__should_open_relay(cur_status):
                self.__open_relay()
            self.__statuses.append(cur_status)
            self.__draw()


def parse_args():
    parser = OptionParser()
    parser.add_option(
        '--dht11',
        action='store',
        dest='dht11',
        type='str',
        default='37',
        help='dht11 gpio wiringpi pins'
    )
    parser.add_option(
        '--max30102',
        action='store',
        dest='max30102',
        type='str',
        default='7',
        help='max30102 gpio wiringpi pin'
    )
    parser.add_option(
        '--relay',
        action='store',
        dest='relay',
        type='str',
        default='12',
        help='relay gpio wiringpi pin'
    )
    parser.add_option(
        '--model',
        action='store',
        dest='model',
        type='str',
        default='physical',
        help='gpio pin model, physical or wiringpi'
    )
    parser.add_option(
        '--debug',
        action='store',
        dest='debug',
        type='int',
        default=0,
        help=' print all log'
    )
    (opt, args) = parser.parse_args()
    if opt.model == 'wiringpi':
        for key in SmartConfig.phy2wpi:
            SmartConfig.phy2wpi[key] = key
    return opt


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(filename)s[line:%(lineno)d] - %(funcName)s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    opt = parse_args()

    smart_clothes = SmartClothes(opt.dht11, opt.max30102, opt.relay)
    smart_clothes.run()


if __name__ == '__main__':
    main()

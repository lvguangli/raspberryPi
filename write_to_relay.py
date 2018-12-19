# coding=utf-8
import sys

import wiringpi as gpio


def set_value(gpio_index: int, value: int):
    gpio.wiringPiSetup()  # 初始化wiringpi库
    gpio.pinMode(gpio_index, 1)  # 设置针脚为输出状态
    gpio.digitalWrite(gpio_index, value)  # 输出电平0,1


def blink(gpio_index: int, delay: int):
    for i in range(10):
        print(i)
        set_value(gpio_index, i % 2)
        gpio.delay(delay)


def main(gpio_index=2):
    if len(sys.argv) > 1:
        gpio_index = int(sys.argv[1])
    blink(gpio_index, 500)


if __name__ == '__main__':
    main()

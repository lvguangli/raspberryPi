# raspberryPi
以下gpio 为物理位置，括号内为wpi位置,或者说明
##电子元器件与gpio引脚接线配置
pgio引脚编号可以参考文档 ./documents/gpio引脚图.png
MAX30102
心率传感器                    gpio
vcc         --------        1(3.3v)
SCL         --------        5(SCL)
SDA         --------        3(SDA)
INT         --------        7(7)
GND         --------        9(GND)

DHT11
温度湿度传感器1--------        gpio
（注：vcc通过面包板连接, 也可以使用3.3v(gpio引脚图.png 17号)）
vcc         --------        2(5v)
GND         --------        39(GND)
DAT         --------        37(25)

温度湿度传感器2--------        gpio
（注：vcc通过面包板连接）
vcc         --------        2(5v)
GND         --------        25(GND)
DAT         --------        23(14)

relay
继电器       --------        gpio
vcc         --------        4(5v)
GND         --------        6(GND)
IN          --------        12(1)





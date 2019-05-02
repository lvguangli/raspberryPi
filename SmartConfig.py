# debug = False


class Temperature:
    """
    主要用来校验人体状态
    """
    up_threshold = 27
    down_threshold = 27


class Humidity:
    """
    主要用来判断人体状态
    """
    up_threshold = 40
    down_threshold = 25


class HeartRate:
    """
    主要用来判断人体状态
    """
    up_threshold = 100
    down_threshold = 50


class Status:
    """
    主要用来描述人体状态和继电器状态
    """
    CLOSE = 0
    OPEN = 1
    COLD = 4
    HOT = 5
    UNKNOWN = 6


# coding:utf-8


# class MyConst:
#     class ConstError(TypeError):
#         pass
#
#     def __setattr__(self, name, value):
#         if name in self.__dict__:
#             raise self.ConstError("can't change const %s" % name)
#         if not name.isupper():
#             raise self.ConstError('const name "%s" is not all uppercase' % name)
#         self.__dict__[name] = value
#
#
# const = MyConst()
# const.PI = 3.14

phy2wpi = {
    3: 8,
    5: 9,
    7: 7,
    11: 0,
    13: 2,
    15: 3,
    19: 12,
    21: 13,
    23: 14,
    27: 30,
    29: 21,
    31: 22,
    33: 23,
    35: 24,
    37: 25,
    8: 15,
    10: 16,
    12: 1,
    16: 4,
    18: 5,
    22: 6,
    24: 10,
    26: 11,
    28: 31,
    32: 26,
    36: 27,
    38: 28,
    40: 29
}

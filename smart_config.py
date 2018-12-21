# debug = False


class Temperature:
    """
    主要用来校验人体状态
    """
    up_threshold = 35
    down_threshold = 20


class Humidity:
    """
    主要用来判断人体状态
    """
    up_threshold = 60
    down_threshold = 55


class HeartRate:
    """
    主要用来判断人体状态
    """
    up_threshold = 60
    down_threshold = 50


class Status:
    """
    主要用来描述人体状态和继电器状态
    """
    COLD = 1
    HOT = 2
    SPORT = 3
    UNKNOWN = 4
    OPEN = 65
    CLOSE = 66


# class DHT11:
#     wait_micros_second = 10000
#     end_micros_second = 500


# coding:utf-8


class MyConst:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


const = MyConst()
const.PI = 3.14

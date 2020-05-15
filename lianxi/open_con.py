import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]  #获取系统当前绝对值路径
configPath = os.path.join(proDir, "config.ini")
cf = configparser.ConfigParser()
cf.read(configPath)
fd = open(configPath)
data = fd.read()
print(data)
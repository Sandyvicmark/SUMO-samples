import os

initFileDir = os.path.dirname(os.path.abspath(__file__)) + '\\Temp_init.bat'
nameStr = str(input('请输入地图文件名称：\n'))
cfgFileDir = os.path.dirname(os.path.abspath(__file__)) + '\\' + nameStr + '.sumo.cfg'
initContentStr = '@echo off\nset name=' + nameStr + '\ncall converter.bat %name%\n'
cfgContentStr = "<?xml version = '1.0' encoding = 'UTF-8'?>\n<configuration xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='http://sumo.dlr.de/xsd/netconvertConfiguration.xsd'>\n    <input>\n        <net-file value='" + nameStr + ".net.xml'/>\n        <route-files value='" + nameStr + ".rou.xml'/>\n        <additional-files value='" + nameStr + ".poly.xml'/>\n    </input>\n    <time>\n        <begin value='0'/>\n        <end value='5000'/>\n    </time>\n</configuration>"

with open(initFileDir, 'w') as file:
    file.write(initContentStr)

os.system('Temp_init.bat')

with open(cfgFileDir, 'w') as file:
    file.write(cfgContentStr)
    
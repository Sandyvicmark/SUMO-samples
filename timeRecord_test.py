import os
import sys
import optparse
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
from sumolib import checkBinary
import traci


def gene_roufile():
    traci.
    roufiledir = 'timeRecord_test.rou.xml'
    por = 1./3
    num = 0
    with open(roufiledir, 'w') as file:
        print('<routes>\n    <vType id="com-car" type="passenger" length="4" accel="%f" decel="%f" maxspeed="%d"/>' \
              % (random.uniform(2.5,3.5),random.uniform(2.5,3.5),random.randint(13,20)),file = file)
        print('    <vType id="emer-car" guiShape="emergency" type="emergency" accel="%f" decel="%f" maxspeed="%d"/>' \
              % (random.uniform(1.5,2.5),random.uniform(2,3),random.randint(13,20)),file = file)

        print('    <route id="com-rou0" edges="in1 edge1 edge9 -edge11 -edge5 out5"/>', file = file)
        print('    <route id="com-rou1" edges="in1 edge1 edge2 edge3 edge4 out5"/>', file=file)
        print('    <route id="com-rou2" edges="in1 -edge8 -edge7 -edge6 -edge5 out5"/>', file=file)
        print('    <route id="com-rou3" edges="in5 edge5 edge11 -edge12 edge8 out1"/>', file=file)
        print('    <route id="com-rou4" edges="in5 -edge4 edge10 -edge9 -edge1 out1"/>', file=file)
        print('    <route id="com-rou5" edges="in5 -edge4 edge10 -edge12 edge8 out1"/>', file=file)
        print('    <route id="test-rou1" edges="edge1"/>', file=file)
        print('    <route id="test-rou2" edges="edge2"/>', file=file)
        print('    <route id="test-rou3" edges="edge3"/>', file=file)
        print('    <route id="test-rou4" edges="edge4"/>', file=file)
        print('    <route id="test-rou5" edges="edge5"/>', file=file)
        print('    <route id="test-rou6" edges="edge6"/>', file=file)
        print('    <route id="test-rou7" edges="edge7"/>', file=file)
        print('    <route id="test-rou8" edges="edge8"/>', file=file)
        print('    <route id="test-rou9" edges="edge9"/>', file=file)
        print('    <route id="test-rou10" edges="edge10"/>', file=file)
        print('    <route id="test-rou11" edges="edge11"/>', file=file)
        print('    <route id="test-rou12" edges="edge12"/>', file=file)
        print('    <route id="test-rou-1" edges="-edge1"/>', file=file)
        print('    <route id="test-rou-2" edges="-edge2"/>', file=file)
        print('    <route id="test-rou-3" edges="-edge3"/>', file=file)
        print('    <route id="test-rou-4" edges="-edge4"/>', file=file)
        print('    <route id="test-rou-5" edges="-edge5"/>', file=file)
        print('    <route id="test-rou-6" edges="-edge6"/>', file=file)
        print('    <route id="test-rou-7" edges="-edge7"/>', file=file)
        print('    <route id="test-rou-8" edges="-edge8"/>', file=file)
        print('    <route id="test-rou-9" edges="-edge9"/>', file=file)
        print('    <route id="test-rou-10" edges="-edge10"/>', file=file)
        print('    <route id="test-rou-11" edges="-edge11"/>', file=file)
        print('    <route id="test-rou-12" edges="-edge12"/>', file=file)
        N = 300000
        for i in range(N):
            if random.uniform(0,1) < por:
                print('    <vehicle id="car%d" type="com-car" depart="%d" route="com-rou%d"/>' % (num, i, random.randint(0,5)), file = file)
                num += 1
        print('</routes>\n', file = file)

def run():
    step = 0
    sum = 0
    time0 = -1
    in_buf = 0
    out_buf = -1
    outputdir = 'timeRecord_test.out.xml'
    result = []                  #一条路线内单次通过时间
    resultDic = {}
    array = []                   #最终排序队列
    testcarNum = 0               #测试过的测试车数量
    testNum = 1                  #测试次数
    with open(outputdir, 'w') as init:
        print('>>>>>>>>>>Record Started<<<<<<<<<<<', file=init)
    traci.vehicle.add('emer-car%d' % testcarNum, 'test-rou-1', 'emer-car', depart=100) #Initial
    while traci.simulation.getMinExpectedNumber():
        traci.simulationStep()
        if testcarNum == 1000:
            testcarNum = 0
            testNum += 1
            for eachEle in result:                      #计算该路径所有测试的平均时间
                sum += eachEle
            mean = sum / len(result)
            with open(outputdir, 'a') as outfile:               #将该路径平均时间写入文件
                print('The Mean Time is %f' % mean, file=outfile)
            resultDic.update({str(testNum): str(mean)})           #将该路径平均时间存入字典
            result.clear()                      #清除数据，为下次计算做准备
            sum = 0
            if testNum > 12:                    #检测是否跑完所有路径，没有再发车
                break
            traci.vehicle.add('emer-car%d' % testcarNum, 'test-rou-%d' % testNum, 'emer-car', depart=step + 1)

        if ('emer-car%d' % testcarNum) not in traci.vehicle.getIDList() and time0 > 0 and out_buf == -1:
            out_buf = 0
        if in_buf and out_buf == 0:
            time = step - time0
            result.append(time)
            testcarNum += 1
            print(testcarNum)
            if testcarNum < 1000:
                traci.vehicle.add('emer-car%d' % testcarNum, 'test-rou-%d' % testNum, 'emer-car', depart=step + 1)
            out_buf = -1
            in_buf = 0
            time0 = -1
            print('time = %d' % time)
            #with open(outputdir, 'a') as outfile:          #将同一路线每一次经过时间记录
             #   print('time = %d' % time, file=outfile)
        if ('emer-car%d' % testcarNum) in traci.vehicle.getIDList() and time0 < 0:
            in_buf = 1
            time0 = step
            print('timer0 = %d' % time0)                #显示每辆车起始时间

        step += 1
    with open(outputdir, 'a') as outfile:
        for eachKey in resultDic:
            print('No%s: %s s' % (eachKey, resultDic[eachKey]), file=outfile)
        print('The Optimum Order is:', file=outfile)
        for eachKey in sorted(resultDic, key=resultDic.__getitem__):
            print('No%s: %s s' % (eachKey, resultDic[eachKey]), file=outfile)

    traci.close(wait=False)
    sys.stdout.flush()

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary , "-c" , "timeRecord_test.sumocfg"]
gene_roufile()
traci.start(sumoCmd)
run()
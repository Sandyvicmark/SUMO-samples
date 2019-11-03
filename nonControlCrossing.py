import os
import sys
import random
import traci

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def gene_file():
    pWE = 1. / 3
    pNS = 1. / 9
    roudir = 'D:\\Program Files (x86)\\Sumo\\map\\fuzzy_tls.rou.xml'
    carnum = 0
    departTime = 0
    with open(roudir, 'w') as file:
        print(
            "<routes>\n    <vType id='car' accel='5' decel='3.5' maxSpeed='20' length='5' sigma='0.6' vClass='passenger'/>",
            file=file)
        print("    <route id='WE' edges='1o 1 -3 -3o'/>", file=file)
        print("    <route id='NS' edges='2o 2 -4 -4o'/>", file=file)
        while carnum <= 1000:
            a = random.uniform(0, 1)
            if a < pWE:
                print("    <vehicle id='%d' type='car' depart='%d' route='WE'/>" % (carnum, departTime), file=file)
                carnum += 1
            if a < pNS:
                print("    <vehicle id='%d' type='car' depart='%d' route='NS'/>" % (carnum, departTime), file=file)
                carnum += 1
            departTime += 1
        print("</routes>", file=file)


def run():
    while traci.simulation.getMinExpectedNumber():
        traci.simulationStep()



#gene_file()
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", 'fuzzy_tls.sumocfg']
traci.start(sumoCmd)
run()

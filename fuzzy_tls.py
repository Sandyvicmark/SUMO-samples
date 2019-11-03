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
    step = 0
    time = 0
    flag = 1
    curntPhase = ''
    lastPhase = ''
    traci.trafficlight.setPhase('gneJ11', 0)
    phase2passlane = {0: '2_0', 2: '1_0'}
    phase2waitlane = {0: '1_0', 2: '2_0'}
    control = {0: 0, 1: 0, 2: 0.78, 3: 2.42, 4: 3.69, 5: 5, 6: 5, 7: 5, 8: 6.8, 9: 7.8,
               0.1: -0.03, 1.1: -0.07, 2.1: 0.9, 3.1: 2.4, 4.1: 3.43, 5.1: 5, 6.1: 5, 7.1: 5, 8.1: 6.4, 9.1: 6.5,
               0.2: -0.43, 1.2: -1, 2.2: 0.35, 3.2: 2, 4.2: 3.14, 5.2: 4.6, 6.2: 4.5, 7.2: 4.2, 8.2: 5, 9.2: 5,
               0.3: -1.96, 1.3: -2.5, 2.3: -1.1, 3.3: 0.56, 4.3: 1.3, 5.3: 3, 6.3: 3, 7.3: 3.3, 8.3: 5, 9.3: 5,
               0.4: -3.95, 1.4: -3, 2.4: -2.8, 3.4: -1.5, 4.4: -0.3, 5.4: 2.5, 6.4: 2.7, 7.4: 3, 8.4: 4.7, 9.4: 5,
               0.5: -4.87, 1.5: -4.7, 2.5: -4, 3.5: -2.5, 4.5: -1.2, 5.5: 1.7, 6.5: 1.7, 7.5: 1.3, 8.5: 3, 9.5: 5,
               0.6: -5, 1.6: -5, 2.6: -4, 3.6: -3, 4.6: -3, 5.6: -0.7, 6.6: -0.3, 7.6: 0.9, 8.6: 3, 9.6: 5,
               0.7: -5, 1.7: -5, 2.7: -4.57, 3.7: -4.5, 4.7: -4.6, 5.7: -2, 6.7: -1.7, 7.7: -0.9, 8.7: 2.95, 9.7: 5,
               0.8: -5.88, 1.8: -6.4, 2.8: -4.97, 3.8: -5, 4.8: -4.9, 5.8: -2.5, 6.8: -2.2, 7.8: -1.9, 8.8: 0.6, 9.8: 3.4,
               0.9: -7.8, 1.9: -6.8, 2.9: -5, 3.9: -5, 4.9: -5, 5.9: -3.9, 6.9: -3.9, 7.9: -3.6, 8.9: -0.07, 9.9: 1.1}
    while traci.simulation.getMinExpectedNumber():
        traci.simulationStep()
        lastPhase = curntPhase
        curntPhase = traci.trafficlight.getPhase('gneJ11')
        if not (lastPhase == curntPhase):
            flag = 1
            time = 0
        if curntPhase == 2 or curntPhase == 0:
            time += 1
            # if time >= 5 and flag:
            passnmb = traci.lane.getLastStepVehicleNumber(phase2passlane[curntPhase])
            waitnmb = traci.lane.getLastStepVehicleNumber(phase2waitlane[curntPhase])
            key = round(passnmb + waitnmb * 0.1, 1)
            print(key)
            remainTime = 20 - time + 3 * control[key]
            if passnmb == 0 and waitnmb:
                remainTime = 20 - 5 * time
            print(remainTime)
            if remainTime < 0:
                remainTime = 0
            traci.trafficlight.setPhaseDuration('gneJ11', remainTime)
            flag = 0


#gene_file()
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", 'fuzzy_tls.sumocfg']
traci.start(sumoCmd)
run()

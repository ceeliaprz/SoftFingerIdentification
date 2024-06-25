from model.system_motors import SystemMotors
import time
import numpy as np
import json as js
import os
import math

def FingerInverseKinematics(incl, orien):
    #Medidas en m
    a = 0.013 #‘a' es la longitud del centro del triángulo al cables y en este caso ‘a' y ‘b' son iguales
    Lo = 0.098 # Longitud dedo en reposo
    radio = 0.008 #Radio de la polea donde se enrrolla el cable 

    # ángulos en radianes
    theta=incl*math.pi/180 
    psi=orien*math.pi/180 

    # Vector que guardará las variaciones
    v_lengths = np.zeros(2)

    if (theta!=0):
        R=Lo/theta

        phi8= (math.pi/2)-psi 
        phi7= (7*math.pi/6)-psi 
        #phi9= (11*math.pi/6)-psi # tengo que ver que orientaciones puedo alcanzar sin tener el 3 motor

        #Variaciones en los cables (L-Li)
        v_lengths[0]= theta * a * math.cos(phi8) 
        v_lengths[1]= theta * a * math.cos(phi7)
        #v_lengths[2]= theta * a * math.cos(phi9) 

    else:
        v_lengths[0]=0
        v_lengths[1]=0

    # Angulos en radianes de los motores
    posan8 = v_lengths[0]/radio #motor8
    posan7 = v_lengths[1]/radio #motor7
    # posan9 = v_lengths[2]/radio #motor9
    # print("motor 9", posan9) 

    return posan8, posan7


def main():
    # Setting the motor's position to 0
    # Motors
    #id_fingers=[1,2,4,5,7,8]
    id_fingers=[7,8]
    motors = SystemMotors(2)  # instantiate SystemMotors class >> number of motors
    motors.loadMotors(id_fingers, "SoftGripperMotorConfig.json")  # motor's ids
    print("Starting motors...")

    motors.startMotors()  # start m

    time.sleep(2)

    print("Setting up motors...")
    motors.setupPositionsMode(5, 5)  # setting velocity and acceleration values
    time.sleep(1)

    #Inclinación y orientación deseadas: mi rango de orinetaciones va de 90 a 210
    inclinacion = 30 # limite 20 grados
    orientacion = 190 

    print("Vamos a cero")

    #motors.setPositions([0,0,0,0,0,0])
    motors.setPositions([0,0])
    time.sleep(1)
    i=0
    for id in id_fingers:
        print("Initial motor "+str(id)+" position: "+str(round(motors.motorsArray[i].getPosition(),2)))
        i=i+1

    # Aquí es donde introducimos la posición a la que queremos que lleguen los motores en radianes
    posan8, posan7 = FingerInverseKinematics(inclinacion, orientacion)
    #motors.setPositions([posan1, posan2, posan1, posan2,posan1, posan2])
    motors.setPositions([posan7, -posan8])
    time.sleep(3)
    i=0
    for id in id_fingers:
        print("During motor "+str(id)+" position: "+str(round(motors.motorsArray[i].getPosition(),2)))
        i=i+1


    motors.setPositions([0,0])
    time.sleep(3)
    i=0
    for id in id_fingers:
        print("Final motor "+str(id)+" position: "+str(round(motors.motorsArray[i].getPosition(),2)))
        i=i+1


if __name__ == "__main__":
    main()
#python3 -m pip install modbus-tk
import os
import time
import json
import serial
import threading
import modbus_tk.defines as cts
from modbus_tk import modbus_rtu
from tkinter import *
from tkinter.ttk import *

raiz = Tk()
raiz.title("EMC Energy Meassurement Control")
raiz.resizable(True,True)
raiz.geometry("400x400")

myFrame = Frame(raiz, width=400, height=400)
myFrame.pack()

voltaje = StringVar()
current = StringVar()
power = StringVar()
energy = StringVar()
frecuency = StringVar()
powerfact = StringVar()
alarm = StringVar()
pzem = StringVar()

voltajeLabel = Label(myFrame, text="Voltaje")
voltajeLabel.grid(row=0, column=0, sticky="w", padx=10, pady=10)
voltajeEntry = Entry(myFrame, textvariable=voltaje)
voltajeEntry.grid(row=0, column=1, sticky="e", padx=10, pady=10)

currentLabel = Label(myFrame, text="Current A")
currentLabel.grid(row=1, column=0, sticky="w", padx=10, pady=10)
currentEntry=Entry(myFrame, textvariable =current)
currentEntry.grid(row=1, column=1, sticky="e", padx=10, pady=10)

powerLabel = Label(myFrame, text="Power W")
powerLabel.grid(row=2, column=0, sticky="w", padx=10, pady=10)
powerEntry=Entry(myFrame, textvariable=power)
powerEntry.grid(row=2, column=1, sticky="e", padx=10, pady=10)

energyLabel = Label(myFrame, text="Energy Wh")
energyLabel.grid(row=3, column=0, sticky="w", padx=10, pady=10)
energyEntry=Entry(myFrame,textvariable=energy)
energyEntry.grid(row=3, column=1, sticky="e", padx=10, pady=10)

frecuencyLabel = Label(myFrame, text="Frecuency")
frecuencyLabel.grid(row=4, column=0, sticky="w", padx=10, pady=10)
frecuencyEntry=Entry(myFrame,textvariable=frecuency)
frecuencyEntry.grid(row=4, column=1, sticky="e", padx=10, pady=10)

powerfactorLabel = Label(myFrame, text="Power Factor")
powerfactorLabel.grid(row=5, column=0, sticky="w", padx=10, pady=10)
powerfactorEntry=Entry(myFrame, textvariable=powerfact)
powerfactorEntry.grid(row=5, column=1, sticky="e", padx=10, pady=10)

alarmLabel = Label(myFrame, text="Alarm")
alarmLabel.grid(row=6, column=0, sticky="w", padx=10, pady=10)
alarmEntry=Entry(myFrame, textvariable=alarm)
alarmEntry.grid(row=6, column=1, sticky="e", padx=10, pady=10)

pzemLabel = Label(myFrame, text="PZEM_status")
pzemLabel.grid(row=7, column=0, sticky="w", padx=10, pady=10)
pzemEntry=Entry(myFrame, textvariable=pzem)
pzemEntry.grid(row=7, column=1, sticky="e", padx=10, pady=10)



COM_PORT = '/dev/ttyUSB0'   #/dev/ttyUSB0  in case ubuntu
BAUD_RATE = 9600
BYTE_SIZE = 8
PARITY = 'N'
STOP_BITS = 1
XON_XOFF = 0

#if __name__ == 'main':
#connect to serial slave
dict_payload = dict()
dict_payload['voltaje']=0
dict_payload['current_A']= 0
dict_payload['power_W'] = 0
dict_payload['energy_Wh'] = 0
dict_payload['frecuency'] = 0
dict_payload['power_factor'] = 0
dict_payload['alarm'] = 0
dict_payload['PZEM_status'] = 'NO-CONNECTED'
dict_payload['coment'] = ' '

stop = False

def detener():
	global stop
	stop = True
	#print(stop) 

def continuar():
	global stop
	stop = False
	lectura()

def lectura():

	try:
		seriala = serial.Serial(port=COM_PORT,baudrate=BAUD_RATE,bytesize=BYTE_SIZE,parity=PARITY,stopbits=STOP_BITS,xonxoff=XON_XOFF)
		master = modbus_rtu.RtuMaster(serial=seriala)
		master.set_timeout(2.0)
		master.set_verbose(True)

		#while(True):
		    
		    #print(',cts.READ_INPUT_REGISTERS: ',str(cts.READ_INPUT_REGISTERS))
		    #print('Entro master: ',str(master))
		data = master.execute(1,cts.READ_INPUT_REGISTERS,0,10)
		#print('data: ',str(data))
		dict_payload['voltaje']=data[0] / 10.0
		dict_payload['current_A']= (data[1] + (data[2]<<16) ) / 1000.0  #byte 1 & 2 Amps
		dict_payload['power_W'] = (data[3] + (data[4]<<16) ) / 10.0     #Byte 1 & 4 Waths / 10
		dict_payload['energy_Wh'] = (data[5] + (data[6]<<16) )          #Bytes 5 & 6 [Wh]
		dict_payload['frecuency'] = (data[7] / 10.0)          #Bytes 7 [Hz]
		dict_payload['power_factor'] = (data[8] / 100.0)          #Bytes 8
		dict_payload['alarm'] = (data[9])          #Bytes 9
		dict_payload['PZEM_status'] = 'CONNECTED'
		print(dict_payload)
		print(stop)
		    #print('\nVoltaje: %.2f' % (dict_payload['voltage']))
		    #print('Current: %.2f'% (dict_payload['current_A']))
		    #print('Power: %.2f' % (dict_payload['power_W']))
		    #print('Energy: %.2f' % (dict_payload['energy_Wh']))
		    #print('Frecuency: %.2f' % (dict_payload['frecuency']))
		    #print('Power_factor: %.2f' % (dict_payload['power_factor']))
		    #print('Alarm: %.2f' % (dict_payload['alarm']))
		voltaje.set(dict_payload['voltaje'])
		current.set(dict_payload['current_A'])
		power.set(dict_payload['power_W'])
		energy.set(dict_payload['energy_Wh'])
		frecuency.set(dict_payload['frecuency'])
		powerfact.set(dict_payload['power_factor'])
		alarm.set(dict_payload['alarm'])
		pzem.set(dict_payload['PZEM_status'])
		    #time.sleep(1)		    	

	except KeyboardInterrupt:
	    dict_payload['PZEM_status'] = 'DISCONNECTED'
	    dict_payload['coment'] = 'Exit from the terminal'
	    #print(dict_payload)
	    print('Keyboard')
	except Exception as e:
	    dict_payload['PZEM_status'] = 'DISCONNECTED'
	    dict_payload['coment'] = 'Exception: '+ str(e)
	    print('Exception: ',str(e))
	finally:
	    #dict_payload['status'] = 'DISCONNECTED'
	    #dict_payload['coment'] = 'Si este'
	    #print('Finally')
	    #print(dict_payload)
	    with open('result.json', 'w') as file:
	        json.dump(dict_payload, file, indent=4)
	    master.close()
	    
	    if(stop==False):
	        raiz.after(1000, lectura)
		

#th= threading.Thread(target=lectura)
#th.start
button = Button(raiz, text="Read", command=continuar)
button.pack()

button = Button(raiz, text="Stop", command=detener)
button.pack()

raiz.mainloop()



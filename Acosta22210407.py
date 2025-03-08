"""
Práctica 0: Mecánica pulmonar


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno:Perez Castillo Natalie Jaqueline
Número de control: 22210425
Correo institucional

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot


# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,6,3
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N) #escalón unitario
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 #Impulso
u3 = (np.linspace(0,tend,N))/tend # Rampa con pendiente 1/10
u4 = np.sin(m.pi/2*t) #Función sinusoidal, pi/2 = 250 mHz

u = np.stack((u1,u2,u3,u4), axis = 1)
signal = ['Escalón','Impulso','Rampa','Sin']

# Componentes del circuito RLC y función de transferencia
R = 5E3
L = 470E-6
C = 100E-6
num = [C*L*R,(C*(R*R))+L,R]
den = [3*R*C*L,(5*C*(R*R))+ L,2*R]
sys = ctrl.tf(num,den)
print(sys)

# Componentes del controlador
Cr = 10E-6
kI= 297.7835
Re = 1/(kI*Cr); print ('Re =',Re)
numPID = [1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(PID)


# Sistema de control en lazo cerrado
X = ctrl.series(PID,sys)
sysPID = ctrl.feedback(X,1, sign = -1)
print(sysPID)

# Respuesta del sistema en lazo abierto y en lazo cerrado

rosa = [255/255, 32/255, 78/255]
rosamasrosa = [160/255, 21/255, 62/255]
morado = [93/255, 14/255, 65/255]
azul = [0/255, 34/255, 77/255]

fig1 = plt.figure();
plt.plot(t,u1,'-', color = azul, label = 'Ve(t)')
_, PA = ctrl.forced_response(sys,t,u1,x0)
plt.plot(t,PA,'-', color = rosa, label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u1,x0)
plt.plot(t,VPID,":", linewidth =3 , color= [0/255, 34/255, 77/255], label= "VI(t)")
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel("t[s]", fontsize = 11)
plt.ylabel("Vi(t) [V]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = "center", ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig1.savefig("esca.pdf",bbox_inches = "tight")


fig2 = plt.figure();
plt.plot(t,u2,'-', color = morado, label = 'Ve(t)')
_, PA = ctrl.forced_response(sys,t,u2,x0)
plt.plot(t,PA,'-', color = rosamasrosa, label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u2,x0)
plt.plot(t,VPID,":", linewidth =3 , color= [0/255, 34/255, 77/255], label= "VI(t)")
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel("t[s]", fontsize = 11)
plt.ylabel("Vi(t) [V]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = "center", ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig2.savefig("puls.pdf",bbox_inches = "tight")

fig3 = plt.figure();
plt.plot(t,u3,'-', color = rosamasrosa, label = 'Ve(t)')
_, PA = ctrl.forced_response(sys,t,u3,x0)
plt.plot(t,PA,'-', color = morado, label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u3,x0)
plt.plot(t,VPID,":", linewidth =3 , color= [0/255, 34/255, 77/255], label= "VI(t)")
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel("t[s]", fontsize = 11)
plt.ylabel("Vi(t) [V]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = "center", ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig3.savefig("rampa.pdf",bbox_inches = "tight")

fig4 = plt.figure();
plt.plot(t,u4,'-', color = rosa, label = 'Ve(t)')
_, PA = ctrl.forced_response(sys,t,u4,x0)
plt.plot(t,PA,'-', color = azul, label = 'Vs(t)')
_,VPID = ctrl.forced_response(sysPID,t,u4,x0)
plt.plot(t,VPID,":", linewidth =3 , color= [0/255, 34/255, 77/255], label= "VI(t)")
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2);plt.yticks(np.arange(-1,1.2,0.1))
plt.xlabel("t[s]", fontsize = 11)
plt.ylabel("Vi(t) [V]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = "center", ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig4.savefig("sinu.pdf",bbox_inches = "tight")
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:16:04 2016

@author: Carlosjunior
"""

#imports
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy import linspace 
from numpy import linalg 
from numpy import multiply 
from numpy import arange
from numpy import cross
import math

#constantes
#p = 0.25
#p = 0.25
#r = 35 * 10 ** -2 #m
#Area = 4 * math.pi * r ** 2 #m2
#g = 10 # m/s**2
#m = 430 * 10 ** -3 #kg
#s = 200 #rpm

def forca_drag(V,r,Area): # V = [vx,vy,vz]
    v = linalg.norm(V)
    
    v_versor =  V/v
    
    f_c = - p * Area * v**2 / 2
    
    f = multiply(f_c,  v_versor)
    
    return f
    
def forca_magnus(V): #V = [vx,vy,vz]
    v = linalg.norm(V)
    
    v_versor = V/v
    w = [0,0,1]
    
    versor = cross(w,v_versor)
    f_d = (4/3)* (4 *math.pi * r ** 3 * p * v * s)
    
    f = multiply(f_d, versor)
    
    return f
    

def func(A,t): #A=[x,y,z,vx,vy,vz]
    dxdt = A[3]
    dydt = A[4]
    dzdt = A[5]
    V = [A[3],A[4],A[5]]
    
    Fmagnus = forca_magnus(V)
    Fdrag = forca_drag(V,r,Area)
    
    dvxdt = + (Fdrag[0]/m) + (Fmagnus[0]/m) 
    dvydt =  + (Fmagnus[1]/m) + (Fdrag[1]/m)
    dvzdt = -g + (Fdrag[2]/m)
    return [dxdt,dydt,dzdt,dvxdt,dvydt,dvzdt]


    
#Constantes
p = 0.25
r = 0.11 #m
Area = 4 * math.pi * r ** 2 #m2
g = 9.8 # m/s**2
m = 430 * 10 ** -3 #kg 430
s = 3.3 #Hz

#Valores iniciais
teta = 0.295765
v0 = 30.48
vx = v0 * math.cos(teta)#2.6565
vy =  0
vz = v0 * math.sin(teta)#30.640
x = 0
y = 0
z = 0
V = [vx,vy,vz]



#Implementação
Y0 = [x,y,z,vx,vy,vz]
T = linspace(0,1.4,16)
y0 = odeint(func,Y0,T)


#Listas dos Espaços e Velocidade
velocidade = []
Sz = y0[:,2]
Sy = []
Sx = y0[:,0]
velz = y0[:,5]
vely = y0[:,4]
velx = y0[:,3]

for i in range(len(Sx)):
    velocidade.append(math.sqrt(y0[:,3][i]**2 + y0[:,4][i]**2 +y0[:,5][i]**2))
    Sy.append(-y0[:,1][i])

#print("A altura maxima da bola é {0}.".format(max(Sz)))
#
#for i in range(len(Sz)):
#    print("Na posição {0} em z, o tempo é {1}.".format(Sz[i],T[i]))    
#    if Sz[i] <= 0:
#        print("Deu errado irmão")
  
#======================Gráfico da posicao de y por z==============================================    

plt.plot(y0[:,1], y0[:,2],'o',color = 'black')
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Visão do goleiro')
plt.xlabel('Espaço y[m]')
plt.ylabel('Espaço z[m]')

plt.grid()
plt.show()



#======================Gráfico da posicao de y por x==============================================    
#for i in range(len(Sx)):
#    print("({0},{1})".format(Sx[i],Sy[i]))
plt.plot(y0[:,1], y0[:,0],'o',color = 'black')
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Visão de cima do campo')
plt.xlabel('Espaço y[m]')
plt.ylabel('Espaço x[m]')

plt.grid()
plt.show()

#======================Gráfico da posicao z por x==============================================
plt.plot(y0[:,0], y0[:,2],'o',color = 'black',)
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Visão do banco de reservas')
plt.xlabel('Espaço x[m]')
plt.ylabel('Espaço z[m]')

plt.grid()
plt.show()

#======================Gráfico da posicao x, y e z==============================================

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(Sx, Sy, Sz, label='Movimento da bola',marker = 'o',color = 'black')
ax.set_xlabel('Posição em x')
ax.set_ylabel('Posição em y')
ax.set_zlabel('Posicção em z')
ax.legend()

plt.show()

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(y0[:,0], y0[:,1], Sz, label='Movimento da bola',marker = 'o',color = 'black')
ax.set_xlabel('Posição em x')
ax.set_ylabel('Posição em y')
ax.set_zlabel('Posicção em z')
ax.legend()

plt.show()

#======================Gráfico da posicao de y pelo tempo==============================================
plt.plot(T,y0[:,1],'-',label = 'Posição em y')
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Gráfcos das posições em y')
plt.xlabel('Tempo[s]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()


#======================Gráfico da posicao de x e z pelo tempo==============================================
plt.plot(T,y0[:,0],'-',label = 'Posição em x')
plt.plot(T,y0[:,2],'-',label = 'Posição em z')
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Gráfcos das posições em x e z')
plt.xlabel('Tempo[s]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()


#======================Gráfico da posicao de v, vx e vz pelo tempo==============================================
plt.plot(T,velocidade,'-',label = 'Velocidade')
plt.plot(T,y0[:,3],'-',label = 'Velocidade em x')
plt.plot(T,y0[:,5],'-',label = 'Velocidade em z')
plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1))
plt.title('Gráfcos das velocidades em x e z')
plt.xlabel('Tempo[s]')
plt.ylabel('Velocidade[m/s]')

plt.grid()
plt.show()


#======================Gráfico da posicao de v e vy pelo tempo==============================================
#plt.plot(T,velocidade,'-',label = 'Velocidade')
plt.plot(T,y0[:,4],'-',label = 'Velocidade em y')
plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1))
plt.title('Gráfcos das velocidades em x e z')
plt.xlabel('Tempo[s]')
plt.ylabel('Velocidade[m/s]')

plt.grid()
plt.show()

#__________________________________________________________________________________________________________




#======================Figura de mérito==============================================

merito = []
merito.append(max(Sz))
merito2 = []
merito2.append(max(Sx))
tetas = []
tetas.append(teta)
for i in range(1,10):
    teta-=math.pi/180
    tetas.append(teta)

    #Inicio
    v0 = 30.48
    vx = v0 * math.cos(teta)#2.6565
    vy =  0
    vz = v0 * math.sin(teta)#30.640
    x = 0
    y = 0
    z = 0
    V = [vx,vy,vz]
    Y = [x,y,z,vx,vy,vz]


    
    y =  odeint(func,Y,T)
    
    #Listas
    velocidade = []
    Sz = y[:,2]
    Sy = y[:,1]
    Sx = y[:,0]
    velz = y[:,5]
    vely = y[:,4]
    velx = y[:,3]
    for i in range(len(Sx)):
        velocidade.append(math.sqrt(y[:,3][i]**2 + y[:,4][i]**2 +y[:,5][i]**2))
    merito.append(max(Sz))
    merito2.append(max(Sx))
    if i%2 == 0:
        plt.plot(T,y0[:,0],'-',label = 'Posição em x')
        plt.plot(T,y0[:,2],'-',label = 'Posição em z')
        plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
        plt.title('Gráfcos das posições em x e z')
        plt.xlabel('Tempo[s]')
        plt.ylabel('Espaço[m]')
        
        plt.grid()
        plt.show()

  
plt.plot(tetas,merito,'o',label = '',c = 'r')
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Gráfcos da altura máxima da bola')
plt.xlabel('Tetas[rad]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()
    
plt.plot(tetas,merito2,'o',label = '',c = 'g')
plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
plt.title('Gráfcos da distância máxima da bola')
plt.xlabel('Tetas[rad]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()
    
    

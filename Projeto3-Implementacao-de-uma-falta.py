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
def gra_rad(teta):
    ang = teta * math.pi/180
    return ang

def forca_drag(V,r,Area): # V = [vx,vy,vz]
    v = linalg.norm(V)
    
    v_versor =  V/v
    
    f_c =  p * Area * v**2 / 2
    
    f = multiply(f_c, - v_versor)
    
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
    
    dvxdt = (Fdrag[0]/m) + (Fmagnus[0]/m) 
    dvydt =   (Fmagnus[1]/m) + (Fdrag[1]/m)
    dvzdt = -g + (Fdrag[2]/m)
    return [dxdt,dydt,dzdt,dvxdt,dvydt,dvzdt]


#Dados para a validacao

td = [
0.03,
0.1,
0.17,
0.23,
0.3, 
0.33,
0.4,
0.47,  
0.53, 
0.57,
0.63, 
0.67,
0.73, 
0.8, 
0.83, 
0.9, 
0.93, 
1.0,  
1.07,
1.13, 
1.2,  
1.27, 
1.3,  
1.37,
1.43]

yr = [
-0.11338987,
2.3404646,
4.1523185,
5.91356,
7.624514,
8.882342,
10.24107,
11.197501,
12.455438,
13.712832,
14.869869,
15.675331,
16.182221,
16.937568,
17.594963,
18.004834,
18.563052,
19.424142,
20.932105,
21.490713,
22.499825,
23.709327,
24.164413,
25.519717,
25.975735,
]

xr = [
0.004234587,
0.12618159,
0.20462011,
0.26616883,
0.3277297,
0.36123002,
0.41160792,
0.46208298,
0.50121725,
0.51218164,
0.53443825,
0.5793158,
0.5790244,
0.5731597,
0.5841241,
0.5893452,
0.5833591,
0.5772516,
0.5430835,
0.49761102,
0.46339434,
0.3896913,
0.31053638,
0.24264942,
0.152178,
]

#for a in td:
#    yr.append(float("{0:.2f}".format(a)))
#print(len(td),len(xr))
#Constantes
p = 0.25
r = 0.11 #m
Area = 4 * math.pi * r ** 2 #m2
g = 9.8 # m/s**2
m = 430 * 10 ** -3 #kg 430
s = 11 #Hz

#Valores iniciais
teta = gra_rad(15)
#teta = 0.295765
v0 = 30#30.48
vx = 2.5
vy = v0 * math.cos(teta)#2.6565
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
    Sy.append(- y0[:,1][i])
#print(Sy)
#print("A altura maxima da bola é {0}.".format(max(Sz)))
#
#for i in range(len(Sz)):
#    print("Na posição {0} em z, o tempo é {1}.".format(Sz[i],T[i]))    
#    if Sz[i] <= 0:
#        print("Deu errado irmão")
  
#======================Gráfico da posicao de y por z==============================================    

plt.plot(y0[:,0], y0[:,2],'o',color = 'black')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Visão do Roberto Carlos')
plt.xlabel('Espaço y[m]')
plt.ylabel('Espaço z[m]')
plt.axis([0,0.7,0,2])


plt.grid()
plt.show()



#======================Gráfico da posicao de y por x==============================================    
#for i in range(len(Sx)):
#    print("({0},{1})".format(Sx[i],Sy[i]))

plt.plot(y0[:,1],y0[:,0],'-',color = 'black')
plt.plot(yr,xr,'o',color = 'blue',label = 'Bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Visão de cima do campo')
plt.xlabel('Espaço y[m]')
plt.ylabel('Espaço x[m]')

plt.grid()
plt.show()

#======================Gráfico da posicao z por x==============================================
plt.plot(y0[:,1], y0[:,2],'o',color = 'black',label = 'Bola implementação')
#plt.plot(xr,zr,'o',color = 'blue',label = 'Bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Visão do banco de reservas')
plt.xlabel('Espaço x[m]')
plt.ylabel('Espaço z[m]')
#plt.axis([-0.15,25,-0.15,2.5])

plt.grid()
plt.show()

#======================Gráfico da posicao x, y e z==============================================

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(y0[:,0], y0[:,1], y0[:,2], label='Movimento da bola',marker = 'o',color = 'black')
ax.set_xlabel('Posição em x')
ax.set_ylabel('Posição em y')
ax.set_zlabel('Posicção em z')
ax.legend()

plt.show()

#======================Gráfico da posicao de y pelo tempo==============================================
plt.plot(T,y0[:,1],'-',label = 'Posição em y',c='y')
plt.plot(td,yr,'o',color = 'blue',label = 'Posição y da bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das posições em y')
plt.xlabel('Tempo[s]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()


#======================Gráfico da posicao de x  pelo tempo==============================================
plt.plot(T,y0[:,0],'-',label = 'Posição em x',c='red')
plt.plot(td,xr,'o',color = 'blue',label = 'Posição x da bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das posições em x')
plt.xlabel('Tempo[s]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()

#======================Gráfico da posicao de z  pelo tempo==============================================
plt.plot(T,y0[:,2],'-',label = 'Posição em z',c='green')
#plt.plot(td,zr,'o',color = 'blue',label = 'Posição z da bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das posições em z')
plt.axis([0,1.4,0,2])
plt.xlabel('Tempo[s]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()


#======================Gráfico da posicao de v pelo tempo==============================================
plt.plot(T,velocidade,'-',label = 'Velocidade',c='black')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das velocidades')
plt.xlabel('Tempo[s]')
plt.ylabel('Velocidade[m/s]')


plt.grid()
plt.show()

#======================Gráfico da posicao de vx pelo tempo==============================================
plt.plot(T,y0[:,3],'-',label = 'Velocidade em x',c='r')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das velocidades em x')
plt.xlabel('Tempo[s]')
plt.ylabel('Velocidade[m/s]')


plt.grid()
plt.show()

#======================Gráfico da posicao de vz pelo tempo==============================================
plt.plot(T,y0[:,5],'-',label = 'Velocidade em z',c='green')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das velocidades em z')
plt.xlabel('Tempo[s]')
plt.ylabel('Velocidade[m/s]')


plt.grid()
plt.show()


#======================Gráfico da posicao de v e vy pelo tempo==============================================
#plt.plot(T,velocidade,'-',label = 'Velocidade')
plt.plot(T,y0[:,4],'-',label = 'Velocidade em y',c='y')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos das velocidades em y')
plt.xlabel('Tempo[s]')
plt.ylabel('Velocidade[m/s]')

plt.grid()
plt.show()

#__________________________________________________________________________________________________________




#======================Figura de mérito==============================================
def rad_gra(teta):
    ang=180*teta/math.pi
    return ang
merito = []
merito.append(max(Sz))
merito2 = []
merito2.append(max(Sx))
tetas = []
#teta = gra_rad(16.5)
ang = rad_gra(teta)
tetas.append(ang)
#tetas.append(teta)
for i in range(1,10):
    print(teta)
    teta -= math.pi * 0.5/180
    
    v0 = 31.48
    vx = 2.7
    vy = v0 * math.cos(teta)#2.6565
    vz = v0 * math.sin(teta)#30.640
    x = 0
    y = 0
    z = 0
    V = [vx,vy,vz]
    ang = rad_gra(teta)
    print(ang)
    tetas.append(ang)
    
    #Implementação
    Y0 = [x,y,z,vx,vy,vz]
    T = linspace(0,1.3,16)
    y = odeint(func,Y0,T)
    
    
    #Listas dos Espaços e Velocidade
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
    merito2.append(max(Sy))

#for i in range(len(merito)):
#    if merito[i] >= 1.8:
#        print(tetas[i])
        

plt.plot(tetas,merito,'o',label = '',c = 'r')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos da altura máxima da bola')
plt.xlabel('ß [º]')
plt.ylabel('Espaço[m]')

plt.grid()
plt.show()
    
plt.plot(tetas,merito2,'o',label = '',c = 'g')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1))
plt.title('Gráficos da distância máxima da bola')
plt.xlabel('ß [º]')
plt.ylabel('Espaço[m]')
plt.axis([0,25,22.6,23.2])

plt.grid()
plt.show()
    
    

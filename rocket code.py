# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 14:17:15 2025

@author: dumj7
"""

import numpy as np
from matplotlib import pyplot as plt
import pint
ur=pint.UnitRegistry()

emptymass=29500*ur.kg
payload=2000*ur.kg
fuelmass=500000*ur.kg
TSFC=0.00035*ur.s/ur.kg
Fullthrust=7600000*ur.N
G=6.674*10**-11*ur.m**3/(ur.kg*ur.s**2)
VenusMass=4.867*10**24*ur.kg
dvenus=12104000*ur.m
vsurface=100*ur.m/ur.s
pos=np.array((dvenus.to(ur.m).magnitude/2.0,0.0))*ur.m
vel=np.array((vsurface.magnitude,0))*ur.m/ur.s
T_angle=(30.0)*ur.degree
horiT_direc=(np.cos((T_angle.to(ur.rad)).magnitude))
vertT_direc=(np.sin((T_angle.to(ur.rad)).magnitude))
T_direc=(horiT_direc,vertT_direc)
plt.ion()
fig=plt.figure()
plt.axis((6e6,7.5e6,-1e6,1e6))
plt.grid(True)
venus=plt.Circle((0,0),float(dvenus/2.0/ur.m),color='y')
fig.gca().add_artist(venus)
x=np.cos(T_angle.to(ur.rad))
y=np.sin(T_angle.to(ur.rad))
arrowplt = plt.arrow(pos[0].magnitude, pos[1].magnitude,x*50000,y*50000,width=30000)
plt.show()
def event_handler(event):
    global T_angle
    if event.key==',': #press comma to rotate left
    #Rotate left (increase angle)
        T_angle += 10.0*ur.degree
        pass
    elif event.key==',': # press period to rotate right
    # Rotate right(decrease angle)
        T_angle-=10.0*ur.degree
        pass
    elif hasattr(event,'button') and event.button==1:
        if event.xdata < 0.0:
            #Click on left-half of plot to
            #Rotate left (increase angle)
            T_angle += 100.0*ur.degree
            pass
        else:
            # Click on right-half of plot to
            #Rotate right (decrease angle)
            T_angle-=10.0*ur.degree
            pass
        pass
    
    pass
#Connect this event handler to the figure so it is called
#when the mouse is clicked or keys are pressed.
fig.canvas.mpl_connect('key_press_event',event_handler)
fig.canvas.mpl_connect('button_press_event', event_handler)
dt=1*ur.s
time=np.arange(0,500+dt.magnitude,dt.magnitude)*ur.s
mass_history=np.zeros(len(time.magnitude))*ur.kg

if fuelmass >0:
    dt=1*ur.s
    dm=(-TSFC.magnitude*Fullthrust.magnitude)*dt.magnitude*ur.kg
    fuelmass=fuelmass+dm

if fuelmass<0:
    dt=10*ur.s
    fuelmass=0*ur.kg

total_mass=emptymass+payload+fuelmass

if fuelmass >0:
    plt.axis((5.5e6,8e6,-1.6e6,1e6))
    
if fuelmass<0:
    plt.axis((-1e7,1e7,-1e7,1e7))

def norm(vec):
    return np.sqrt(np.sum(vec**2.0))
r=norm(pos)
m1=VenusMass
m2=total_mass
Fgrav=(G*m1*m2)/(r**2)

Direc_Gravity=-(pos)/r
Vec_Gravity=Fgrav*Direc_Gravity

if fuelmass >0:
    Vec_Thrust=Fullthrust*T_direc
if fuelmass <0:
    Fthrust=0
    Vec_Thrust=0*ur.N*T_direc

if fuelmass >0:
    dt=1*ur.s
    dm=(-TSFC.magnitude*Fullthrust.magnitude)*dt.magnitude*ur.kg
    fuelmass=fuelmass+dm

if fuelmass<0:
    dt=10*ur.s
    fuelmass=0  

F_rocket=Vec_Gravity+Vec_Thrust
acceleration=F_rocket/total_mass
dv=(acceleration*dt)
vel=vel+dv
dpos=vel*dt
pos=pos+dpos
t=0*ur.s
while t<3600*ur.s:
      arrowplt.remove()
      T_angle=(30.0)*ur.degree
      horiT_direc=(np.cos((T_angle.to(ur.rad)).magnitude))
      vertT_direc=(np.sin((T_angle.to(ur.rad)).magnitude))
      T_direc=(horiT_direc,vertT_direc)

      x=np.cos(T_angle.to(ur.rad))
      y=np.sin(T_angle.to(ur.rad))
      arrowplt = plt.arrow(pos[0].magnitude, pos[1].magnitude,x*500000,y*500000,width=300000)
      plt.title("Fuel remaining %f kg" %(fuelmass.magnitude))
      plt.xlabel("time=%f s"%(t.magnitude))
      if fuelmass >0:
          plt.axis((5.5e6,8e6,-1.6e6,1e6))
         
      if fuelmass<=0:
          plt.axis((-1e7,1e7,-1e7,1e7))
      fig.canvas.draw()
      fig.canvas.flush_events()
           
      if fuelmass >0:
          dt=1*ur.s
          dm=(-TSFC.magnitude*Fullthrust.magnitude)*dt.magnitude*ur.kg
          fuelmass=fuelmass+dm
    
      if fuelmass<=0:
          dt=10*ur.s
          fuelmass=0*ur.kg

      total_mass=emptymass+payload+fuelmass
      r=norm(pos)
      m1=VenusMass
      m2=total_mass
      Fgrav=(G*m1*m2)/(r**2)

      Direc_Gravity=-(pos)/r
      Vec_Gravity=Fgrav*Direc_Gravity
 
      if fuelmass >0:
          Vec_Thrust=Fullthrust*T_direc
      if fuelmass <=0:
          Fthrust=0*ur.N
          Vec_Thrust=0*ur.N*T_direc

     
      F_rocket=Vec_Gravity+Vec_Thrust
      acceleration=F_rocket/total_mass
      dv=(acceleration*dt)
      vel=vel+dv
      dpos=vel*dt
      pos=pos+dpos
      t=t+dt

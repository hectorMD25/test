from gekko import GEKKO
import numpy as np
#import matplotlib.pyplot as plt
m = GEKKO()
m.solver_options = ['max_iter 500']#,'max_cpu_time 100']
nt = 501
tm = np.linspace(0,1,nt)
m.time = tm
#m.options.SOLVER=1 #compare all solvers



#variables

#initialMass = m.Const(value=10)
v = m.Var(name='v',value=0.) #speed
h = m.Var(name='h', value=50.) #height
mass = m.Var(name='m', value=10, lb=0., ub=10) #mass
g = m.Const(value=1.625) #gravitational acceleration
k = m.Const(value=0.1)
power = m.Const(value=10.)


#MV

alpha = m.MV(value=0.2, lb=0.2, ub=1.) #control variable
alpha.STATUS = 1

#FV

tf = m.FV(value=12, lb=0.01)#, ub=100000)
tf.STATUS = 1 # the value can be adjusted by the optimizer

p = np.zeros(nt)
p[-1] = 1.
final = m.Param(value=p)


#print(tf.value*(-g+2*alpha*g*power/mass).value)


#Equations

m.Equation(v.dt() == tf*(-g+2*alpha*g*power/mass))
m.Equation(h.dt() == tf*v)
m.Equation(mass.dt() == -tf*k*alpha)

m.Equation(h*final == 0.)
#m.fix_final(h, 0.0)
m.Equation(v*final == 0.)
#m.fix_final(v, 0.0)
m.Equation(mass*final >= 0.)

m.Obj(tf)
#m.Obj(10-mass)
#m.Maximize(10-mass)

m.options.IMODE = 6#6
m.solve(disp=False)

print('Solution')
print('Final time: '+str(tf.value[0]))



#plt.figure(1)
#plt.plot(tm,h.value,'k-')#,LineWidth=2,label=r'$h$')
#plt.plot(tm,v.value,'b-')#,LineWidth=2,label=r'$v$')
#plt.plot(tm,mass.value,'g--')#,LineWidth=2,label=r'$m$')
#plt.plot(tm,alpha.value,'r--')#,LineWidth=2,label=r'$\alpha$')
#plt.legend(loc='best')
#plt.xlabel('Time')
#plt.ylabel('Value')
#plt.show()

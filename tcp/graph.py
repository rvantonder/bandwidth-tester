import random as r
import time
from pylab import *
from numpy import *

ion()

tstart = time.time()               # for profiling
x = arange(0,100,1)            # x-array
y = []

while len(y) < 100:
  y.append(r.random()*100) 

line, = plot(x,y)

while 1:
     time.sleep(.5)
     y.pop(0)
     y.append(r.random()*100)
     line.set_ydata(y)  # update the data
     draw()                         # redraw the canvas

print 'FPS:' , 200/(time.time()-tstart)


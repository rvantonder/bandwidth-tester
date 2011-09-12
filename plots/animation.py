from pylab import *
import time
import random

ion()

tstart = time.time()               # for profiling
x = arange(0,2*pi,0.01)            # x-array
print x
y = zeros((x.shape))
#print y

line, = plot(x,sin(x))
draw()
for i in arange(1,300):
    time.sleep(.5)
    line.set_ydata(sin(x+i/10.0))  # update the data
    #y += .2
    #print y
    #line.set_ydata(y)
    #line.set_ydata(int(random.random()))
    draw()                         # redraw the canvas

print 'FPS:' , 200/(time.time()-tstart)


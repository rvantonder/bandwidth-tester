import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()
#mu, sigma = 100, 15
fig = plt.figure()
#x = mu + sigma*np.random.randn(10000)
x = np.arange(0,5,.1)
y = np.zeros((x.shape))
print x.shape
print y.shape
for i in range(350):
    #x = mu + sigma*np.random.randn(10000)
    #n, bins = np.histogram(x, bins, normed=True)
    #for rect,h in zip(patches,n):
    #    rect.set_height(h)
#    time.sleep(.1)
    y[0:i] += x[0:i]
    line = plt.plot(x,y)
    fig.canvas.draw()
    


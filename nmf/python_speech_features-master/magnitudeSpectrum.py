import scipy.io.wavfile as wavfile
import numpy as np
import pylab as pl

rate, data = wavfile.read("butterfly.wav")
# print(data)
t = np.arange(len(data[:,0]))*1.0/rate
print(data)
# merge_y = [x*np.log10(x) if x>=1 else 1 for x in n]
print(data.shape)
print(data[100000:1180778,1])
for i in range(0,180778):
  if(data[i,1]>0):
      start = i
      break
print(start)
temp = np.abs(np.fft.rfft(data[start:180778,1]))
# print(data[:2048])
p = [20*np.log10(x) if x>=1 else 1 for x in temp]


f = np.linspace(0, rate/2.0, len(p))
pl.plot(f, p)
pl.xlabel("Frequency(Hz)")
pl.ylabel("Power(dB)")
pl.show()
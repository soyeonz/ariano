#part 1
import scipy.io.wavfile as wavfile
import numpy as np
import pylab as pl
import librosa

from time import time

start = time()

song = "E1_bass.wav"
rate, data = wavfile.read(song)
t = np.arange(len(data[:]))*1.0/rate



#part 2 : Voice activity detector
sample_count = 2048
# y : time series / sr : sampling frequency
y, sr = librosa.load(song)
hop_l = 64
frame_arr = librosa.util.frame(y, frame_length=sample_count, hop_length=hop_l)
# print(frame_arr)
frame_length, frame_column = frame_arr.shape
frame_arr_avg = np.ndarray(shape=(frame_length),dtype=float)
for i in range(0, frame_length):
    frame_arr_avg[i] = np.average(frame_arr[i, :])



#part 3 : stft

stft_arr_abs = np.abs(librosa.stft(frame_arr_avg))
print(stft_arr_abs)
stft_row, stft_column = stft_arr_abs.shape

g3 = fig.add_subplot(223)
g3.set_title("STFT")
g3.plot(stft_arr_abs)

#p = [20*np.log10(x) if x>=1 else 1 for x in stft_arr_abs[i, :] ]
# for i in range(0, stft_row):
#     x = stft_arr_abs[i, :]
#     p = 20*np.log10(np.maximum(x, 1))
    # print(p)
# print(p)

#part 4
# f = np.linspace(0, rate/2.0, len(p))
#
# g3 = fig.add_subplot(223)
# g3.set_title("STFT")
# g3.plot(f, p)
#g3.xlabel("Frequency(Hz)")
#g3.ylabel("Power(dB)")

end = time()
print('Took %.3f seconds' %(end-start))

#Original Signal graph
fig = pl.figure()
g1 = fig.add_subplot(221)
g1.set_title("Original signal")
g1.plot(data)

g2 = fig.add_subplot(222)
g2.set_title("Frame Average")
g2.plot(frame_arr_avg)

g3 = fig.add_subplot(223)
g3.set_title("STFT")
g3.plot(stft_arr_abs)

pl.show()


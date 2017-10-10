#part 1
import scipy.io.wavfile as wavfile
import numpy as np
import pylab as pl
import librosa

rate, data = wavfile.read("E1_bass.wav")
t = np.arange(len(data[:]))*1.0/rate
#Original Signal graph
fig = pl.figure()
g1 = fig.add_subplot(221)
g1.set_title("Original signal")
g1.plot(data)

#part 2 : Voice activity detector
sample_count = 2048
# y : time series / sr : sampling frequency
y, sr = librosa.load("E1_bass.wav")
hop_l = 64
frame_arr = librosa.util.frame(y, frame_length=sample_count, hop_length=hop_l)
print("frame_arr: ")
print(frame_arr)
frame_length, frame_column = frame_arr.shape
# frame_arr_avg = np.ndarray(shape=(frame_length),dtype=float)
frame_arr_avg = np.ndarray.mean(frame_arr, axis=1)

print("frame_arr_avg")
print(frame_arr_avg)
g2 = fig.add_subplot(222)
g2.set_title("Frame Average")
g2.plot(frame_arr_avg)


# print(frame_arr)
#part 3 : stft

temp = librosa.stft(y)
stft_arr_abs = np.abs(temp)
print("stft_arr_abs")
print(stft_arr_abs)
stft_row, stft_column = stft_arr_abs.shape
# p = [20*np.log10(x) if x>=1 else 1 for x in stft_arr_abs[i, :] ]

# print("p")
# for i in range(0, stft_row):
#     x = stft_arr_abs[i, :]
#     p = 20*np.log10(np.maximum(x, 1))
#     print(p)
# print(p)

#part 4
f = np.linspace(0, rate/2.0, len(stft_arr_abs))

g3 = fig.add_subplot(223)
g3.set_title("STFT")
g3.plot(f, stft_arr_abs)
#g3.xlabel("Frequency(Hz)")
#g3.ylabel("Power(dB)")

pl.show()
import matplotlib
import IPython
import seaborn
import numpy, scipy, IPython.display as ipd, matplotlib.pyplot as plt
import librosa, librosa.display
from time import time
# from concurrent.futures import ProcessPoolExecutor
# from jitpy import setup
# setup('<path-to-pypy-home>')
# from jitpy.wrapper import jittify
start = time()
plt.rcParams['figure.figsize'] = (14, 5)

# start_time = time.time()
frequency = [0, 261.6256, 293.6648, 329.6276, 349.2282, 391.9954, 440.0000, 493.8833]

music_map = {
    'samesame': [261, 329, 391, 261, 329, 391, 440, 440, 440, 391, 349, 349, 349, 329, 329, 329, 293, 293, 293, 261, 261, 329, 391, 261, 329, 391, 440, 440, 440, 391, 349, 349, 349, 329, 329, 329, 293, 293, 293, 261],
    'butterfly': [frequency[5], frequency[3], frequency[3], frequency[4], frequency[2], frequency[2],
                 frequency[1], frequency[2], frequency[3], frequency[4], frequency[5], frequency[5],
                 frequency[5], frequency[5], frequency[3], frequency[3], frequency[3], frequency[4],
                 frequency[2], frequency[2], frequency[1], frequency[3], frequency[5], frequency[5],
                 frequency[3], frequency[3], frequency[3], frequency[2], frequency[2], frequency[2],
                 frequency[2], frequency[2], frequency[3], frequency[4], frequency[3], frequency[3],
                 frequency[3], frequency[3], frequency[3], frequency[4], frequency[5], frequency[5],
                 frequency[3], frequency[3], frequency[4], frequency[2], frequency[2], frequency[1],
                 frequency[3], frequency[5], frequency[5], frequency[3], frequency[3], frequency[3]]
}

# pool = ProcessPoolExecutor(max_workers=2)
#Load an audio file.
# filename = '/Users/imsoyeon/ariano/nmf/python_speech_features-master/butterfly2.m4a'
filename = '/Users/bttb66/Documents/ariano/ariano/nmf/python_speech_features-master/butterfly2.m4a'

yt, sr = librosa.load(filename, sr=22050, mono=True)

x, idx = librosa.effects.trim(yt, top_db=10)
print(librosa.get_duration(yt), librosa.get_duration(x))

# filename2 = filename + '_2'
# librosa.output.write_wav(filename2, y=x0, sr=sr0, norm=True)
#
# x, sr = librosa.load(filename2, sr=22050, mono=True)
x = x / numpy.max(numpy.abs(x))

#Display the CQT of the signal.
bins_per_octave = 36
# x = abs(librosa.feature.chroma_cqt(xx, sr=sr, bins_per_octave=bins_per_octave))
cqt = librosa.cqt(x, sr=sr, n_bins=300, bins_per_octave=bins_per_octave)
log_cqt = librosa.logamplitude(cqt)

# print(cqt.shape)

# librosa.display.specshow(log_cqt, sr=sr, x_axis='time', y_axis='cqt_note',%
#                          bins_per_octave=bins_per_octave)

#Step 1: Detect Onsets
hop_length = 100
onset_env = librosa.onset.onset_strength(x, sr=sr, hop_length=hop_length)
# plt.plot(onset_env)
# plt.xlim(0, len(onset_env))

#Next, we try to detect onsets. For more details, see librosa.onset.onset_detect and librosa.util.peak_pick.
onset_samples = librosa.onset.onset_detect(x,
                                           sr=sr, units='samples',
                                           hop_length=hop_length,
                                           backtrack=False,
                                           pre_max=20,
                                           post_max=20,
                                           pre_avg=100,
                                           post_avg=100,
                                           delta=0.2,
                                           wait=0)

#Let's pad the onsets with the beginning and end of the signal.
onset_boundaries = numpy.concatenate([[0], onset_samples, [len(x)]])
# print onset_boundaries

#Convert the onsets to units of seconds:
onset_times = librosa.samples_to_time(onset_boundaries, sr=sr)
# print onset_times

#Display the results of the onset detection:
librosa.display.waveplot(x, sr=sr)
plt.vlines(onset_times, -1, 1, color='r')

#Step 2: Estimate Pitch
#Estimate pitch using the autocorrelation method:
def estimate_pitch(segment, sr, fmin=50.0, fmax=2000.0):
    # Compute autocorrelation of input segment.
    r = librosa.autocorrelate(segment)

    # Define lower and upper limits for the autocorrelation argmax.
    i_min = sr / fmax
    i_max = sr / fmin
    r[:int(i_min)] = 0
    r[int(i_max):] = 0

    # Find the location of the maximum autocorrelation.
    i = r.argmax()
    f0 = float(sr) / i
    return f0

#Step 3: Generate Pure Tone
#Create a function to generate a pure tone at the specified frequency:
# def generate_sine(f0, sr, n_duration):
#     n = numpy.arange(n_duration)
#     return 0.2*numpy.sin(2*numpy.pi*f0*n/float(sr))

#Step 4: Put it together
#Create a helper function for use in a list comprehension:
def estimate_pitch_and_generate_sine(x, onset_samples, i, sr):
    n0 = onset_samples[i]
    n1 = onset_samples[i+1]
    f0 = estimate_pitch(x[n0:n1], sr)
    return f0

#Use a list comprehension to concatenate the synthesized segments:
# y = numpy.concatenate([
#     estimate_pitch_and_generate_sine(x, onset_boundaries, i, sr=sr)



#     for i in range(len(onset_boundaries)-1)
# ])
n = []
for i in range(len(onset_boundaries)-1):
    n.append(estimate_pitch_and_generate_sine(x, onset_boundaries, i, sr=sr))

length = len(music_map['butterfly'])
if len(n) <= len(music_map['butterfly']):
    length = len(n)

print( '-----diff-------')
sum = 0
nidx = 0
for i in range (length - 1):
    if i > 0 and nidx < len(n) - 3:
        diff1 = abs(music_map['butterfly'][i] - music_map['butterfly'][i+1])
        diff2 = abs(n[nidx] - n[nidx+1])
        diff = abs(diff1 - diff2)
        print diff
        if diff > 20:

            tt = abs(n[nidx+1] - n[nidx+2])
            if abs(tt - diff1) < 20:
                nidx += 1
            diff = 0

        sum += diff
    nidx += 1

print('avg of sum=?')
print sum/length


#Play the synthesized transcription.
# ipd.Audio(y, rate=sr, autoplay=True)
# librosa.output.write_wav('/Users/bttb66/Documents/ariano/ariano/nmf/python_speech_features-master/buttertter.wav', y, sr)
#

# # test 2
# hop_length = 512
# chromagram = librosa.feature.chroma_cens(x, sr=sr, hop_length=hop_length)
# # librosa.display.specshow(abs(chromagram), x_axis='time', y_axis='chroma', hop_length=hop_length)
#
# print("start_time", start_time)
# print("--- %s seconds ---" %(time.time() - start_time))

#Plot the CQT of the synthesized transcription.
# detection auto tune
# cqt = librosa.cqt(y, sr=sr)
# librosa.display.specshow(abs(cqt), sr=sr, x_axis='time', y_axis='cqt_note')

#A chroma vector (Wikipedia) (FMP, p. 123) is a typically a 12-element feature vector indicating how much energy of each pitch class, {C, C#, D, D#, E, ..., B}, is present in the signal.
# hop_length = 512
# chromagram = librosa.feature.chroma_stft(x, sr=sr, hop_length=bins_per_octave)
# librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=bins_per_octave)
# chromagram = librosa.feature.chroma_cqt(y, sr=sr)
# print(abs(chromagram))
# print "\n"
# librosa.display.specshow(abs(chromagram), x_axis='time', y_axis='chroma')

# chromagram = librosa.feature.chroma_cens(x, sr=sr, hop_length=hop_length)
# librosa.display.specshow(abs(chromagram), x_axis='time', y_axis='chroma', hop_length=hop_length)

# # test
# data = abs(chromagram)
# print data[numpy.isfinite(data)]
# print "\n"
# min_p, max_p = 2, 98
# max_val = numpy.percentile(data, max_p)
# min_val = numpy.percentile(data, min_p)
#
# print(max_val)
# print(min_val)
#
# if min_val >= 0 or max_val <= 0:
#     # Get the x and y coordinates
#     y_coords = __mesh_coords(y_axis, y_coords, data.shape[0])
#     x_coords = __mesh_coords(x_axis, x_coords, data.shape[1])

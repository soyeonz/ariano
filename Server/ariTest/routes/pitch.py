# %matplotlib osx
import sys
import matplotlib
matplotlib.use('Agg')
import IPython
#import seaborn
import numpy, scipy, IPython.display as ipd, matplotlib.pyplot as plt
import librosa, librosa.display
from pydub import AudioSegment
AudioSegment.ffmpeg = "/usr/local/bin/ffmpeg-normalize"
plt.rcParams['figure.figsize'] = (14, 5)
filename = sys.argv[1]
song = sys.argv[2]

frequency = [0, 261, 293, 329, 349, 391, 440, 493, 523]
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
                 frequency[3], frequency[5], frequency[5], frequency[3], frequency[3], frequency[3]],
    'tutorial': [frequency[1], frequency[2], frequency[3], frequency[4], frequency[5], frequency[6], 
                 frequency[7], frequency[8], frequency[7], frequency[6], frequency[5], frequency[4], 
                 frequency[3], frequency[2], frequency[1], frequency[1], frequency[2], frequency[3], 
                 frequency[4], frequency[5], frequency[6], frequency[7], frequency[8], frequency[7], 
                 frequency[6], frequency[5], frequency[4], frequency[3], frequency[2], frequency[1]],
    'jinglebell': [frequency[3], frequency[3], frequency[3], frequency[3], frequency[3], frequency[3], 
                   frequency[3], frequency[5], frequency[1], frequency[2], frequency[3], frequency[4],
                   frequency[4], frequency[4], frequency[4], frequency[4], frequency[3], frequency[3],
                   frequency[3], frequency[3], frequency[2], frequency[2], frequency[3], frequency[2],
                   frequency[5], frequency[3], frequency[3], frequency[3], frequency[3], frequency[3], 
                   frequency[3],frequency[3], frequency[5], frequency[1], frequency[2], frequency[3], 
                   frequency[4],frequency[4], frequency[4], frequency[4], frequency[4], frequency[3], 
                   frequency[3], frequency[3], frequency[5], frequency[5], frequency[4], frequency[2],
                   frequency[1]]
}

#Load an audio file.


wav_file_pydub = AudioSegment.from_file(filename)

with wav_file_pydub.export('audio.ogg', format='ogg', codec='libvorbis', bitrate='192k') as wav_file:
    wav_file.close()

x, sr = librosa.load('audio.ogg')
x = x / numpy.max(numpy.abs(x))

#
# #Play the audio file.
# ipd.Audio(x, rate = sr, autoplay = True)
# librosa.output.write_wav('/Users/imsoyeon/ariano/nmf/python_speech_features-master/Butterfly2.wav', x, sr)

#Display the CQT of the signal.
bins_per_octave = 36
#cqt = librosa.cqt(x, sr = sr, n_bins = 300, bins_per_octave = bins_per_octave)
#log_cqt = librosa.logamplitude(cqt)

# print(cqt.shape)

# librosa.display.specshow(log_cqt, sr = sr, x_axis = 'time', y_axis = 'cqt_note',%
    #                          bins_per_octave = bins_per_octave)

#Step 1: Detect Onsets
hop_length = 100
#onset_env = librosa.onset.onset_strength(x, sr = sr, hop_length = hop_length)
#plt.plot(onset_env)
#plt.xlim(0, len(onset_env))

#Next, we try to detect onsets.For more details, see librosa.onset.onset_detect and librosa.util.peak_pick.
onset_samples = librosa.onset.onset_detect(x,
    sr = sr, units = 'samples',
    hop_length = hop_length,
    backtrack = False,
    pre_max = 20,
    post_max = 20,
    pre_avg = 100,
    post_avg = 100,
    delta = 0.2,
    wait = 0)

#Let's pad the onsets with the beginning and end of the signal.
onset_boundaries = numpy.concatenate([[0], onset_samples, [len(x)]])
# print onset_boundaries

#Convert the onsets to units of seconds:
onset_times = librosa.samples_to_time(onset_boundaries, sr = sr)
# print onset_times

#Display the results of the onset detection:
# librosa.display.waveplot(x, sr = sr)
# plt.vlines(onset_times, -1, 1, color = 'r')

#Step 2: Estimate Pitch
#Estimate pitch using the autocorrelation method:
def estimate_pitch(segment, sr, fmin = 50.0, fmax = 2000.0):
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


#Step 3: Put it together
#Create a helper function for use in a list comprehension:
def estimate_pitch_and_generate_sine(x, onset_samples, i, sr):
    n0 = onset_samples[i]
    n1 = onset_samples[i + 1]
    f0 = estimate_pitch(x[n0:n1], sr)
    return f0

#Step 4: Get score (Use Longest Common Sequense)
n = []
for i in range(len(onset_boundaries)-1):
    n.append(estimate_pitch_and_generate_sine(x, onset_boundaries, i, sr=sr))


def lcs(a, b):
    prev = [0] * len(a)
    for i, r in enumerate(a):
        current = []
        for j, c in enumerate(b):
            if abs(r - c) <= 10:
                e = prev[j - 1] + 1 if i * j > 0 else 1
            else:
                e = max(prev[j] if i > 0 else 0, current[-1] if j > 0 else 0)
            current.append(e)
        prev = current
    return current[-1]


lcs_ret = lcs(n, music_map[song])

score = lcs_ret * 100 / len(music_map[song])
print score

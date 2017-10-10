%matplotlib inline
import seaborn
import numpy, scipy, matplotlib.pyplot as plt, sklearn, IPython.display as ipd
import librosa, librosa.display
plt.rcParams['figure.figsize'] = (14, 4)

x, sr = librosa.load('audio/conga_groove.wav')
print sr

#Compute stft
S = librosa.stft(x)
print S.shape

#Display spectrogrm
Smag = librosa.amplitude_to_db(S)
librosa.display.specshow(Smag, sr=sr, x_axis='time', y_axis='log')
plt.colorbar()

#Perform factorization
X = numpy.absolute(S)
n_components = 6
W, H = librosa.decompose.decompose(X, n_components=n_components, sort=True)

#Display spectra
plt.figure(figsize=(12, 6))
logW= numpy.log10(W)
for n in range(n_components):
    plt.subplot(numpy.ceil(n_components / 2.0), 2, n + 1)
    plt.plot(logW[:, n])
    plt.ylim(-2, logW.max())
    plt.xlim(0, W.shape[0])
    plt.ylabel('Component %d' % n)

#Display the temporal activations

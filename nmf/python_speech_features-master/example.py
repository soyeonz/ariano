#!/usr/bin/env python
import numpy as np
import scipy.sparse as spr
import nimfa
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import os

(rate,sig) = wav.read("butterfly.wav")
print(sig[1180720:])
mfcc_feat = mfcc(sig,rate,nfft=2048)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat = logfbank(sig,rate,nfft=2048)
V = spr.bsr_matrix(logfbank(sig,rate,nfft=2048))
print(logfbank(sig,rate,nfft=2048))

nmf = nimfa.Nmf(V, max_iter=200, rank=2, update='euclidean', objective='fro')
nmf_fit = nmf()

print(nmf_fit)

W = nmf_fit.basis()
print('Basis matrix:\n%s' % W.todense())

H = nmf_fit.coef()
print('Mixture matrix:\n%s' % H.todense())


#print(fbank_feat)
#print(wav.read("english.wav"))
#print(d_mfcc_feat)

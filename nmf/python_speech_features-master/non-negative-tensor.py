import tensorflow as tf
import numpy as np
import pandas as pd

#example.py
import scipy.sparse as spr
import nimfa
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import os

#np.random.seed(0)
# A_orig = np.array([[3, 4, 5, 2],
#                    [4, 4, 3, 3],
#                    [5, 5, 4, 4]], dtype=np.float32).T

#example.py
(rate,sig) = wav.read("butterfly.wav")
print(sig[1180720:])
mfcc_feat = mfcc(sig,rate,nfft=2048)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat = logfbank(sig,rate,nfft=2048)
#A_orig = spr.bsr_matrix(logfbank(sig,rate,nfft=2048))

A_orig = np.array(logfbank(sig,rate,nfft=2048), dtype=np.float32).T

A_orig = np.fabs(A_orig)

A_orig_df = pd.DataFrame(A_orig)

A_orig_df #(4 users, 3 movies)

print('A_orig_df', A_orig_df)

A_df_masked = A_orig_df.copy()
A_df_masked.iloc[0,0]=np.NAN

np_mask = A_df_masked.notnull()

print(np_mask)

# Boolean mask for computing cost only on valid (not missing) entries
tf_mask = tf.Variable(np_mask.values)

A = tf.constant(A_df_masked.values)
shape = A_df_masked.values.shape

#latent factors
rank = 3

# Initializing random H and W
temp_H = np.random.randn(rank, shape[1]).astype(np.float32)
temp_H = np.divide(temp_H, temp_H.max())

temp_W = np.random.randn(shape[0], rank).astype(np.float32)
temp_W = np.divide(temp_W, temp_W.max())

H =  tf.Variable(temp_H)
W = tf.Variable(temp_W)
WH = tf.matmul(W, H)

#cost of Frobenius norm
cost = tf.reduce_sum(tf.pow(tf.boolean_mask(A, tf_mask) - tf.boolean_mask(WH, tf_mask), 2))

# Learning rate
lr = 0.0001
# Number of steps
steps = 1000
train_step = tf.train.GradientDescentOptimizer(lr).minimize(cost)
init = tf.initialize_all_variables()


# Clipping operation. This ensure that W and H learnt are non-negative
clip_W = W.assign(tf.maximum(tf.zeros_like(W), W))
clip_H = H.assign(tf.maximum(tf.zeros_like(H), H))
clip = tf.group(clip_W, clip_H)
merged = tf.merge_all_summaries()


steps = 1000
with tf.Session() as sess:
    sess.run(init)
    writer = tf.train.SummaryWriter("/Users/imsoyeon/ariano/nmf/python_speech_features-master", sess.graph)
    for i in range(steps):
        sess.run(train_step)
        sess.run(clip)
        if i%100==0:
            print("\nCost: %f" % sess.run(cost))
            print("*"*40)
    learnt_W = sess.run(W)
    learnt_H = sess.run(H)

    print("W -")
    print(learnt_W)
    print("H -")
    print(learnt_H)
    #summary = sess.run(merged, feed_dict=)
    # writer.add_summary(summary, i)
    # summary_writer.flush()

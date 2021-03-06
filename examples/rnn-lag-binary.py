#!/usr/bin/python
# coding: utf-8

import theano
import theano.tensor as T
import numpy
from DL.models.RNN import RNN
from DL.optimizers import optimize
from DL.utils import *
import time
import matplotlib.pyplot as plt

# hide warnings
import warnings
warnings.simplefilter("ignore")

print "Testing an RNN with binary outputs"
print "Generating lag test data..."

n_hidden = 30
n_in = 5
n_out = 2
n_steps = 11
n_seq = 100

# simple lag test
seq = numpy.random.randn(n_seq, n_steps, n_in)
targets = numpy.zeros((n_seq, n_steps, n_out))

# whether lag 1 (dim 3) is greater than lag 2 (dim 0)
targets[:, 2:, 0] = numpy.cast[numpy.int](seq[:, 1:-1, 3] > seq[:, :-2, 0])

# whether product of lag 1 (dim 4) and lag 1 (dim 2)
# is less than lag 2 (dim 0)
targets[:, 2:, 1] = numpy.cast[numpy.int]((seq[:, 1:-1, 4] * seq[:, 1:-1, 2]) > seq[:, :-2, 0])

# split into training, validation, and test
trainIdx = int(numpy.floor(4./6.*n_seq))
validIdx = int(numpy.floor(5./6.*n_seq))

lagData = ((seq[0:trainIdx,:,:], targets[0:trainIdx,:,:]), 
           (seq[trainIdx:validIdx,:,:], targets[trainIdx:validIdx,:,:]),
           (seq[validIdx:,:,:], targets[validIdx:,:,:]))

print "loading data to the GPU"
# if you change this to int32, make you change the target tensor type!
dataset = load_data(lagData)

print "creating the RNN"
x = T.tensor3('x')  # input
t = T.tensor3('t')  # targets
inputs = [x,t]
# cast to an int. needs to be initially a float to load to the GPU
it = t.astype('int64')

rng = numpy.random.RandomState(int(time.time())) # random number generator

rnn = RNN(rng=rng, 
          input=x, 
          n_in=n_in, 
          n_hidden=n_hidden, 
          n_out=n_out, 
          activation='tanh', 
          outputActivation='sigmoid'
)

# regularization
L1_reg=0.00
L2_reg=0.0001

# cost function
cost = (
    nll_binary(rnn.output, it)
    + L1_reg * rnn.L1
    + L2_reg * rnn.L2_sqr
)

pred = pred_binary(rnn.output)

errors = pred_error(pred, it)

params = flatten(rnn.params)

print "training the rnn with rmsprop"

optimize(dataset=dataset,
        inputs=inputs,
        cost=cost,
        params=params,
        errors=errors,
        n_epochs=5000,
        batch_size=20,
        patience=1000,
        patience_increase=1.5,
        improvement_threshold=0.995,
        optimizer="rmsprop")

print "compiling the prediction function"

predict = theano.function(inputs=[x], outputs=rnn.output)

print "predicting the first 10 samples of the training dataset"

seqs = xrange(10)
for seq_num in seqs:
    fig = plt.figure()
    ax1 = plt.subplot(211)
    plt.plot(seq[seq_num])
    ax1.set_title('input')
    ax2 = plt.subplot(212)
    true_targets = plt.step(xrange(n_steps), targets[seq_num], marker='o')

    guess = predict(seq[seq_num:seq_num+1])[0]
    guessed_targets = plt.step(xrange(n_steps), guess)
    plt.setp(guessed_targets, linestyle='--', marker='d')
    for i, x in enumerate(guessed_targets):
        x.set_color(true_targets[i].get_color())
    ax2.set_ylim((-0.1, 1.1))
    ax2.set_title('solid: true output, dashed: model output (prob)')

plt.show()
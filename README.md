# Some Deep Learning models built with Theano


## To Do

- save and reload model.

LSTM
- try on dice model

RNN
- tensor.alloc in RNN instead of repeat
- modify rnn to handle varying length sequences with a mask
- dropout?

MRNN
- character prediction
- hf optimization

MUSE
- USE with multiplicative units

Theano-users
- ask about rnn dropout
- ask about ubuntu install script

CNN
- conv net on images or maybe even imagenet

DA
- denoising autoencoder on mnist

Writing
- write about deep learning, https://imgur.com/a/Hqolp

TSNE
- low dimensional visualization: http://lvdmaaten.github.io/tsne/

## Getting Started

Some examples use `sparkprob` to visualize probablity distributions at the commandline so you may need to install it

    pip install sparkprob

All of the examples use the `DL` package. To use it:
  
    cd DL
    python setup.py develop

To unlink this package when you are done:

    cd DL
    python setup.py develop --uninstall

To load the datasets

    cd datasets
    curl -O http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz
    curl -O http://www.iro.umontreal.ca/~lisa/deep/data/imdb.pkl


<!-- ### Models

The general idea works like this. A "model" take symbolic tensors representing a minibatch. The model constructs the computational graph and produces some class variables to hook into: params, L1, L2_sqr, loss, errors, output, pred. Thus, we can compose models and propagate the L1 and L2_sqr for regularization. We can save the params and pass them as inputs to load a model. We can use the loss and the errors to pass into an optimization function. And we can create a prediction function using output or pred.

Some subtleties here about the naming. Loss is typically something like cross-entropy-error, negative-log-likelihood, or mean-square-error. Errors would be something like, did the model predict the correct MNIST number? Similarly, the output of model could be a distribution of MNIST number likelihoods, but pred, the prediction, is the number with the maximum likelihood.

### Optimizers

An "optimizer" takes in a dataset which is a list of 3 elements: training dataset, validation dataset, test dataset. Each these sub-datasets is an array of data for each of the inputs to the computational graph of the model. Note that the inputs to the "computational graph of the model" includes the "outputs of the model" so-to-speak. The order of the data must correspond to the order of the tensors list passed into inputs. Optimizers are also given param's to update with respect to a cost function. The errors are used for test and validation.
 -->
import keras
from keras.models import load_model
from numpy.random import randn
from matplotlib import pyplot
import os

def load_generator(model_name):
    model = load_model('model/uglf_face.h5')
    return model

def run_generator(generator):
    latent_points = generate_latent_points(100, 25)
    X = generator.predict(latent_points)
    X = (X + 1) / 2.0
    pyplot.imshow(X[0])
    pyplot.show()

def generate_latent_points(latent_dim, n_samples):
    # generate points in the latent space
    x_input = randn(latent_dim * n_samples)
    # reshape into a batch of inputs for the network
    z_input = x_input.reshape(n_samples, latent_dim)
    return z_input


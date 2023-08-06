import math

import numpy as np

from PuzzleLib.Containers import Sequential
from PuzzleLib.Modules import Conv2D, MaxPool2D, Activation, relu, Flatten, Linear

from PuzzleLib.Datasets import Cifar10Loader
from PuzzleLib.Visual import showImageBasedFilters, showFilters
from PuzzleLib.Handlers import Trainer, Validator
from PuzzleLib.Optimizers import MomentumSGD
from PuzzleLib.Cost import CrossEntropy


def buildNet():
	seq = Sequential()

	seq.append(Conv2D(3, 32, 5, pad=2, wscale=0.0001, initscheme="gaussian"))
	seq.append(MaxPool2D(3, 2))
	seq.append(Activation(relu))

	seq.append(Conv2D(32, 32, 5, pad=2, wscale=0.01, initscheme="gaussian"))
	seq.append(MaxPool2D(3, 2))
	seq.append(Activation(relu))

	seq.append(Conv2D(32, 64, 5, pad=2, wscale=0.01, initscheme="gaussian"))
	seq.append(MaxPool2D(3, 2))
	seq.append(Activation(relu))

	seq.append(Flatten())
	seq.append(Linear(seq.dataShapeFrom((1, 3, 32, 32))[1], 64, wscale=0.1, initscheme="gaussian"))
	seq.append(Activation(relu))

	seq.append(Linear(64, 10, wscale=0.1, initscheme="gaussian"))
	return seq


def main():
	cifar10 = Cifar10Loader()
	data, labels = cifar10.load(path="../TestData/")
	data, labels = data[:], labels[:]
	print("Loaded cifar10")

	np.random.seed(1234)
	net = buildNet()

	optimizer = MomentumSGD()
	optimizer.setupOn(net, useGlobalState=True)
	optimizer.learnRate = 0.01
	optimizer.momRate = 0.9

	cost = CrossEntropy(maxlabels=10)
	trainer = Trainer(net, cost, optimizer)

	validator = Validator(net, cost)
	currerror = math.inf

	for i in range(25):
		trainer.trainFromHost(
			data[:50000], labels[:50000], macroBatchSize=50000,
			onMacroBatchFinish=lambda train: print("Train error: %s" % train.cost.getMeanError())
		)
		valerror = validator.validateFromHost(data[50000:], labels[50000:], macroBatchSize=10000)
		print("Accuracy: %s" % (1.0 - valerror))

		if valerror >= currerror:
			optimizer.learnRate *= 0.5
			print("Lowered learn rate: %s" % optimizer.learnRate)

		currerror = valerror

		showImageBasedFilters(net[0].W.get(), "../TestData/conv1.png")
		showFilters(net[3].W.get(), "../TestData/conv2.png")
		showFilters(net[6].W.get(), "../TestData/conv3.png")


if __name__ == "__main__":
	main()

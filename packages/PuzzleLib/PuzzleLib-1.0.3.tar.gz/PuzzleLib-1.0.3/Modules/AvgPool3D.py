import numpy as np

from PuzzleLib.Backend import gpuarray
from PuzzleLib.Backend.Dnn import PoolMode, poolNd, poolNdBackward

from PuzzleLib.Modules.Pool3D import Pool3D


class AvgPool3D(Pool3D):
	def __init__(self, size=2, stride=2, pad=0, includePad=True, name=None):
		super().__init__(size, stride, pad, name)
		self.registerBlueprint(locals())

		self.mode = PoolMode.avgWithPad if includePad else PoolMode.avgNoPad


	def updateData(self, data):
		self.data, self.workspace = poolNd(data, size=self.size, stride=self.stride, pad=self.pad, mode=self.mode,
										   test=not self.train)


	def updateGrad(self, grad):
		self.grad = poolNdBackward(self.inData, self.data, grad, self.workspace, size=self.size, stride=self.stride,
								   pad=self.pad, mode=self.mode)


def unittest():
	batchsize, maps, d, h, w = 2, 6, 5, 7, 5
	data = gpuarray.to_gpu(np.random.randn(batchsize, maps, d, h, w).astype(np.float32))

	size = 3
	stride, pad = 2, 1

	avgpool3d = AvgPool3D(size=size, stride=stride, pad=pad, includePad=True)
	avgpool3d(data)

	hostData = np.zeros(shape=(batchsize, maps, d + 2 * pad, h + 2 * pad, w + 2 * pad), dtype=np.float32)
	hostData[:, :, pad:-pad, pad:-pad, pad:-pad] = data.get()
	hostOutData = np.empty(avgpool3d.data.shape, dtype=np.float32)

	for b in range(batchsize):
		for c in range(maps):
			for z in range(hostOutData.shape[2]):
				for y in range(hostOutData.shape[3]):
					for x in range(hostOutData.shape[4]):
						hostOutData[b, c, z, y, x] = np.mean(hostData[b, c, z * stride:z * stride + size,
															 y * stride:y * stride + size,x * stride:x * stride + size])

	assert np.allclose(hostOutData, avgpool3d.data.get())

	grad = gpuarray.to_gpu(np.random.randn(*avgpool3d.data.shape).astype(np.float32))
	avgpool3d.backward(grad)

	hostGrad = grad.get()
	hostInGrad = np.zeros(hostData.shape, dtype=np.float32)

	for b in range(batchsize):
		for c in range(maps):
			for z in range(hostOutData.shape[2]):
				for y in range(hostOutData.shape[3]):
					for x in range(hostOutData.shape[4]):
						for dz in range(size):
							for dy in range(size):
								for dx in range(size):
									hostInGrad[b,c,z*stride+dz,y*stride+dy,x*stride+dx] += hostGrad[b,c,z,y,x]/size**3

	assert np.allclose(hostInGrad[:, :, pad:-pad, pad:-pad, pad:-pad], avgpool3d.grad.get())


if __name__ == "__main__":
	unittest()

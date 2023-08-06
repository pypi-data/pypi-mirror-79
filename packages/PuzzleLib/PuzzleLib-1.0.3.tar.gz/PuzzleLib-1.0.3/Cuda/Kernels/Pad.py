from string import Template

import numpy as np

from PuzzleLib.Compiler.Codegen.Types import half_t, float_t
from PuzzleLib.Cuda.Utils import roundUpDiv


atomicAddTmpl = """

#include <cuda_fp16.h>


__device__ __forceinline__ void atomicAddFP16(half *address, half val)
{
#if __CUDA_ARCH__ < 700
	const size_t halfbits = 8 * sizeof(half);
	size_t offset = (size_t)address & 2;

	unsigned *addrUI = (unsigned *)((size_t)address - offset);
	unsigned assumed, old = *addrUI;

	do
	{
		assumed = old;

		unsigned short s = offset ? (old >> halfbits) : (old & 0xFFFF);
		s = __half_as_short((float)__short_as_half(s) + (float)val);

		unsigned packed = offset ? ((old & 0xFFFF) | (s << halfbits)) : ((old & 0xFFFF0000) | s);
		old = atomicCAS(addrUI, assumed, packed);
	}
	while (assumed != old);

#else
	atomicAdd(address, val);

#endif
}

"""


mapTmpl = """

__device__ __forceinline__ void map1d(int insize, int outsize, int index, int lpad, int *inindex, int *outindex)
{
	int inoffset = (blockIdx.y + blockIdx.z * gridDim.y) * insize;
	int outoffset = (blockIdx.y + blockIdx.z * gridDim.y) * outsize;

	int instart = max(0, -lpad), outstart = max(0, lpad);

	int x = abs(index - lpad) - abs(index - (insize + lpad - 1)) - index + 2 * lpad + insize - 1 - outstart + instart;
	*inindex = inoffset + x, *outindex = outoffset + index;
}

__device__ __forceinline__ void map2d(int inh, int inw, int outh, int outw, int index, int upad, int lpad,
									  int *inindex, int *outindex)
{
	int inoffset = (blockIdx.y + blockIdx.z * gridDim.y) * inh * inw;
	int outoffset = (blockIdx.y + blockIdx.z * gridDim.y) * outh * outw;

	int outx = index % outw, outy = index / outw;

	int instartx = max(0, -lpad), outstartx = max(0, lpad);
	int instarty = max(0, -upad), outstarty = max(0, upad);

	int inx = abs(outx - lpad) - abs(outx - (inw + lpad - 1)) - outx + 2 * lpad + inw - 1 - outstartx + instartx;
	int iny = abs(outy - upad) - abs(outy - (inh + upad - 1)) - outy + 2 * upad + inh - 1 - outstarty + instarty;

	*inindex = inoffset + iny * inw + inx;
	*outindex = outoffset + outy * outw + outx;
}

"""


padTmpl = Template("""

extern "C"
__global__ void reflectpad1d$ext($T *outdata, const $T *indata, int insize, int lpad, int rpad)
{
	int index = threadIdx.x + blockIdx.x * blockDim.x;
	int outsize = insize + lpad + rpad;

	if (index < outsize)
	{
		int inindex = 0, outindex = 0;
		map1d(insize, outsize, index, lpad, &inindex, &outindex);

		outdata[outindex] = indata[inindex];
	}
}

extern "C"
__global__ void reflectpad1dBackward$ext($T *ingrad, const $T *outgrad, int insize, int lpad, int rpad)
{
	int index = threadIdx.x + blockIdx.x * blockDim.x;
	int outsize = insize + lpad + rpad;

	if (index < outsize)
	{
		int inindex = 0, outindex = 0;
		map1d(insize, outsize, index, lpad, &inindex, &outindex);

		atomicAdd$ext(&ingrad[inindex], outgrad[outindex]);
	}
}

extern "C"
__global__ void reflectpad2d$ext($T *outdata, const $T *indata, int inh, int inw,
								 int upad, int bpad, int lpad, int rpad)
{
	int index = threadIdx.x + blockIdx.x * blockDim.x;
	int outh = inh + upad + bpad, outw = inw + lpad + rpad;

	if (index < outh * outw)
	{
		int inindex = 0, outindex = 0;
		map2d(inh, inw, outh, outw, index, upad, lpad, &inindex, &outindex);

		outdata[outindex] = indata[inindex];
	}
}

extern "C"
__global__ void reflectpad2dBackward$ext($T *ingrad, const $T *outgrad, int inh, int inw,
										 int upad, int bpad, int lpad, int rpad)
{
	int index = threadIdx.x + blockIdx.x * blockDim.x;
	int outh = inh + upad + bpad, outw = inw + lpad + rpad;

	if (index < outh * outw)
	{
		int inindex = 0, outindex = 0;
		map2d(inh, inw, outh, outw, index, upad, lpad, &inindex, &outindex);

		atomicAdd$ext(&ingrad[inindex], outgrad[outindex]);
	}
}

""")


class PadModule:
	def __init__(self, backend):
		self.backend = backend
		self.GPUArray, self.warpSize = backend.GPUArray, backend.warpSize

		self.mod = backend.SourceModule("%s%s%s%s" % (
			atomicAddTmpl, mapTmpl, padTmpl.substitute(T=half_t, ext="FP16"), padTmpl.substitute(T=float_t, ext="")
		))


	def reflectpad(self, data, pad, allocator=None):
		if data.ndim == 3:
			batchsize, maps, insize = data.shape
			lpad, rpad = pad

			assert insize >= max(lpad, rpad) + 1
			outsize = insize + lpad + rpad

			block = (self.warpSize, 1, 1)
			grid = (roundUpDiv(outsize, self.warpSize), maps, batchsize)

			outdata = self.GPUArray.empty((batchsize, maps, outsize), dtype=data.dtype, allocator=allocator)
			fn = self.mod.reflectpad1d if data.dtype == np.float32 else self.mod.reflectpad1dFP16

			fn(outdata, data, np.int32(insize), np.int32(lpad), np.int32(rpad), block=block, grid=grid)

		elif data.ndim == 4:
			batchsize, maps, inh, inw = data.shape
			upad, bpad, lpad, rpad = pad

			assert inh >= max(upad, bpad) + 1 and inw >= max(lpad, rpad) + 1
			outh, outw = inh + upad + bpad, inw + lpad + rpad

			block = (self.warpSize, 1, 1)
			grid = (roundUpDiv(outh * outw, self.warpSize), maps, batchsize)

			outdata = self.GPUArray.empty((batchsize, maps, outh, outw), dtype=data.dtype, allocator=allocator)
			fn = self.mod.reflectpad2d if data.dtype == np.float32 else self.mod.reflectpad2dFP16

			fn(
				outdata, data, np.int32(inh), np.int32(inw),
				np.int32(upad), np.int32(bpad), np.int32(lpad), np.int32(rpad), block=block, grid=grid
			)

		else:
			raise NotImplementedError(data.ndim)

		return outdata


	def reflectpadBackward(self, grad, pad, allocator=None):
		if grad.ndim == 3:
			batchsize, maps, outsize = grad.shape
			lpad, rpad = pad

			block = (self.warpSize, 1, 1)
			grid = (roundUpDiv(outsize, self.warpSize), maps, batchsize)

			insize = outsize - lpad - rpad
			ingrad = self.GPUArray.zeros((batchsize, maps, insize), dtype=grad.dtype, allocator=allocator)
			fn = self.mod.reflectpad1dBackward if grad.dtype == np.float32 else self.mod.reflectpad1dBackwardFP16

			fn(ingrad, grad, np.int32(insize), np.int32(lpad), np.int32(rpad), block=block, grid=grid)

		elif grad.ndim == 4:
			batchsize, maps, outh, outw = grad.shape
			upad, bpad, lpad, rpad = pad

			inh, inw = outh - upad - bpad, outw - lpad - rpad

			block = (self.warpSize, 1, 1)
			grid = (roundUpDiv(outh * outw, self.warpSize), maps, batchsize)

			ingrad = self.GPUArray.zeros((batchsize, maps, inh, inw), dtype=grad.dtype, allocator=allocator)
			fn = self.mod.reflectpad2dBackward if grad.dtype == np.float32 else self.mod.reflectpad2dBackwardFP16

			fn(
				ingrad, grad, np.int32(inh), np.int32(inw),
				np.int32(upad), np.int32(bpad), np.int32(lpad), np.int32(rpad), block=block, grid=grid
			)

		else:
			raise NotImplementedError(grad.ndim)

		return ingrad


def unittest():
	from PuzzleLib.Cuda import Backend
	backendTest(Backend)


def backendTest(Backend):
	for deviceIdx in range(Backend.getDeviceCount()):
		module = PadModule(Backend.getBackend(deviceIdx))

		for dtype, atol in module.backend.dtypesSupported():
			reflectpad1dTest(module, dtype)
			reflectpad2dTest(module, dtype, atol)


def reflectpad1dTest(module, dtype):
	batchsize, maps, insize = 4, 8, 48
	lpad, rpad = 2, 3

	hostData = np.random.randn(batchsize, maps, insize).astype(dtype)

	data = module.GPUArray.toGpu(hostData)
	outdata = module.reflectpad(data, pad=(lpad, rpad))

	hostOutData = outdata.get()
	outsize = hostOutData.shape[2]

	assert np.allclose(hostOutData[:, :, lpad:insize + lpad], hostData)
	assert np.allclose(hostOutData[:, :, :lpad][:, :, ::-1], hostData[:, :, 1:lpad+1])
	assert np.allclose(hostOutData[:, :, insize + lpad:][:, :, ::-1], hostData[:, :, insize - 1 - rpad:insize - 1])

	hostGrad = np.random.randn(batchsize, maps, outsize).astype(np.float32)

	grad = module.GPUArray.toGpu(hostGrad)
	ingrad = module.reflectpadBackward(grad, pad=(lpad, rpad))

	hostInGrad = ingrad.get()

	assert np.allclose(
		hostInGrad[:, :, lpad + 1:insize - rpad - 1], hostGrad[:, :, 2 * lpad + 1:outsize - 2 * rpad - 1]
	)
	assert np.allclose(
		hostInGrad[:, :, 1:lpad + 1], hostGrad[:, :, :lpad][:, :, ::-1] + hostGrad[:, :, lpad + 1:2 * lpad + 1]
	)
	assert np.allclose(
		hostInGrad[:, :, insize - rpad - 1:insize - 1],
		hostGrad[:, :, outsize - rpad:][:, :, ::-1] + hostGrad[:, :, outsize - 2 * rpad - 1:outsize - rpad - 1]
	)


def reflectpad2dTest(module, dtype, atol):
	batchsize, maps, inh, inw = 4, 8, 12, 15
	upad, bpad, lpad, rpad = 2, 3, 2, 3

	hostData = np.random.randn(batchsize, maps, inh, inw).astype(dtype)

	data = module.GPUArray.toGpu(hostData)
	outdata = module.reflectpad(data, pad=(upad, bpad, lpad, rpad))

	hostOutData = outdata.get()
	outh, outw = hostOutData.shape[2:]

	assert np.allclose(hostOutData[:, :, upad:inh + upad, lpad:inw + lpad], hostData)
	assert np.allclose(hostOutData[:, :, :upad, :lpad][:, :, ::-1, ::-1], hostData[:, :, 1:upad + 1, 1:lpad + 1])
	assert np.allclose(
		hostOutData[:, :, inh + upad:, inw + lpad:][:, :, ::-1, ::-1],
		hostData[:, :, inh - 1 - bpad:inh - 1, inw - 1 - rpad:inw - 1]
	)

	hostGrad = np.random.randn(batchsize, maps, outh, outw).astype(dtype)

	grad = module.GPUArray.toGpu(hostGrad)
	ingrad = module.reflectpadBackward(grad, pad=(upad, bpad, lpad, rpad))

	hostInGrad = ingrad.get()

	assert np.allclose(
		hostInGrad[:, :, upad + 1:inh - bpad - 1, lpad + 1:inw - rpad - 1],
		hostGrad[:, :, 2 * upad + 1:outh - 2 * bpad - 1, 2 * lpad + 1:outw - 2 * rpad - 1]
	)
	assert np.allclose(
		hostInGrad[:, :, 1:upad + 1, 1:lpad + 1],
		hostGrad[:, :, :upad, :lpad][:, :, ::-1, ::-1] +
		hostGrad[:, :, upad + 1:2 * upad + 1, lpad + 1:2 * lpad + 1] +
		hostGrad[:, :, :upad, lpad + 1:2 * lpad + 1][:, :, ::-1, :] +
		hostGrad[:, :, upad + 1:2 * upad + 1, :lpad][:, :, :, ::-1], atol=atol
	)
	assert np.allclose(
		hostInGrad[:, :, inh - bpad - 1:inh - 1, inw - rpad - 1:inw - 1],
		hostGrad[:, :, outh - bpad:, outw - rpad:][:, :, ::-1, ::-1] +
		hostGrad[:, :, outh - 2 * bpad - 1:outh - bpad - 1, outw - 2 * rpad - 1:outw - rpad - 1] +
		hostGrad[:, :, outh - bpad:, outw - 2 * rpad - 1:outw - rpad - 1][:, :, ::-1, :] +
		hostGrad[:, :, outh - 2 * bpad - 1:outh - bpad - 1, outw - rpad:][:, :, :, ::-1], atol=atol
	)


if __name__ == "__main__":
	unittest()

__author__ = 'tony'

import numpy
import subprocess
# from numbapro import autojit, jit, int32, vectorize
# from numba import cuda, float32, int32, f8

def calculate_delaunay_using_triangle(node_filepath):

    # build the triangle input file
    # nodata_coords = write_node_input(nparray)

    # execute the triangle code
    proc = subprocess.Popen(['../triangle/triangle', '-en', node_filepath],
                                stdout=subprocess.PIPE,
                            )
    proc.wait()
    output = proc.communicate()[0]
    out_files = []
    for line in output.split('\n'):
        if 'Writing' in line:
            out_files.append(line.split(' ')[-1][:-1])

    return out_files

def read_triangle_outputs(filelist):

    delaunay_triangles = []

    for file in filelist:
        if 'ele' in file:
            # parse delaunay triangles
            with open(file,'r') as f:
                lines = f.readlines()
                for line in lines[1:]:
                    if line[0] != '#': # omit comments
                        idx,a,b,c = line.strip().split()
                        delaunay_triangles.append([a,b,c])

            return delaunay_triangles

def write_node_input(nparray, writepath):
    """
    writes the nparray to triangle input node files
    :param nparray: numpy array [[index, x, y, boundary]].  index is 1 based, boundary is represented as 1 all others 0.
    :return: 1
    """
    '''
        First line: <# of vertices> <dimension (must be 2)> <# of attributes> <# of boundary markers (0 or 1)>
        Remaining lines: <vertex #> <x> <y> [attributes] [boundary marker]
    '''

    # with open('triangle_input.node','w') as f:


        # i = 1
        # rows = nparray.shape[0]
        # cols = nparray.shape[1]

        # coords, nodata_coords, boundary = format_numpy_array(nparray, 0, rows, cols )

    bounds = sum(nparray[:,-1])     # add up the boundary values

    numpy.savetxt(writepath,nparray,fmt='%d %d %d %d', header='%d 2 1 %d'%(nparray.shape[0], bounds),comments='')
        # write triangle input node file
        # f.write("%d 2 1 %d\n" % (len(coords), boundary))
        # for i in xrange(0,len(coords)):
        #     f.write(coords[i])

        # return nodata_coords
    return 1


# todo: THIS IS FASTER WITHOUT CUDA!
# @autojit
def format_numpy_array(nparray):

    # build bounday array
    boundaries = numpy.zeros(nparray.shape)
    boundaries[:,0] = 1
    boundaries[:,-1] = 1
    boundaries[0,:] = 1
    boundaries[-1,:] = 1

    # get all nodata coordinates
    nodata_coords = numpy.where(nparray == 0)

    # format the remainder
    x,y = numpy.nonzero(nparray)            # X,Y coords of non-zero elements
    ids = numpy.arange(1,len(x)+1,1)        # element ids
    bounds = boundaries[x,y]                # boundaries for the non-zero elements

    # stack these data together
    stack = numpy.vstack((ids, x, y, bounds))
    formatted = numpy.vstack(stack)
    formatted = formatted.reshape((-1,4))
    return formatted, nodata_coords


def transpose(a):
    '''
    https://github.com/lebedov/scikit-cuda/issues/33
    pip install --upgrade --no-deps git+https://github.com/lebedov/scikits.cuda.git

    :return:
    '''
    import time
    import numpy as np
    import pycuda.autoinit
    import pycuda.gpuarray as gpuarray
    import scikits.cuda.cublas as cublas

    handle = cublas.cublasCreate()
    # N = 1000
    # a = np.random.rand(N, N)
    R =  a.shape[0]
    C = a.shape[1]
    a_gpu = gpuarray.to_gpu(a)
    a_trans_gpu = gpuarray.zeros((C, R), dtype=np.double)
    alpha = 1.0
    beta = 0.0
    start = time.time()
    cublas.cublasDgeam(handle, 't', 'n', R, R,
                       alpha, a_gpu.gpudata, R,
                       beta, a_gpu.gpudata, R,
                       a_trans_gpu.gpudata, R)
    print time.time()-start
    # assert np.allclose(a_trans_gpu.get(), a.T)
    cublas.cublasDestroy(handle)

    return a_trans_gpu


from osgeo import gdal
from osgeo.gdalconst import *
image = './data/LE70380332014363EDC00_B1.TIF'
ds = gdal.Open(image, GA_ReadOnly)
band = ds.GetRasterBand(1)
data = band.ReadAsArray()
img = data
nparray = img.astype(numpy.float32)

t = transpose(nparray)

print 'here'
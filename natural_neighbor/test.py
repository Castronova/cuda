__author__ = 'tony'

import time
from osgeo import gdal
from gdalconst import GA_ReadOnly
import numpy
import build_delaunay


# read the image into memory
image = '../matlab_landsat_7_interpolation/LE70380332014363EDC00/LE70380332014363EDC00_B1.TIF'
ds = gdal.Open(image, GA_ReadOnly)
band = ds.GetRasterBand(1)
data = band.ReadAsArray()

# grab a subset of the data to work with
# img = data[3000:3250, 3000:3250]
img = data
# img = data[0:5000, 0:5000]
i = 1
rows = img.shape[0]
cols = img.shape[1]
# coords, nodata_coords, boundary =
nparray = img.astype(numpy.float32)



print 'Testing Natural Neighbor on an Array of Shape ' +str(nparray.shape)





st = time.time()
a, a_nodata = build_delaunay.format_numpy_array(img)
print '1. Format_numpy_array: elapsed time %3.5f sec'%(time.time()-st)

print 'Testing Transpose Array ' +str(nparray.shape),
st = time.time()
# from numba import cuda
# blockdim = (32, 8)
# griddim = (32,16)
# a = cuda.to_device(nparray)
# b = numpy.empty(a.shape)
d = build_delaunay.transpose(a)
# b.to_host()

# res = build_delaunay.transpose(a, numpy.empty(a.shape))
print 'elapsed time %3.5f sec'%(time.time()-st)

#
# build_delaunay.write_node_input(a,'triangle_input.node')
# print '2. Write_node_input: elapsed time %3.5f sec'%(time.time()-st)
#
# st = time.time()
# outfiles = build_delaunay.calculate_delaunay_using_triangle('triangle_input.node')
# print '3. Calculate_delaunay_using_triangle: elapsed time %3.5f sec'%(time.time()-st)

# # read triangle.c data into memory
# st = time.time()
# delauney = build_delaunay.read_triangle_outputs(outfiles)
# print 'read_triangle_outputs: elapsed time %3.5f sec'%(time.time()-st)
#

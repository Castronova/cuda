import multiprocessing
import os
import time
import random

import voronoi
import numpy as np
from scipy.spatial import Voronoi
from multiprocessing import Queue



def worker(i):
    """worker function"""

    sleep = random.randint(1,5)
    time.sleep(sleep)

    print 'Worker %d \t\t sleep = %d'%(i,sleep)
    return

def calc_voronoi(i, num_pts, q):

    st = time.time()
    np.random.seed(i)
    pts = np.random.rand(num_pts,2)

    vor = Voronoi(pts)
    regions, vertices = voronoi.voronoi_finite_polygons_2d(vor)

    print ("Job # %d \t\t Elapsed: %3.5f sec \t\t %d points" % (i, time.time()-st, num_pts))

def run_serial_voronoi(count, num_pts):

    for i in range(count):
        st = time.time()
        np.random.seed(i)

        pts = np.random.rand(num_pts, 2)

        vor = Voronoi(pts)
        regions, vertices = voronoi.voronoi_finite_polygons_2d(vor)

        print "Job # %d \t\t Elapsed: %3.5f sec \t\t %d points"  % (i, time.time()-st, num_pts)


if __name__ == '__main__':
    q = multiprocessing.Queue()

    # run the multiprocess version
    jobs = []
    print 'MULTIPROCESS VERSION'
    t1 = time.time()
    count = 10

    for i in range(count):
        # p = multiprocessing.Process(target=worker, args=(i,))
        p = multiprocessing.Process(target=calc_voronoi, args=(i,50000, q))
        jobs.append(p)
        p.start()
    p.join()
    print 'Total Elapsed %3.5f seconds \n\n' %(time.time() - t1)

    # run the serial version
    print 'SERIAL VERSION'
    t2 = time.time()
    run_serial_voronoi(count=10, num_pts=50000)
    print 'Total Elapsed %3.5f seconds ' %(time.time() - t2)

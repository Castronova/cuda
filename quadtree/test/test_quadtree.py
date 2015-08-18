__author__ = 'tonycastronova'

import time
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from quadtree.quadtree import *
import unittest

class test_quadtree(unittest.TestCase):



    def setUp(self):
        pass

    def test_visualizaton(self):

        NUM_TRIANGLES = 200         # number of random triangles to build
        MIN = 10                    # minimum x,y values
        MAX = 1000                  # maximum x,y values
        TRIANGLE_OFFSET = 2         # offset value for generating the triangle coordinates from a random seed point
        MAX_OBJECTS = 4             # max number of object per quadtree node
        MAX_DEPTH = 5               # max depth of quadtree children
        NUM_SEARCH_POINTS = 50      # number of random points to search for triangle intersection

        triangles = np.ones((NUM_TRIANGLES*3,2))

        for i in range(0, len(triangles), 3):
            triangles[i:i+3,0] *= random.uniform(MIN, MAX)
            triangles[i:i+3,1] *= random.uniform(MIN, MAX)
            triangles[i,0] -= TRIANGLE_OFFSET
            triangles[i+1,0] += TRIANGLE_OFFSET
            triangles[i+2,1] += TRIANGLE_OFFSET
        pass


        # generate points that intersect and don't intersect with the triangles
        search_pts =[np.array([triangles[i,0], triangles[i,1] - 1]) for i in range(2,50,3)]
        # my_points.extend([[random.uniform(10,100), random.uniform(10,100)] for i in range(0, 50)])
        # search_pts = [[random.uniform(MIN, MAX), random.uniform(MIN, MAX)] for i in range(0, NUM_SEARCH_POINTS)]



        # build triangle objects
        triobjects =[]
        for i in range(0, len(triangles),3):
            triobjects.append(Triangle(triangles[i,:], triangles[i+1,:], triangles[i+2,:] ))

        # calculate the boundary for the quadtree
        mins = triangles.min(axis=0) - 0.0001
        maxs = triangles.max(axis=0) + 0.0001

        # generate and interactive plot
        fig1 = plt.figure(figsize=(20, 10))
        ax = plt.subplot(1,2,1)
        ax2 = plt.subplot(1,2,2)
        plt.ion()
        plt.show()



        print 'Max Depth = %d' % MAX_DEPTH

        # build quadtree
        print 'Building QuadTree...'
        quadtree = QuadTree(MAX_DEPTH,[ mins[0], maxs[0], mins[1], maxs[1]], MAX_OBJECTS)
        quadtree.clear_gobjects()

        level = quadtree.get_minlevel()
        plt.title('Level '+str(level))
        plotted_bounds = []
        for t in triobjects:
            quadtree.insert_gobject(t)
            bounds = []
            quadtree.getBounds(bounds)
            ax.plot([t.P1[0], t.P2[0], t.P3[0], t.P1[0]],
                    [t.P1[1], t.P2[1], t.P3[1], t.P1[1]])

            plt.draw()
            for b in bounds:
                if b not in plotted_bounds:
                    ax.plot(b[0], b[1], color='k')
                    plotted_bounds.append(b)

        print 'Searching QuadTree...'
        found = 0
        for p in search_pts:
            res = quadtree.find_gobject_that_contains(p)
            if res is not None:
                bounds = []
                res[0].getBounds(bounds)
                for b in bounds:
                    ax2.plot(b[0], b[1], 'k-')

                t = res[1]
                ax2.plot([t.P1[0], t.P2[0], t.P3[0], t.P1[0]],
                    [t.P1[1], t.P2[1], t.P3[1], t.P1[1]])

                ax2.plot(p[0], p[1], 'g+')

                found += 1
                plt.draw()
            else:
                ax2.plot(p[0], p[1], 'rx')

        # update the plot area
        plt.draw()

        print 'Found %d triangles\n\n'%found

    def test_benchmark_sparse(self):

        MIN = 10                    # minimum x,y values
        MAX = 1000                  # maximum x,y values
        TRIANGLE_OFFSET = 2         # offset value for generating the triangle coordinates from a random seed point
        MAX_OBJECTS = 4             # max number of object per quadtree node
        MAX_DEPTH = 5               # max depth of quadtree children
        NUM_SEARCH_POINTS = 5000     # number of random points to search for triangle intersection

        search_pts = [[random.uniform(MIN, MAX), random.uniform(MIN, MAX)] for i in range(0, NUM_SEARCH_POINTS)]

        for nt in range(1000, 51000, 10000):


            NUM_TRIANGLES = nt         # number of random triangles to build

            print '#################################################'
            print 'NUM_TRIANGLES ',NUM_TRIANGLES
            print 'NUM_SEARCH_POINTS', NUM_SEARCH_POINTS
            print '\n'

            for d in range(1,6):
                MAX_DEPTH = d

                total = time.time()

                print 'MAX_DEPTH ', MAX_DEPTH

                triangles = np.ones((NUM_TRIANGLES*3,2))

                for i in range(0, len(triangles), 3):
                    triangles[i:i+3,0] *= random.uniform(MIN, MAX)
                    triangles[i:i+3,1] *= random.uniform(MIN, MAX)
                    triangles[i,0] -= TRIANGLE_OFFSET
                    triangles[i+1,0] += TRIANGLE_OFFSET
                    triangles[i+2,1] += TRIANGLE_OFFSET
                # pass


                # generate points that may intersect the triangles
                search_pts.extend([np.array([triangles[i,0], triangles[i,1] - 1]) for i in range(2,50,3)])


                # build triangle objects
                print 'Building Triangle Objects...',
                st=time.time()
                triobjects =[]
                for i in range(0, len(triangles),3):
                    triobjects.append(Triangle(triangles[i,:], triangles[i+1,:], triangles[i+2,:] ))
                print '%3.5f sec' % (time.time()-st)

                # calculate the boundary for the quadtree
                mins = triangles.min(axis=0) - 0.0001
                maxs = triangles.max(axis=0) + 0.0001

                # build quadtree
                print 'Building QuadTree...',
                st = time.time()
                quadtree = QuadTree(MAX_DEPTH,[ mins[0], maxs[0], mins[1], maxs[1]], MAX_OBJECTS)
                quadtree.clear_gobjects()
                for t in triobjects:
                    quadtree.insert_gobject(t)
                print '%3.5f sec' % (time.time()-st)

                print 'Searching QuadTree...',
                st = time.time()
                found = 0
                for p in search_pts:
                    res = quadtree.find_gobject_that_contains(p)
                    if res is not None:
                        found += 1
                print '%3.5f sec' % (time.time()-st)
                print 'Elapsed Time = %3.5f sec '%(time.time() - total)
                print '---'

            print '#################################################'
'''
MAX_OBJECTS = 10
        for d in range(5,6):

            print 'Depth = %d' % d

            st = time.time()
            # build quadtree
            print 'Building QuadTree...',

            quadtree = QuadTree(d,[ mins[0], maxs[0], mins[1], maxs[1]], MAX_OBJECTS)

            quadtree.clear_gobjects();

            colors = []
            for i in range(d):
                colors.append(cm.Blues(1.*i/d) )

            level = quadtree.get_minlevel()
            plt.title('Level '+str(level))
            plotted_bounds = []
            for t in triobjects:
                quadtree.insert_gobject(t)
                bounds = []
                quadtree.getBounds(bounds)
                ax.plot([t.P1[0], t.P2[0], t.P3[0], t.P1[0]],
                        [t.P1[1], t.P2[1], t.P3[1], t.P1[1]])
                # plt.draw()

                level = quadtree.get_minlevel()

                for b in bounds:
                    if b not in plotted_bounds:
                        ax.plot(b[0], b[1], color='k')#colors[level-1])
                        plotted_bounds.append(b)
                        plt.title('Level '+str(level))
            plt.draw()

            print '%3.5f sec' % (time.time() - st)

            st = time.time()
            print 'Searching QuadTree...',
            found = 0
            for p in my_points:
                res = quadtree.find_gobject_that_contains(p)
                if res is not None:
                    bounds = []
                    res[0].getBounds(bounds)
                    for b in bounds:
                        ax2.plot(b[0], b[1], 'k-')

                    t = res[1]
                    ax2.plot([t.P1[0], t.P2[0], t.P3[0], t.P1[0]],
                        [t.P1[1], t.P2[1], t.P3[1], t.P1[1]])

                    ax2.plot(p[0], p[1], 'g+')

                    # plt.draw()
                    found += 1
                else:
                    ax2.plot(p[0], p[1], 'rx')
            plt.draw()

            print '%3.5f sec' % (time.time() - st)
            print 'Found %d triangles\n\n'%found

'''

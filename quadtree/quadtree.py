__author__ = 'tonycastronova', 'caleb buahin'

import random
import numpy as np
import matplotlib.pyplot as plt
import time

class GObject:
    def __init__(self):
        pass

    def get_bounds(self):
        pass

    def contains(self, point):
        return False


class Triangle(GObject):
    def __init__(self, p1, p2, p3):
        GObject.__init__(self)

        self.P1 = p1
        self.P2 = p2
        self.P3 = p3
        self.Bounds = [min(p1[0], p2[0], p3[0]), max(p1[0], p2[0], p3[0]), min(p1[1], p2[1], p3[1]),
                       max(p1[1], p2[1], p3[1])]

    def get_bounds(self):
        return self.Bounds

    def contains(self, point):
        if (point[0] >= self.Bounds[0] and
                    point[0] <= self.Bounds[1] and
                    point[1] >= self.Bounds[2] and
                    point[1] <= self.Bounds[3]):
            b1 = self.sign(point, self.P1, self.P2) < 0.0
            b2 = self.sign(point, self.P2, self.P3) < 0.0
            b3 = self.sign(point, self.P3, self.P1) < 0.0

            return ((b1 == b2) and (b2 == b3))

        return False

    def sign(self, p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


class QuadTree:

    def __init__(self, level, bounds, max_objects=5):

        self.Level = level
        self.max_objects = max_objects

        self.Xmin = bounds[0]
        self.Xmax = bounds[1]
        self.Ymin = bounds[2]
        self.Ymax = bounds[3]
        self.GObjects = []
        self.Nodes = [None, None, None, None]


    def split(self):

        if self.Level - 1 >= 0:
            midX = (self.Xmax + self.Xmin) / 2.0
            midY = (self.Ymax + self.Ymin) / 2.0

            topLeft = [self.Xmin, midX, midY, self.Ymax]
            self.Nodes[0] = QuadTree(self.Level - 1, topLeft, self.max_objects)

            topRight = [midX, self.Xmax, midY, self.Ymax]
            self.Nodes[1] = QuadTree(self.Level - 1, topRight, self.max_objects)

            bottomLeft = [self.Xmin, midX, self.Ymin, midY]
            self.Nodes[2] = QuadTree(self.Level - 1, bottomLeft, self.max_objects)

            bottomRight = [midX, self.Xmax, self.Ymin, midY]
            self.Nodes[3] = QuadTree(self.Level - 1, bottomRight, self.max_objects)

    def completely_contains(self, gobject):

        bounds = gobject.get_bounds()

        if (bounds[0] >= self.Xmin and bounds[1] <= self.Xmax and
                    bounds[2] >= self.Ymin and bounds[3] <= self.Ymax):
            return True

        return False

    def contains(self, point):

        if (point[0] >= self.Xmin and point[0] <= self.Xmax and
                    point[1] >= self.Ymin and point[1] <= self.Ymax):
            return True

        return False

    def get_quadindex_for_gobject(self, gobject):

        if self.Nodes[0] is not None:
            if (self.Nodes[0].completely_contains(gobject)):
                return 0
            elif (self.Nodes[1].completely_contains(gobject)):
                return 1
            elif (self.Nodes[2].completely_contains(gobject)):
                return 2
            elif (self.Nodes[3].completely_contains(gobject)):
                return 3

        return -1

    def get_quadindex_for_point(self, point):

        if self.Nodes[0] is not None:
            if (self.Nodes[0].contains(point)):
                return 0
            elif (self.Nodes[1].contains(point)):
                return 1
            elif (self.Nodes[2].contains(point)):
                return 2
            elif (self.Nodes[3].contains(point)):
                return 3

        return -1

    def insert_gobject(self, gobject):

        if (self.Nodes[0] is not None):
            index = self.get_quadindex_for_gobject(gobject)
            if index != -1:
                self.Nodes[index].insert_gobject(gobject)
                return

        if (self.completely_contains(gobject)):

            self.GObjects.append(gobject)

            if len(self.GObjects) > self.max_objects and self.Level - 1 >= 0:

                if (self.Nodes[0] is None):
                    self.split()

                i = 0;

                while (i < len(self.GObjects)):
                    index = self.get_quadindex_for_gobject(self.GObjects[i])
                    if (index != -1):
                        self.Nodes[index].insert_gobject(self.GObjects.pop(i))
                    else:
                        i += 1

    def clear_gobjects(self):

        self.GObjects = []

        for i in range(0, len(self.Nodes)):
            node = self.Nodes[0];
            if node is not None:
                node.clear_objects()


    def find_gobject_that_contains(self, point):

        if (self.contains(point)):

            if len(self.GObjects) > 0:
                for i in range(0 , len (self.GObjects)):

                    gobject = self.GObjects[i]

                    if gobject.contains(point):
                        return self , gobject


            index = self.get_quadindex_for_point(point)

            if index != -1 and self.Nodes[0] is not None:

                node = self.Nodes[index]

                if len(node.GObjects) > 0:

                    for i in range(0 , len (node.GObjects)):
                        gobject = node.GObjects[i]

                        if gobject.contains(point):
                            return node , gobject

                return   node.find_gobject_that_contains(point)

        return None

    def getBounds(self, list):

        list.append( [[self.Xmin , self.Xmax , self.Xmax , self.Xmin , self.Xmin] ,
                      [self.Ymin , self.Ymin , self.Ymax , self.Ymax , self.Ymin]] )

        if(self.Nodes[0] is not None):

            for i in range(0,4):
                self.Nodes[i].getBounds(list)

    def get_minlevel(self):

        level  = self.Level

        if self.Nodes[0] is not None:

            for i in range(0,4):

                currentL = self.Nodes[i].get_minlevel()

                if currentL < level:
                    level = currentL

        return  level

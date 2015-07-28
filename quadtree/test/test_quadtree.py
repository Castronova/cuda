__author__ = 'tonycastronova'

from matplotlib import cm

from quadtree.quadtree import *

np.random.seed(0)
triangles = np.ones((200*3,2))

for i in range(0, len(triangles), 3):
    triangles[i:i+3,0] *= random.uniform(10, 1000)
    triangles[i:i+3,1] *= random.uniform(10, 1000)
    triangles[i,0] -= 2
    triangles[i+1,0] += 2
    triangles[i+2,1] += 2


# generate points that intersect and don't intersect with the triangles
my_points =[np.array([triangles[i,0], triangles[i,1] - 1]) for i in range(2,50,3)]
my_points.extend([[random.uniform(10,100), random.uniform(10,100)] for i in range(0, 50)])
# my_points = [np.array([0,0]), np.array([20,20])]
# build triangle objects
triobjects =[]
for i in range(0, len(triangles),3):
    triobjects.append(Triangle(triangles[i,:], triangles[i+1,:], triangles[i+2,:] ))
mins = triangles.min(axis=0) - 0.0001
maxs = triangles.max(axis=0) + 0.0001

# generate and interactive plot
fig1 = plt.figure(figsize=(20, 10))
ax = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
plt.ion()
plt.show()

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

x = raw_input('wait')
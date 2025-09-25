### This file contains some helper functions and classes for generating better plots

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp


### to format ticks as multiples of whole-numbered fractions of pi
def multiple_formatter(denominator=2, number=np.pi, latex="\pi"):
    def gcd(a,b):
        while b:
            a, b = b, a%b
        return a
    
    def _multiple_formatter(x, pos):
        den = denominator
        num = int(np.rint(den*x/number))
        com = gcd(num,den)
        num,den = int(num/com), int(den/com)
        if den == 1:
            return {
                0 : r'$0$' ,
                1 : r'$%s$'%latex ,
                -1: r'$-%s$'%latex
            }.get(num, r'$%s%s$'%(num,latex))
        else:
            return {
                1 : r'$\frac{%s}{%s}$'%(latex,den) ,
                -1: r'$\frac{-%s}{%s}$'%(latex,den)
            }.get(num, r'$\frac{%s}{%s}%s$'%(num,den,latex) )
        
    return _multiple_formatter

class Multiple:
    def __init__(self, denominator=2, number=np.pi, latex='\pi'):
        self.denominator = denominator
        self.number = number
        self.latex = latex
    
    def locator(self):
        return plt.MultipleLocator(self.number / self.denominator)
    
    def formatter(self):
        return plt.FuncFormatter(multiple_formatter(self.denominator, self.number, self.latex))

MULTIPLE_PI_2 = Multiple(denominator=2, number=np.pi, latex='\pi')
MULTIPLE_PI_3 = Multiple(denominator=3, number=np.pi, latex='\pi')
MULTIPLE_PI_4 = Multiple(denominator=4, number=np.pi, latex='\pi')
MULTIPLE_PI_6 = Multiple(denominator=6, number=np.pi, latex='\pi')
MULTIPLE_PI_12 = Multiple(denominator=12, number=np.pi, latex='\pi')


### plot scalar data defined on an irregular point cloud to a voronoi tesselation heatmap
def voronoi_heatmap(ax, positions, labels, abstract_cmap:callable, alpha:float=1.0):
    xmin,ymin = np.min(positions,axis=1)
    xmax,ymax = np.max(positions,axis=1)

    xspan = xmax-xmin
    yspan = ymax-ymin

    #points = positions.T
    dummy_points = np.array([
        [xmin - 10 * xspan, ymin - 10 * yspan],
        [0.5*(xmax+xmin), ymin - 10 * yspan],
        [xmax + 10 * xspan, ymin - 10 * yspan],
        [xmin - 10 * xspan, ymax + 10 * yspan],
        [0.5*(xmax+xmin), ymax + 10 * yspan],
        [xmax + 10 * xspan, ymax + 10 * yspan],
    ])
    tess = sp.spatial.Voronoi( np.concatenate( [positions.T, dummy_points], axis=0 ) )

    for j in range(len(tess.points)):
        point_region = tess.point_region[j]
        if point_region != -1:
            region = tess.regions[point_region]
            if not -1 in region:
                polygon = [tess.vertices[i] for i in region]
                #plt.fill(
                #    *zip(*polygon), 
                #    ring_access(SEGMENT_COLORS, labels[j]),
                #    alpha=alpha
                #)
                ax.add_patch(
                    mpl.patches.Polygon(
                        polygon, 
                        facecolor=abstract_cmap(labels[j]),
                        alpha=alpha,
                        linewidth=0,
                        #hatch='/'
                    )
                )
        #    else:
        #        print(f"-1 in point_region {point_region} <- point {j}")
        #else:
        #    print(f"point_region of point {j} is -1")
    
    #sp.spatial.voronoi_plot_2d(tess,ax,show_vertices=False,show_points=False)

    ax.set_xlim(xmin - 0.1 * xspan, xmax + 0.1 * xspan)
    ax.set_ylim(ymin - 0.1 * yspan, ymax + 0.1 * yspan)



if __name__=="__main__":
    ### tests
    pass

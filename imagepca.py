#!/usr/bin/env python
from PIL import Image
import sys
import os.path

from matplotlib.mlab import PCA
import numpy
import math

f = open( sys.argv[1], 'rb' )
root, ext = os.path.splitext( sys.argv[1] )
fout = open( root + '-pca-delta.png', 'wb' )
fout2 = open( root + '-pca-cross.png', 'wb' )
im  = Image.open( f )
im2 = Image.new( "L", im.size )
data = numpy.array(im.getdata())

pca = PCA( data )
mu = pca.mu
newdata = pca.Y #pca.project( data )
newdata = [ math.sqrt( y**2 + z**2 ) for (x,y,z) in newdata ]
mx = max( newdata )
mn = min( newdata )
delta = mx - mn
newdata = [ 255 * (x - mn) / delta for x in newdata ]
im2.putdata( newdata )

centered = data - pca.mu


wt = numpy.linalg.inv( pca.Wt )[0]
wt = pca.Wt[0]
row = centered[2300]


crossed = [ (wt[2] * row[1] - row[2] * wt[1], wt[0] * row[2] - row[0] * wt[2], wt[1] * row[0] - row[1] * wt[0]) for row in centered ]
newcrossed = []
for row in crossed:
	norm = math.sqrt( row[0]**2 + row[1]**2 + row[2]**2 )
	newvec = (int(128 + 128 * row[0] / norm), int(128 + 128* row[1]/norm), int(128 + 128*row[2] / norm))
	newcrossed.append( newvec )

im2.save( fout, "PNG" )
im.putdata( newcrossed )
im.save( fout2 )

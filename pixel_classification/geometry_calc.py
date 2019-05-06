
import numpy as np
from mpl_toolkits.basemap import Basemap
from shapely.geometry import LineString
from shapely.geometry import Point

# set up map
def set_m(lons_t,lats_t):
  x1 = np.min(lons_t) - 0.5
  x2 = np.max(lons_t) + 0.5
  y1 = np.min(lats_t) - 0.2
  y2 = np.max(lats_t) + 0.2
  m = Basemap(llcrnrlat=y1,urcrnrlat=y2,llcrnrlon=x1,urcrnrlon=x2,
            projection='lcc',lat_1=(y1+y2)/2,lat_2=(y1+y2)/2,lon_0=(x1+x2)/2,
            resolution ='f')
  return m

# get number of segments, segment centre line list and list of lines parallel to segment centre lines
def sgm(x_t,y_t):
  sgm_length=20000.0
  sgm_width=30000.0
  zipxy=zip(x_t,y_t)
  line_t = LineString(zipxy)
  line_t_length=line_t.length
  sgm_nr=int(line_t_length/sgm_length)
  sgm_l=[]
  sgm_l_left=[]
  for sgm_i in range(0,sgm_nr, 1):
    t_startp=sgm_i*sgm_length
    t_endp=(sgm_i+1)*sgm_length
    sgm_l_i_start=line_t.interpolate(t_startp)
    sgm_l_i_end=line_t.interpolate(t_endp)
    sgm_l_i= LineString([sgm_l_i_start,sgm_l_i_end])
    sgm_l_left_i=sgm_l_i.parallel_offset(sgm_width+1000.0,'left',join_style=1)
    sgm_l.append(sgm_l_i)
    sgm_l_left.append(sgm_l_left_i)
  return sgm_nr,sgm_l,sgm_l_left

# polygon around centre line
def get_buf(sgm_l_i):
  sgm_width=30000.0
  t_buf = sgm_l_i.buffer(sgm_width, cap_style=2)
  return t_buf

# points inside polygon
def inpoly(polygon, xp, yp):
  return np.array([Point(x, y).intersects(polygon) for x, y in zip(xp, yp)],dtype=np.bool)

# calculate distance
def dist(object, xp, yp):
  return np.array([object.distance(Point(x, y)) for x, y in zip(xp, yp)],dtype=np.float)
  
# count neighbours  
def count_neighbours(x_index,y_index):
  nr=np.zeros(x_index.shape[0])
  for i in xrange(x_index.shape[0]):
    x=x_index[i]
    y=y_index[i]
    for ii in xrange(x_index.shape[0]):
      if x_index[ii]==x+1 and y_index[ii]==y+1:
        nr[i]=nr[i]+1   
      if x_index[ii]==x+1 and y_index[ii]==y:
        nr[i]=nr[i]+1   
      if x_index[ii]==x+1 and y_index[ii]==y-1:
        nr[i]=nr[i]+1 
      if x_index[ii]==x and y_index[ii]==y-1:
        nr[i]=nr[i]+1 
      if x_index[ii]==x-1 and y_index[ii]==y-1:
        nr[i]=nr[i]+1
      if x_index[ii]==x-1 and y_index[ii]==y:
        nr[i]=nr[i]+1
      if x_index[ii]==x-1 and y_index[ii]==y+1:
        nr[i]=nr[i]+1
      if x_index[ii]==x and y_index[ii]==y+1:
        nr[i]=nr[i]+1
  return nr  
  
  
  
  


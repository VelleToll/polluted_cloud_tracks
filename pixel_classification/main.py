

import numpy as np
import geometry_calc as gm
import classification as cl

# track centre line points (lons and lats)
t_file='track.txt'
lons_t,lats_t=np.loadtxt(t_file, skiprows=0, unpack=True)

# lons, lats and near-infrared NIRlectance of (MODIS) INPUT data to be anlyzed
lons=np.load('./lons.npy')
lats=np.load('./lats.npy')
NIR=np.load('./NIR.npy')

# create index arrays
index=np.nonzero(np.ones((NIR.shape[0],NIR.shape[1])))
x_in=index[0].reshape(NIR.shape[0],NIR.shape[1])
y_in=index[1].reshape(NIR.shape[0],NIR.shape[1])


#set up map
m=gm.set_m(lons_t,lats_t)

# track (t) centre lines (l) and segments (sgm)
x_t, y_t = m(lons_t,lats_t)
sgm_nr,sgm_l,sgm_l_left=gm.sgm(x_t,y_t)
x, y = m(lons,lats)

#cycle over segments
for sgm_i in range(0,sgm_nr, 1):
  print 'working on segment nr:',sgm_i 
  sgm_l_i=sgm_l[sgm_i]
  t_buf_i = gm.get_buf(sgm_l_i)
  sgm_l_left_i=sgm_l_left[sgm_i]
  # plot polluted pixels and unpolluted control pixels on the same image
  cl.plot_polluted_control(sgm_i,sgm_l_i,t_buf_i,sgm_l_left_i,x,y,NIR,x_in,y_in)  












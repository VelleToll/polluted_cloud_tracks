

import numpy as np
import geometry_calc as gm
import matplotlib.pyplot as plt
import matplotlib as mpl


def plot_polluted_control(sgm_i,sgm_l_i,t_buf_i,sgm_l_left_i,x,y,NIR,x_in,y_in):
  
  mask_sgm = gm.inpoly(t_buf_i, x.ravel(), y.ravel())
  mask_sgm = mask_sgm.reshape(x.shape)

  # mask segment
  NIR_sgm = np.ma.masked_array(NIR,~mask_sgm)
  NIR_sgm = np.ma.compressed(NIR_sgm)
  x_sgm = np.ma.masked_array(x,mask=~mask_sgm)
  x_sgm = np.ma.compressed(x_sgm)
  y_sgm = np.ma.masked_array(y,mask=~mask_sgm)
  y_sgm = np.ma.compressed(y_sgm)

  # define threshold line  
  dist_left = gm.dist(sgm_l_left_i,x_sgm,y_sgm)
  e1 = dist_left < 21000.0 
  e2 = dist_left > 40000.0
  mask_e = e1+e2
  dist_left_e=np.ma.masked_array(dist_left,mask=~mask_e)
  dist_left_e=np.ma.compressed(dist_left_e)
  NIR_sgm_e=np.ma.masked_array(NIR_sgm,mask=~mask_e)
  NIR_sgm_e=np.ma.compressed(NIR_sgm_e)
  k, b = np.polyfit(dist_left_e/1000.0,NIR_sgm_e, 1)
  stdedges=np.std(NIR_sgm_e)
  mask_bl = NIR_sgm > dist_left/1000.0*k + b + 2*stdedges
  
  # get pixels with NIR reflectance below thresholdline
  bl_NIR=np.ma.masked_array(NIR_sgm,mask=mask_bl)
  bl_NIR=np.ma.compressed(bl_NIR)
  bl_dist=np.ma.masked_array(dist_left,mask=mask_bl)
  bl_dist=np.ma.compressed(bl_dist)
  
  # get pixels with NIR reflectance above thresholdline
  NIR_polluted=np.ma.masked_array(NIR_sgm,mask=~mask_bl)
  NIR_polluted=np.ma.compressed(NIR_polluted)
  dist_polluted=np.ma.masked_array(dist_left,mask=~mask_bl)
  dist_polluted=np.ma.compressed(dist_polluted)

  # get x and y index arrays of polluted pixels
  x_index=np.ma.masked_array(x_in,mask=~mask_sgm)
  x_index=np.ma.compressed(x_index)
  x_index=np.ma.masked_array(x_index,mask=~mask_bl)
  x_index=np.ma.compressed(x_index)
  y_index=np.ma.masked_array(y_in,mask=~mask_sgm)
  y_index=np.ma.compressed(y_index)
  y_index=np.ma.masked_array(y_index,mask=~mask_bl)
  y_index=np.ma.compressed(y_index)  
  # mask isolated polluted pixels
  neighbours=gm.count_neighbours(x_index,y_index)
  m_neighbours = neighbours < 3
  NIR_polluted=np.ma.masked_array(NIR_polluted,mask=m_neighbours)
  NIR_polluted=np.ma.compressed(NIR_polluted)
  dist_polluted=np.ma.masked_array(dist_polluted,mask=m_neighbours)
  dist_polluted=np.ma.compressed(dist_polluted)

  # atleast 20 polluted pixels are required
  if NIR_polluted.shape[0] <= 19:
    return None  

  centre=np.median(dist_polluted)
  stddist=np.std(dist_polluted)

  # get mask for unpolluted control pixels mask_c 
  mask_c1 = bl_dist/1000.0 > centre/1000.0+2*stddist/1000.0+5.0+4*stddist/1000.0
  mask_c2 = bl_dist/1000.0 < centre/1000.0-2*stddist/1000.0-5.0-4*stddist/1000.0
  mask_c3 = np.absolute(bl_dist-centre)/1000.0 < 2*stddist/1000.0+5.0    
  mask_c3_r = (bl_dist-centre)/1000.0 < 2*stddist/1000.0+5.0  
  mask_c3_l = (bl_dist-centre)/1000.0 > -2*stddist/1000.0-5.0   
  mask_c=mask_c1+mask_c2+mask_c3
  
  # atleast 20 control pixels are required on both sides of the track
  mask_c_l=mask_c2+mask_c3_l
  mask_c_r=mask_c1+mask_c3_r
  if (np.ma.compressed(np.ma.masked_array(bl_NIR,mask=mask_c_l))).shape[0] <= 19:
    return None    
  if (np.ma.compressed(np.ma.masked_array(bl_NIR,mask=mask_c_r))).shape[0] <= 19:
    return None    
  
  # get NIR reflectance of control pixels
  dist_control=np.ma.masked_array(bl_dist,mask=mask_c)
  dist_control=np.ma.compressed(dist_control)
  NIR_control=np.ma.masked_array(bl_NIR,mask=mask_c)
  NIR_control=np.ma.compressed(NIR_control)

  # plt segment NIR
  mpl.rcParams['font.size']=14
  plt.clf()
  x2=np.arange(0.5,61.5,0.5)
  plt.plot(x2, k*x2 + b, '-',color='#000080',label='Linear fit to edges', linewidth=2.0)
  plt.plot(x2, k*x2 + b + 2*stdedges, '--',color='#dede00', linewidth=2.0)
  plt.plot(bl_dist/1000.0,bl_NIR,'x',color='#808080',markersize=2,alpha=1.0)
  plt.plot(dist_polluted/1000.0,NIR_polluted, '^',color='#dede00',markersize=5,alpha=0.9)
  plt.plot(dist_control/1000.0,NIR_control,  'v',color='#000080',markersize=5,alpha=0.9)
  plt.axvline(centre/1000.0+2*stddist/1000.0+5.0,color='k', linewidth=2.0)
  plt.axvline(centre/1000.0+2*stddist/1000.0+5.0+4*stddist/1000.0,color='k', linewidth=2.0)
  plt.axvline(centre/1000.0-2*stddist/1000.0-5.0,color='k', linewidth=2.0)
  plt.axvline(centre/1000.0-2*stddist/1000.0-5.0-4*stddist/1000.0,color='k', linewidth=2.0)
  plt.xlabel('Distance across track [km]')
  plt.ylabel(r'2.1 $\mu m$ reflectance')
  plt.xlim((0.0,60.0))
  plt.savefig('NIR_sgm_'+str(sgm_i)+'.png')











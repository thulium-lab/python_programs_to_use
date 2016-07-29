
# coding: utf-8

# In[1]:

'''Last modified 11.02.2016
    Added mongoDB functionality - one can query any data he wants DESCRIBE HOW TO DO THIS
    Pandas table can be used
09.02.2016
Nothing changed, database and pandas functionality should be added!!!
''';


# In[2]:

get_ipython().magic('pylab inline')


# In[3]:

# imports

import sys
import os
par_dir = os.path.split(os.getcwd())[0]
if par_dir not in sys.path:
    sys.path.append(par_dir)
# sys.path.append(r'/Users/artemgolovizin/GitHub')
from scipy.optimize import curve_fit
import inspect
import pickle
import imp
import re
import json
import pandas as pd

from IPython.html import widgets
from IPython.display import display
from IPython.html.widgets import interact, interactive, fixed

import thulium_python_lib.usefull_functions as usfuncs
import thulium_python_lib.image_processing_new as impr

import ipyparallel as ipp
ipp.CompositeError.tb_limit = 1

rc1 = ipp.Client()
lview = rc1.load_balanced_view()
dview = rc1.direct_view()
dview['par_dir'] = par_dir
# with dview.sync_imports():
#     import sys, os    
get_ipython().magic('px import sys, os')
get_ipython().magic('px if par_dir not in sys.path: sys.path.append(par_dir)')
get_ipython().magic('px import thulium_python_lib.image_processing_new as impr')
get_ipython().magic('px import imp')
get_ipython().magic('px from ipyparallel import bind_kernel; bind_kernel()')

import datetime
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# start mongoDB client (mongod server should be launched)
client = MongoClient('mongodb://192.168.1.15:27017/')
meas_database = client.measData.meas_data


# In[4]:

# to reload library on remote and local engine
# %px imp.reload(impr)
# imp.reload(impr)
# imp.reload(usfuncs)


# In[5]:

# OLD part for getting data from mongoDB
coursor = meas_database.find({'conf_params.SHUTTER':'on','meas_type':'T'})
tables = []
for item in coursor:
    for key in item:
        if(key == 'avr_table_pickle'):
            tables.append(pickle.loads(item[key]))
            print(key,item[key][-20:])
        else:
            print(key,item[key])
    print('\n')


# In[6]:

mmm = meas_database.find_one()
print(mmm.keys())


# In[7]:

datetime.datetime(2016, 2, 4, 0, 0) < datetime.datetime(2017, 2, 4, 0, 0)


# In[8]:

mmm['date_meas']


# In[9]:

x = copy(data)


# In[10]:

#meas_database.delete_one({'_id': ObjectId('57054a950aad402528297512')})


# In[11]:

# get data from mongo db and print folders names and dates
coursor = meas_database.find()
coursor = meas_database.find({'date_meas':datetime.datetime(2015, 7, 1, 0, 0), 'meas_type':'T', 'conf_params.A': { '$in': ['0dBm','0dBm/'] } }) #
data = []
for item in coursor:
    data.append(item.copy())
    data[-1]['avr_table']=pickle.loads(item['avr_table_pickle'])
    del data[-1]['avr_table_pickle']
    print(len(data)-1, 'date=',data[-1]['date_meas'].date(), 'folder=',data[-1]['folder'])
#     print(data[-1]['conf_params'])
#     print(data[-1]['_id'])
#     for key in item:
#         if(key == 'avr_table_pickle'):
#             tables.append(pickle.loads(item[key]))
#             print(key,item[key][-20:])
#         else:
#             print(key,item[key])
    print('\n')


# In[12]:

#data[12]


# In[13]:

xx46 = []
Ty46 = []
Tx46 = []
Na46 = []
for d in data:
    xx46.append(float(re.findall(r"[-+]?\d*\.?\d+",d['conf_params']['F'])[-1]))
    Tx46.append(d['fits'][0][1][0])
    Ty46.append(d['fits'][1][1][0])
    Na46.append(d['avr_table']['fit1D_x']['N'][0])

xx46 =  array(xx46)
xx46 = 2*(364.7 - xx46)
figsize(10,5)
plot(xx46,Na46,'o')


# In[245]:

figsize(10,50)
subplot(10,1,1)
plot(xx110,Na110,'o')
plot(xx75,Na75,'o')
#plot(xx46,Na46,'o')
plot(xx30,Na30,'o')
plot(xx20,Na20,'o')
ylim(bottom=0)
xlabel('δ, МГц', fontsize=14, family="verdana")
ylabel('Число атомов', fontsize=14, family="verdana")
title('Число атомов от отстройки',fontsize=14,family='verdana')
legend(['s=0,5','s=0,3','s=0,13','s=0,09'])

subplot(10,1,2)
plot(xx110,Tx110,'bo')
plot(xx110,Ty110,'ro')
title('Температуры от отстройки, 110',fontsize=14,family='verdana')

subplot(10,1,3)
plot(xx110,Tx110,'o')
plot(xx75,Tx75,'o')
plot(xx46,Tx46,'o')
plot(xx30,Tx30,'o')
plot(xx20,Tx20,'o')
ylim(bottom=0)
title('Температура (гориз) от отстройки',fontsize=14,family='verdana')
legend('12345')

subplot(10,1,4)
plot(xx110,Ty110,'o')
plot(xx75,Ty75,'o')
plot(xx46,Ty46,'o')
plot(xx30,Ty30,'o')
plot(xx20,Ty20,'o')
title('Температура (верт) от отстройки',fontsize=14,family='verdana')
legend('12345')

#tmp = Ty75.argsort()
#sortedPeople = people[inds]

#plot(xx110,Ty110)
#plot(xx75,Ty75)
#plot(xx46,Ty46,)
#plot(xx30,Ty30)
#plot(xx20,Ty20)
#legend('12345')

subplot(10,1,5)
xs = [0.13, 0.2,0.3,0.5]
Tx = [Tx30[where(xx30==2)[0][0]],Tx46[where(xx46==2)[0][0]],0.5*Tx75[where(np.isclose(xx75,1.82))[0][0]]+0.5*Tx75[where(np.isclose(xx75,2.22))[0][0]],Tx110[where(xx110==2)[0][0]]]
Ty = [Ty30[where(xx30==2)[0][0]],Ty46[where(xx46==2)[0][0]],0.5*Ty75[where(np.isclose(xx75,1.82))[0][0]]+0.5*Ty75[where(np.isclose(xx75,2.22))[0][0]],Ty110[where(xx110==2)[0][0]]]
plot(xs,Tx,'bo')
plot(xs,Ty,'ro')
ylim(bottom=0)
print(Ty)


# In[228]:

where(xx75==2.02)[0][0]


# In[209]:

Tx30[where(xx30)==2]


# In[205]:

#help(sort)


# In[ ]:

# Шаблон
xx = []
yy = []
for d in data:
    tbl = d['avr_table']
    x = tbl.folder
    y = tbl.fit1D_x.sigma
    ff = d['fits'][0]
    fit_func = usfuncs.cloud_expansion0
    plot(x,fit_func(x,*ff[1]))
    plot(x,y,'o',label=d['date_meas'])
legend()
ylim(bottom=0)


# In[ ]:

os.chdir(r'/Users/artemgolovizin/Downloads/2015_12_01')


# In[ ]:

old_ks = dict()


# In[ ]:

with open('all_data.txt', 'rb') as handle:
    data = pickle.loads(handle.read())


# In[ ]:

data.keys()


# In[ ]:

data['01 t']


# In[ ]:

with open('all_data.txt', 'rb') as handle:
    data = pickle.loads(handle.read())
shot_typeN = 1
ks = list(data.keys())
ks.sort()
ch_boxes = dict()
ks_n = []
for k in ks:
    # optional - uncomment line below to sift only keys with specific marker, as 'CL'
#    if 'CL' not in k.upper(): continue
    ch_boxes[k]=old_ks.get(k,True)
    ks_n.append(k)
ks = ks_n
fg = None   
def plot_gr(l_pos,**ar):
    fig,ax = subplots() 
    global fg, old_ks
    old_ks = dict()
    for k in ks:
        old_ks[k]=ar[k]
        if ar[k]:
            d1 = impr.get_avr_data(data[k]['data'], shot_typeN, 'fit1D_x',2)
            errorbar(**d1)
#             d1['fmt']='ro'
#             d1['label']='fit1D_x'
#             val=datat[k]
#             x,y=impr.data2_sort(val[0],val[1])
#             # here it's time to modify data
# #             x = mod_from_AOM_to_real_freq(x, k, 420)
#             #x,y = x[1:],y[1:]
#             ax.plot(x,y,'-*',label=k)
    legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=15)
    #xscale('log')
    #xlabel('Current, A')
    #xlabel('AOM frequency, MHz')
    xlabel('detuning, MHz') #in real frequencyes
    ylabel('atoms number, a.u.')
    ylim(bottom=0)
    #start, end = ax.get_xlim()
    #print(ax.get_xlim())
    #ax.xaxis.set_ticks(arange(start, end, 0.1))
    #axvline(x=l_pos)
    fg = fig
    
ter = interactive(plot_gr,l_pos=(150,250,0.1),**ch_boxes)
ter.box_style='info'
display(ter)


# In[ ]:

help(interactive)


# ###For managing clock line shift and broadening
c_freq = 420 # MHz
working_keys = [x for x in old_ks if old_ks[x]]
print(working_keys)
val1 = []
val2 = []
for key in working_keys:
    # get fit data
    popt = res_dict[key][2]
    for s0 in key.rstrip(r'\/ ').split():
        if '=' in s0:
            s1 = s0.split('=')
            # here one can extract data from folder name of patten 'var=val'
            if s1[0] == 'mod' or s1[0] == 'min':
                val1.append((float(s1[1]), popt[1]))
                val2.append((float(s1[1]), popt[2]))
fig3, ax3 = subplots(1,2,figsize=(12,6))
x, y = list(zip(*val1))
y = mod_from_AOM_to_real_freq(array(y), 'CL', c_freq)
ax3[0].plot(x,y,'*r',ms=10)
ax3[0].set_title('shift (center frequency=' + str(c_freq) + 'MHz)')
ax3[0].set_ylabel('shift, MHz')
ax3[0].set_xlabel('power, W')
x, y = list(zip(*val2))
ax3[1].set_title('width')
ax3[1].set_ylabel('width, MHz')
ax3[1].set_xlabel('power, W')
ax3[1].plot(x,y,'*r',ms=10)
#x, y = list(zip(*val))
#plot(x,y,'*')
# #### Построение списка сканирования

# In[ ]:

res = array(range(-7,7, 1))/10 + 420.1
rr = ''
for x in res:
    rr += str(x) + ' '
print(rr)


# In[ ]:




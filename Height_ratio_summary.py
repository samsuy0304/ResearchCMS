from itertools import islice
import sys, re, os
import numpy as np
import statistics
import skrf as rf
#print(rf.__version__)
#print(.__version__)
#rf.stylely()
#############################################################################################################################

#iMPORTS
import pylab
import pandas as pd
import mpld3
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl



##########################################################################################################################

# USER DEFINED FUNCTIONS
def set_axes(ax, title, ymin, ymax, xmin, xmax, nolim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='0.8', which='minor')
    ax.grid(True, color='0.4', which='major')
    ax.set_title(title) #Time domain
    if nolim==False:
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
    plt.tight_layout()

########################################################################################################################
#NOTES FOR THE SCRIPT
#The dictionary has the lengths ordered in D1, D0, CMD0


#######################################################################################################333333333333#########

                                  #Data
Boardtype= 1          # Boardtype is 1 and 2 for yellow and L- board respectively


#channels
if Boardtype==1:
    chnn=["ChD1", "ChD0", "CMD0"]
elif Boardtype==2:
    chnn=["CHD3", "CHD2","ChD1", "ChD0", "CMD0"]
#HEIGHT OF EYES FOR VARIOUS LENGTHS
xforeye=[(412.36,475.22,484.41),(415.79,485.46,476.93),(409.26,442.06,379.88),(420.33,437.16,453.68),(425.59,396.78,455.57)]

#NOTATION FOR 34 GAUGE WIRES

x_34gvalues=[3560,3561,3556,3558,3559]

#REPSECTIVE HEIGHTS ORDERED IN CH1,CH0,CMD0

if Boardtype ==1:
    y_34gvalues=[(221.4,234.4,221.64),(205.71,232,221.35),(198.97,223.7,217.61),(212.24,226.77,204.13),(215.85,219.97,203.76)]
elif Boardtype==2:
    y_34gvalues=[(156.39,145.46,157.95,165.08,132.17),(144.5,151.92,145.38,160.92,144.02),(161.87,160.2,147.55,165.25,137.32),(159.66,163.41,146.1,130.46,127.01),(155.85,148.05,145.95,152.2,142.82)]

#NOATIONS FOR 35 GAUGE WIRES

x_36gvalues = [3562,3563,3550,3551,3552]

#rESPECTIVE HEIGHTS ORDERED IN CH1, CH0, CMD0
if Boardtype ==1:
    y36=[(257.75,274.37,261.38),(263.58,254.71,261.05),(259.65,273.93,240.93),(239.65,270.95,248.53),(233.29,255.77,222.78)]
elif Boardtype==2:
    y36=[(198.49,194.99,182.89,173.6,178.12),(167.18,166.86	,170.66,167.75,	167.15),(151.65,160.43,	164.83,	165.25,	140.24),(179.49,190.27,	152.42,	170.34,	148.74),(121.26,142.04,	140.07,	187.15,	174.68)]

#number of elements
if Boardtype==1:
    mn = 3
elif Boardtype==2:
    mn = 5

#Labels

labelslist=["62/60","62/61","62/56","62/58","62/59",
"63/60","63/61","63/56","63/58","63/59",
"50/60","50/61","50/56","50/58","50/59",
"51/60","51/61","51/56","51/58","51/59",
"52/60","52/61","52/56","52/58","52/59",]
###########################################################################################################################3

#TABLE CREATED

if Boardtype==1:
    print("Wire ID\t\tD1\t\t\tD0\t\tCMD0")
if Boardtype==2:
    print("Wire ID\t\tD3\t\t\tD2\t\tD1\t\tD0\t\tCMD0")
print("For 34G")
for i in range(len(y_34gvalues)):
    print(x_34gvalues[i],end="          ")
    for j in range(mn):
        print(f"{y_34gvalues[i][j]:2f}\t", end="   ")
    print()
print("For 36 G")
for i in range(len(y36)):
    print(x_36gvalues[i],end="          ")
    for j in range(mn):
        print(f"{y36[i][j]:2f}\t", end="   ")
    print()


##############################################################################################################################3
                                    #RATIOS
CHD3list=[]
CHD2list=[]
CHD1list=[]
CHD0list=[]
CMD0list=[]

for i in range(5): #i is 36 g
    for k in range(5): #k is 34g
        for j in range(mn): # j is channel
            if Boardtype==1:
                print(f"{x_36gvalues[i]} / {x_34gvalues[k]}\t{y36[i][j]}\t{y_34gvalues[k][j]}      =     {y36[i][j]/y_34gvalues[k][j]:6f}",    {chnn[j]}, end="")
                if j ==0:
                    CHD1list.append(y36[i][j]/y_34gvalues[k][j])
                elif j ==1:
                    CHD0list.append(y36[i][j]/y_34gvalues[k][j])
                elif j ==2:
                    CMD0list.append(y36[i][j]/y_34gvalues[k][j])
            if Boardtype==2:
                print(f"{x_36gvalues[i]} / {x_34gvalues[k]}\t{y36[i][j]}\t{y_34gvalues[k][j]}      =     {y36[i][j]/y_34gvalues[k][j]:6f}",    {chnn[j]}, end="")
                if j ==0:
                    CHD3list.append(y36[i][j]/y_34gvalues[k][j])
                elif j ==1:
                    CHD2list.append(y36[i][j]/y_34gvalues[k][j])
                elif j ==2:
                    CHD1list.append(y36[i][j]/y_34gvalues[k][j])
                elif j ==3:
                    CHD0list.append(y36[i][j]/y_34gvalues[k][j])
                elif j ==4:
                    CMD0list.append(y36[i][j]/y_34gvalues[k][j])

            print()
        print()
    print("-"*50)





#############################################################################################################################
#PLOTS

fig = plt.figure(figsize=(15, 20))
fig.patch.set_facecolor('xkcd:black')
plt.style.use('dark_background')  #This is what worked for the background style

ax0=plt.subplot(2,1,1)
ax1=plt.subplot(2,1,2)

ax0.plot(x_34gvalues,y_34gvalues,'ro',color='red', label='34G')
ax0.plot(x_36gvalues,y36, 'ro', color='blue', label='34G')
ax0.set_xlabel('Wire Codes')
ax0.set_title('Channel Heights')
ax0.set_ylabel('Height (mV)')
ax0.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

if Boardtype==1:
    #for i in range(0,len(plotsfordivi),3):
    fig.suptitle('Ratio Plots for 35cm (Yellow Board)', fontsize=16)
    ax1.plot(labelslist,CHD1list,'-ok', color='blue', label='ChD1')

    #for i in range(1,len(plotsfordivi),3):
    ax1.plot(labelslist,CHD0list,'-ok', color='red', label='CHD0')

    #for i in range(2,len(plotsfordivi),3):
    ax1.plot(labelslist,CMD0list,'-ok' ,color='green', label='CMD0')
    ax1.set_xlabel('Wire Pair')
    ax1.set_title('Ratios of 36G to 34G')
    ax1.set_ylabel('Ratio')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
elif Boardtype==2:
    fig.suptitle('Ratio Plots for 35cm (L Board)', fontsize=16)
    ax1.plot(labelslist,CHD3list,'-ok', color='pink', label='ChD3')
    ax1.plot(labelslist,CHD2list,'-ok', color='purple', label='ChD2')
    ax1.plot(labelslist,CHD1list,'-ok', color='blue', label='ChD1')
    ax1.plot(labelslist,CHD0list,'-ok', color='red', label='ChD0')
    ax1.plot(labelslist,CMD0list,'-ok', color='green', label='CMD0')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax1.set_xlabel('Wire Pair')
    ax1.set_title('Ratios of 36G to 34G')
    ax1.set_ylabel('Ratio')

plt.show()

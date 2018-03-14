# -*- coding: utf-8 -*-
##直接用了现有的成份指数 金融、大盘，但是没有找出来所在象限比较稳定的模式
from WindPy import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from hpfilter import hpfilter

w.start()
##"PriceAdj=B"  "Period=W" 注释
t1="2008-1-1"  ##开始时间
t2="2018-2-5"
a=w.wsd("000992.SH", "close", t1,t2)  ##中证全指金融
#a=w.wsd("801811.SI", "close", t1, t2)  ##申万大盘
#if ErrorCode==0:
S=np.array(a.Data[0])
T= a.Times
R=np.log(S/S[0])
##对立:中证全指
Sm=np.array(w.wsd("H20903.CSI", "close", t1, t2).Data[0])
Rm=np.log(Sm/Sm[0])

##相对价格指数
I=R-Rm
I_smt=hpfilter(I,1600)  ##用滤波方法进行平滑
#plt.plot(T,I,T,I_smt)
#plt.show()

##一阶导 直接差分
I1=[0]
for i in range(1,len(I_smt)):
    I1.append(I_smt[i]-I_smt[i-1])
##二阶导
I2=[0,0]
for i in range(2,len(I1)):
    I2.append(I1[i]-I1[i-1])

#plt.plot(I2, I1,'b')
#plt.show()

##判断象限
##没意义 这个统计是没意义的 因为用了未来信息 至少平滑用到了
#p=[]   #储存所在象限1 2 3 4分别代表第1 2 3 4象限
#for i in range(len(I2)):
#    if I1[i]>0 and I2[i]>0:
#        p.append(1)
#    elif I1[i]>0 and I2[i]<0:
#        p.append(2)
#    elif I1[i]<0 and I2[i]<0:
#        p.append(3)
#    else:
#        p.append(4)

#f=pd.DataFrame({'T':T[2:len(p)],'sw':S[2:],'zz':Sm[2:],'xiangxian':p[2:],'beta1':I1[2:],'beta2':I2[2:]})
#f.to_csv('xiangxian.csv',index = None)

####进行测试
##思路一 用2年数据平滑
#T[490]
for i in range(1968):
    Sc=S[0+i:490+i]
    Rc=np.log(Sc/Sc[0])##如果是2年的话基准会变
    Smc=Sm[0+i:490+i]
    Rmc=np.log(Smc/Smc[0])
    Ic=Rc-Rmc
    I_smtc=hpfilter(Ic,1600) #w的取值

    I1=[] ##取了后3个
    for i in range(len(I_smtc)-3,len(I_smtc)):
        I1.append(I_smtc[i]-I_smtc[i-1])

    I2=[] ##取了后2个
    for i in range(1,len(I1)):
        I2.append(I1[i]-I1[i-1])

    signal=[]	##策略产生的信号 也可以看作持仓
    if (I1[-1]>=0 and I2[-1]>=0)and (I1[-2]<=0 and I2[-2]>=0):
        signal.append(1)
    elif (I1[-1]<=0 and I2[-1]<=0)and (I1[-2]>=0 and I2[-2]<=0):
        signal.append(-1)  ##卖空限制就让这个取0
    else:
        signal.append(0)
    ##考虑手续费
    ##下面代码是计算需要买卖（买卖数量只能是+-1 不考虑卖空）
    ##怎么算净值？
 
def apls(a):
	pass #todo


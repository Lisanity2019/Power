import matplotlib.pyplot as plt
import numpy as np

x=np.linspace(-2,2,50) #生成自变量X区间 
y1 = x
y2 = x ** 2
y3 = x ** 3 #函数表达式


plt.figure()
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3,linestyle='--') #绘制图像及属性设置

plt.xlim((0,2)) #X轴取值范围限制
plt.ylim((0,6)) #X轴取值范围限制
plt.ylabel("y轴")

# ax = plt.gca()
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.spines['bottom'].set_position(('data', 0))
# ax.spines['left'].set_position(('data', 0))  #设置坐标原点




plt.show() #显示绘制图像
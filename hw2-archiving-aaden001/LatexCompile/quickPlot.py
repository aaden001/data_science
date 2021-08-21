# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 22:46:21 2021

@author: adeni
"""
import matplotlib.pyplot as plt
   

FileType = ['HTML','Images','Audio/Video','PDF','JavaScript','CSS','Fonts','Plain text','Json','Dash/HlS']
Number_Of_Url = [84,183,0,0,250,77,58,8,107,0]
plt.figure(figsize=(20,10))
plt.bar(FileType, Number_Of_Url)
plt.title('FileType Vs Number_Of_Url')
plt.xlabel('FileType')
plt.ylabel('Number_Of_Url')
plt.show()

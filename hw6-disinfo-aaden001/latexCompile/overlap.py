# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 12:20:50 2021

@author: aadeniran
"""

import pandas as pd

#read the files in pandas dataframe
dfile1= pd.read_csv("D1.csv")
dfile2 = pd.read_csv("D2.csv")
dfile3 = pd.read_csv("D3.csv")

def compareThisB(lowerCase,upperCase):
    #create an empty final dataframe 
    number = 0
    column_name = ["Domain"]
    final = pd.DataFrame(columns = column_name)
    for index, row in upperCase.iterrows():
        #find a match(es) and store as a dataframe
        #set Uppercases domain to lowercase so that it can propermatch
        temp = lowerCase[lowerCase['Domain'] == row['Domain'].lower()]
        #print(dfile1[dfile1['Domain'] == row['Domain']])
        #check if data frame is empty
        if(len(temp) == 0):
            #assign NaN value
            #final = np.nan
            pass
        else:
        #    print(temp)
            #assigne Media Type to final value
            final.at[number,"Domain"] = temp['Domain'].iloc[0]
            number +=1
    return final


"""
    I could literally turn it to a function smh
   Q2 Part A compare D1 and D2
"""
finalA = compareThisB(dfile1,dfile2)

"""
   Q2 Part B compare D2 and D3
"""
finalB = compareThisB(dfile2,dfile3)
"""
   Q2 Part C compare D1 and D3
"""
finalC = compareThisB(dfile1,dfile3)

"""
   Q2 Part D compare finalA  and D3
"""
finalD = compareThisB(finalA,dfile3)


#convert to csv files
finalA.to_csv("Q2/finalA.csv", index = False, header=True)
finalB.to_csv("Q2/finalB.csv", index = False, header=True)
finalC.to_csv("Q2/finalC.csv", index = False, header=True)
finalD.to_csv("Q2/finalD.csv", index = False, header=True)
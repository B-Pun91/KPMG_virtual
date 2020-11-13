import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from collections import Counter
import math as ma

# reading the CustomerDemograohic sheet from the excel file
file_name = 'KPMG_VI_New_raw_data_update_final.xlsx'
sheet_name = 'NewCustomerList'

df = pd.read_excel(io=file_name, sheet_name=sheet_name)
# print(df)
# print (df.columns)

#remnaming column title in the excel file
df.rename(columns={"Note: The data and information in this document is reflective of a hypothetical situation and client. This document is to be used for KPMG Virtual Internship purposes only. ":"first_name",
                   "Unnamed: 1": "last_name",
                   "Unnamed: 2": "gender",
                   "Unnamed: 3": "past_3_years_bike_related_purchases",
                   "Unnamed: 4": "DOB",
                   "Unnamed: 5": "job_title",
                   "Unnamed: 6": "job_industry_category",
                   "Unnamed: 7": "wealth_segment",
                   "Unnamed: 8": "deceased_indicator",
                   "Unnamed: 9": "owns_car",
                   "Unnamed: 10": "tenure",
                   "Unnamed: 11": "address",
                   "Unnamed: 12": "postcode",
                   "Unnamed: 13": "state",
                   "Unnamed: 14": "country",
                   "Unnamed: 15": "property value",
                   "Unnamed: 21": "rank",
                   "Unnamed: 22": "value",
                   }, inplace = True)

df.drop(df.head(1).index, inplace=True)
#print(df)

# checking for missing values in each column
missingValue = df.isna().sum()
#print(missingValue)

#check the uinqueness for each entry in all columns
for col in df.columns[3:]:
    res = {col: df[col].value_counts()}
    #print (res)

#count total gender either male, female or unspecified in the dataset
def gendercount():
    Male= 0
    Female = 0
    Unspecified = 0
    for item in df['gender']:
        if item.startswith('M'):
            Male += 1
        elif item.startswith('F'):
            Female += 1
        else:
            Unspecified +=1
    return (Male, Female, Unspecified)

Totalcount = gendercount()
#print ("Male = "+ str(Totalcount[0]), "Female= " + str(Totalcount[1]), "Unspecified= "+str(Totalcount[2]))

#finding total purchases in last 3 years for all genders
#chanhing to str from int
df[['past_3_years_bike_related_purchases']] = df[['past_3_years_bike_related_purchases']].apply(pd.to_numeric)

#calcualtion of total purchase by each gender including unspecified
malePur = df.loc[df['gender'] == 'Male', 'past_3_years_bike_related_purchases'].sum() + df.loc[df['gender'] == 'M', 'past_3_years_bike_related_purchases'].sum()
femalePur = df.loc[df['gender'] == 'Female', 'past_3_years_bike_related_purchases'].sum() + df.loc[df['gender'] == 'F', 'past_3_years_bike_related_purchases'].sum()+df.loc[df['gender'] == 'Femal', 'past_3_years_bike_related_purchases'].sum()
unspecifiedPur =  df.loc[df['gender'] == 'U', 'past_3_years_bike_related_purchases'].sum()
#print(malePur,femalePur, unspecifiedPur)

#bar plot
N = len(Totalcount)
ind = np.arange(N)
width = 0.27
color1 = (0.2, 0.4, 0.6, 0.6)
color2 = (0.3, 0.1, 0.4, 0.6)
fig = plt.figure()
ax = fig.add_subplot()

data1 = [Totalcount[0], Totalcount[1], Totalcount[2]]
rects1 = ax.bar(ind, data1, width, color=color1)
data2 = [malePur,femalePur,unspecifiedPur]
rects2 = ax.bar(ind+width, data2, width, color=color2)

ax.set_ylabel('Total Number of People',weight='semibold')
ax.set_xlabel('Gender',weight='semibold')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Male', 'Female', 'Unspecified'))
ax.legend( (rects1[0], rects2[0]), ('Gender', 'Gender Purchases'))


#function to label the plots for each bar plot
def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.005*h, '%d'%float(h), ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
#plt.show()

#to save the bar plot
#plt.savefig("image1_1.png")

#bar plot of bike purchases by each gender in percentage
data1 = [malePur,femalePur,unspecifiedPur]
TotalPurchases = sum(data1)
#print(TotalPurchases)

avgPurchase = [0, 0, 0]
for x in range(len(data1)):
    avgPurchase[x] = round((data1[x]/TotalPurchases)*100,2)
#print(avgPurchase)

fig, ax = plt.subplots()
bar_width = 0.8
x = np.arange(len(avgPurchase))
rects3 = ax.bar(x, avgPurchase, bar_width, color=color1)
ax.set_ylabel('Bikes bought by each gender in percentage (%)', weight='semibold')
#plt.bar(x, avgPurchase, color = (0.2, 0.4, 0.6, 0.6), width = bar_width)
plt.xticks(x, ('Male','Female','Unspecified'))
ax.set_xlabel('Gender',weight='semibold')

def autolabel1(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.005*h, '%.2f'%float(h), ha='center', va='bottom')

autolabel1(rects3)

#to save the bar plot
# plt.savefig("image2_1.png")
# plt.show()

#finding the age of each customer using the DOB
df["Age"] = 0
totalCustomers = len(df["DOB"])
k    = 0
for x in range(1, totalCustomers):
    #if actual date
    if isinstance(df["DOB"][x], datetime.date):
        tl = len(df["DOB"][x].ctime().split(" "))
        df["Age"][x] += int(2020 - int(df["DOB"][x].ctime().split(" ")[tl-1]))
    #if date in string
    elif isinstance(df["DOB"][x], str):
        tl = len(df["DOB"][x].split("-"))
        df["Age"][x] += int(2020 - int(df["DOB"][x].split("-")[0]))

# print(df["Age"])
# print(df)


#dividing the total number of people within the specified age group
#finding the mean age and the standard deviation of the age
Male = 0
Female = 0
Unspecified = 0
j = 0
sum1 = 0
stdValue = []

for items in df['gender']:
    if items.startswith('M') and df['Age'][j + 1] != 0:
        sum1 += df['Age'][j+1]
        stdValue.append((df['Age'][j+1]))
        Male +=1
    elif items.startswith('F') and df['Age'][j + 1] != 0:
        sum1 += df['Age'][j+1]
        stdValue.append((df['Age'][j+1]))
        Female +=1
    elif df['Age'][j + 1] != 0:
        sum1 += df['Age'][j + 1]
        stdValue.append((df['Age'][j+1]))
        Unspecified +=1
    j +=1

meanValue = round(sum1/(Male + Female + Unspecified), 0)
overall_stdValue = round(ma.sqrt(1/((Male + Female + Unspecified)-1)*sum((stdValue - (sum1/(Male + Female + Unspecified)))**2)),0)
# print("Mean1", meanValue)
# print("std1", overall_stdValue)

#dividing the total number of people within the specified age group and bike purchases for both gender but ignoring unspecified
#male
mFirst = []
mSecond = []
mThird = []
mFourth = []

mBFirst = []
mBSecond = []
mBThird= []
mBFourth = []

#female
fFirst = []
fSecond = []
fThird = []
fFourth = []

fBFirst = []
fBSecond = []
fBThird = []
fBFourth = []

# four division of age depending upon the mean age and the standard deviation
#finding the upper end for each quarter
firstQ = round(meanValue - overall_stdValue/2,0)
secondQ = round(meanValue,0)
thirdQ = round(meanValue + overall_stdValue/2,0)
fourthQ = max(df['Age'])

print ("first quater", firstQ , "second quarter", secondQ, "third quarter", thirdQ, "fourth quarter", fourthQ)
i = 1
for items in df["gender"]:
    tAge = int (df["Age"][i])
    tPur = int(df["past_3_years_bike_related_purchases"][i])
    if items[0] == "M" and tAge != 0:
        if tAge <= firstQ:
            mFirst.append(tAge)
            mBFirst.append(tPur)
        elif tAge > firstQ  and tAge <= secondQ:
            mSecond.append(tAge)
            mBSecond.append(tPur)
        elif tAge > secondQ and tAge <= thirdQ:
            mThird.append(tAge)
            mBThird.append(tPur)
        elif tAge > thirdQ:
            mFourth.append(tAge)
            mBFourth.append(tPur)
    elif items[0] == "F" and tAge != 0:
        if tAge <= firstQ:
            fFirst.append(tAge)
            fBFirst.append(tPur)
        elif tAge > firstQ  and tAge <= secondQ:
            fSecond.append(tAge)
            fBSecond.append(tPur)
        elif tAge > secondQ and tAge <= thirdQ:
            fThird.append(tAge)
            fBThird.append(tPur)
        elif tAge > thirdQ:
            fFourth.append(tAge)
            fBFourth.append(tPur)
    i += 1

# print (len(mFirst), len(mSecond), len(mBThird), len(mFourth))
# print (len(fFirst), len(fSecond), len(fBThird), len(fFourth))


#bar plot
ind3 = np.arange(4)
bar_width3 = 0.27
color3= (0.1, 0.4, 0.5, 0.8)
color4 = (0.3, 0.2, 0.3, 0.4)
fig = plt.figure()
ax = fig.add_subplot()

data3 = [len(mFirst), len(mSecond), len(mBThird), len(mFourth)]
rects3 = ax.bar(ind3, data3, bar_width3, color=color3)
data4 =  [len(fFirst), len(fSecond), len(fBThird), len(fFourth)]
rects4 = ax.bar(ind3+bar_width3, data4, bar_width3, color=color4)


ax.set_ylabel('Total Number of People',weight='semibold')
ax.set_xlabel('Age group within each gender',weight='semibold')
ax.set_xticks(ind3+bar_width3)
ax.set_xticklabels(('First', 'Second', 'Third', 'Fourth'))
ax.legend( (rects3[0], rects4[0]), ('Male', 'Female'))

autolabel(rects3)
autolabel(rects4)

#to save the bar plot
#plt.savefig("image3_1.png")
# plt.show()

#finding total job categories
counts = Counter(df['job_industry_category'])
#print (counts)

# 10 job categories including n/a, finding the exact number of customers within the specific job category
manu = 0
finS = 0
hea = 0
rea = 0
pro = 0
it = 0
ent = 0
agr = 0
tel = 0
for items in df["job_industry_category"]:
    if str(items).startswith('M'):
        manu += 1
    elif str(items).startswith('F'):
        finS += 1
    elif str(items).startswith('H'):
        hea += 1
    elif str(items).startswith('R'):
        rea += 1
    elif str(items). startswith('P'):
        pro += 1
    elif str(items).startswith('I'):
        it += 1
    elif str(items).startswith('E'):
        ent += 1
    elif str(items).startswith('A'):
        agr += 1
    elif str(items).startswith('T'):
        tel += 1

#print ( manu, finS, hea, rea, pro, it, ent, agr, tel)

#bar plot
ind5 = np.arange(9)
bar_width5 = 0.28
color5 = (0.5, 0.1, 0.4, 0.2)
fig = plt.figure()
ax = fig.add_subplot()

data5 = ( manu, finS, hea, rea, pro, it, ent, agr, tel)
rects5 = ax.bar(ind5+bar_width5, data5, bar_width5, color=color5)

ax.set_ylabel('Total Number of People',weight='semibold')
ax.set_xlabel('Job Categories',weight='semibold')
ax.set_xticks(ind5+bar_width5)
ax.set_xticklabels(('Manufac', 'Finance', 'Health', 'Retail', 'Property', 'IT', 'Ent', 'Agri', 'Telecom'))
plt.xticks(rotation=30)
autolabel(rects5)

#to save the bar plot
# plt.savefig("image4_1.png")
# plt.show()

#in regards to the wealth segment
mFQ = []; mSQ = []; mTQ = []; mFoQ = []
hFQ = []; hSQ = []; hTQ = []; hFoQ = []
aFQ = []; aSQ = []; aTQ = []; aFoQ = []
i = 1

for items in df['wealth_segment']:
    tAge = int(df["Age"][i])
    if items[0] == "M" and tAge != 0:
        if tAge <= firstQ:
            mFQ.append(tAge)
        elif tAge > firstQ  and tAge <= secondQ:
            mSQ.append(tAge)
        elif tAge > secondQ and tAge <= thirdQ:
            mTQ.append(tAge)
        elif tAge > thirdQ:
            mFoQ.append(tAge)
    elif items[0] == "H" and tAge != 0:
        if tAge <= firstQ:
            hFQ.append(tAge)
        elif tAge > firstQ  and tAge <= secondQ:
            hSQ.append(tAge)
        elif tAge > secondQ and tAge <= thirdQ:
            hTQ.append(tAge)
        elif tAge > thirdQ:
            hFoQ.append(tAge)
    elif items[0] == "A" and tAge != 0:
        if tAge <= firstQ:
            aFQ.append(tAge)
        elif tAge > firstQ  and tAge <= secondQ:
            aSQ.append(tAge)
        elif tAge > secondQ and tAge <= thirdQ:
            aTQ.append(tAge)
        elif tAge > thirdQ:
            aFoQ.append(tAge)
    i += 1

# print (len(mFQ), len(mSQ), len(mTQ), len(mFoQ))
# print (len(hFQ), len(hSQ), len(hTQ), len(hFoQ))
# print (len(aFQ), len(aSQ), len(aTQ), len(aFoQ))

#bar plot
ind6= np.arange(4)
bar_width6 = 0.27
color6= (0.1, 0.4, 0.5, 0.8)
color7 = (0.3, 0.2, 0.3, 0.4)
color8 = (0.5, 0.3, 0.4, 0.8)
fig = plt.figure()
ax = fig.add_subplot()

data6 = [len(mFQ), len(mSQ), len(mTQ), len(mFoQ)]
rects6 = ax.bar(ind6, data6, bar_width6, color=color6)
data7 =  [len(hFQ), len(hSQ), len(hTQ), len(hFoQ)]
rects7 = ax.bar(ind6+bar_width6, data7, bar_width6, color=color7)
data8 =  [len(aFQ), len(aSQ), len(aTQ), len(aFoQ)]
rects8 = ax.bar(ind6+2*bar_width6, data8, bar_width6, color=color8)


ax.set_ylabel('Total Number of People',weight='semibold')
ax.set_xlabel('Age group',weight='semibold')
ax.set_xticks(ind3+bar_width3)
ax.set_xticklabels(('First', 'Second', 'Third', 'Fourth'))
ax.legend( (rects6[0], rects7[0], rects8[0]), ('Mass', 'High Net', 'Affluent'))

autolabel(rects6)
autolabel(rects7)
autolabel(rects8)

#to save the bar plot
# plt.savefig("image5_1.png")
# plt.show()

#finding total states
counts = Counter(df['state'])
#print (counts)

#analysis og customer who onws and car and  doesn't based on their state
NSW_y = 0; NSW_n = 0
VIC_y = 0; VIC_n = 0
QLD_y = 0; QLD_n = 0
i = 1

for items in df['state']:
    if items == 'NSW':
        if df['owns_car'][i]== "Yes":
            NSW_y += 1
        else:
            NSW_n += 1
    elif items == 'VIC':
        if df['owns_car'][i] == "Yes":
            VIC_y += 1
        else:
            VIC_n += 1
    elif items == 'QLD':
        if df['owns_car'][i]== "Yes":
            QLD_y += 1
        else:
            QLD_n += 1
    i += 1

#print (NSW_y, NSW_n, VIC_y, VIC_n, QLD_y, QLD_n)

#bar plot
ind8 = np.arange(3)
bar_width8 = 0.27
color8= (0.3, 0.1, 0.2, 0.5)
color9 = (0.2, 0.4, 0.3, 0.7)
fig = plt.figure()
ax = fig.add_subplot()

data8 = [NSW_y, VIC_y, QLD_y]
rects8 = ax.bar(ind8, data8, bar_width8, color=color8)
data9 = [NSW_n, VIC_n, QLD_n]
rects9 = ax.bar(ind8+bar_width8, data9, bar_width8, color=color9)


ax.set_ylabel('Total Number of People',weight='semibold')
ax.set_xlabel('State',weight='semibold')
ax.set_xticks(ind3+bar_width3)
ax.set_xticklabels(('NSW', 'VIC', 'QLD'))
ax.legend( (rects8[0], rects9[0]), ('Owns car', 'Doesn\'t own car'))

autolabel(rects8)
autolabel(rects9)

#to save the bar plot
#plt.savefig("image6_1.png")
# plt.show()





'''
verify that the backend is set.
python3 -c 'import matplotlib; import matplotlib.pyplot; print(matplotlib.backends)'
'''
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
# from openpyxl.workbook import Workbook # Not Implemeneted
import numpy as np
import requests

# Set up some vars
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
workingPath = '/your/working/directory/covidStats/'

newDataRequest = str(input('Do you require a refreshed dataset[y/n]? default[n] '))
if newDataRequest == 'y' or newDataRequest == 'Y':
    print('Downloading new dataset')
    r = requests.get(url)
    with open(workingPath+'freshData.csv', 'wb') as f:
        f.write(r.content)
else:
    print('Alright then, I\'ll work with what I\'ve got')

# The order of the datapoints needs to be reversed for an appropriate visualization
rawData = pd.read_csv('freshData.csv', sep = ',')
reversedDataset = pd.DataFrame(rawData)
reversedDataset = reversedDataset.iloc[::-1]


# define dataset as truth source
dataset = reversedDataset


# Create country specific Report and store each report as discrete dataset/file
NlReport = (dataset.loc[dataset['geoId'] == 'NL'])
ItReport = (dataset.loc[dataset['geoId'] == 'IT'])
UkReport = (dataset.loc[dataset['geoId'] == 'UK'])
UsReport = (dataset.loc[dataset['countriesAndTerritories'] == 'United_States_of_America'])
EsReport = (dataset.loc[dataset['geoId'] == 'ES'])
FrReport = (dataset.loc[dataset['geoId'] == 'FR'])
DEReport = (dataset.loc[dataset['geoId'] == 'DE'])
storedNl = NlReport.to_csv('NL_report.csv', index = None)
storedIt = ItReport.to_csv('IT_report.csv', index = None)
storedUs = UsReport.to_csv('US_report.csv', index = None)
storedfUk = UkReport.to_csv('UK_report.csv', index = None)
storedfEs = EsReport.to_csv('ES_report.csv', index = None)
storedfFr = FrReport.to_csv('FR_report.csv', index = None)
storedfDe = FrReport.to_csv('DE_report.csv', index = None)

# read country specific report as new dataset
reportNl = pd.read_csv('NL_report.csv')
reportIt = pd.read_csv('IT_report.csv')
reportUs = pd.read_csv('US_report.csv')
reportUk = pd.read_csv('UK_report.csv')
reportEs = pd.read_csv('ES_report.csv')
reportFr = pd.read_csv('FR_report.csv')
reportDe = pd.read_csv('DE_report.csv')

#### Plotting #####

#set style of plot
plt.style.use('bmh')
#plt.style.use('dark_background')

# create a graph figure and axis
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

# plot cases against date for each country and scatter deaths
# Cleaning Data: using .replace to remove zero-value and substitute with NaN.
ax.plot(reportNl['dateRep'], reportNl['cases'].replace(0, np.nan), label= "NL", color='r')
ax.scatter(reportNl['dateRep'], reportNl['deaths'].replace(0, np.nan), alpha=0.5, marker='o',label= "NL Deaths", color='r')
ax.plot(reportIt['dateRep'], reportIt['cases'].replace(0, np.nan), label= "IT", color='b')
ax.scatter(reportIt['dateRep'], reportIt['deaths'].replace(0, np.nan), alpha=0.5, marker='o', label= "IT Deaths", color='b')
ax.plot(reportUs['dateRep'], reportUs['cases'].replace(0, np.nan), label= "US", color='g')
ax.scatter(reportUs['dateRep'], reportUs['deaths'].replace(0, np.nan), alpha=0.5, marker='o',label= "US Deaths", color='g')
ax.plot(reportUk['dateRep'], reportUk['cases'].replace(0, np.nan), label= "UK", color='orange')
ax.scatter(reportUk['dateRep'], reportUk['deaths'].replace(0, np.nan), alpha=0.5, marker='o',label= "UK Deaths", color='orange')
ax.plot(reportEs['dateRep'], reportEs['cases'].replace(0, np.nan), label= "ES", color='purple')
ax.scatter(reportEs['dateRep'], reportEs['deaths'].replace(0, np.nan), alpha=0.5, marker='o',label= "ES Deaths", color='purple')
ax.plot(reportEs['dateRep'], reportEs['cases'].replace(0, np.nan), label= "FR", color='gray')
ax.scatter(reportFr['dateRep'], reportFr['deaths'].replace(0, np.nan), alpha=0.5, marker='o',label= "FR Deaths", color='gray')
ax.plot(reportDe['dateRep'], reportDe['cases'].replace(0, np.nan), label= "DE", color='black')
ax.scatter(reportDe['dateRep'], reportDe['deaths'].replace(0, np.nan), alpha=0.5, marker='o',label= "De Deaths", color='black')

# Set up Plot Title and lables
ax.tick_params(labeltop=False, labelright=True)
ax.set_title('COVID-19 Dataset - Compare stats')
ax.set_xlabel('Date')
ax.set_ylabel('Daily Reports')

# limit plot area x,y axis
#ax.set_xlim(0, 200)
ax.set_ylim(0, 50000)
#ax.xaxis.set_major_locator(MultipleLocator(20))
ax.yaxis.set_major_locator(MultipleLocator(1000))
#ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(10))

# set grid style and color (excluded now as using plt.style.use())
ax.grid(which='major', axis='y', color='#CCCCCC', linestyle='--')
#ax.grid(which='minor', color='#CCCCCC', linestyle=':')
#ax.set_facecolor('#d8dcd6')

# create vars for x,y to handle font sizes and text rotation
xmark = ax.get_xticklabels()
ymark = ax.get_yticklabels()
plt.setp(xmark, rotation = 45, fontsize = 6)
plt.setp(ymark, fontsize = 6)

# place legenda and show() plot
plt.legend(loc = "upper left")
plt.show()

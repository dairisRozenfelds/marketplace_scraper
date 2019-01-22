import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pymongo
from scrapy.conf import settings
from car_brands.car_brand import CarBrand

class ItemCollection:
    def __init__(self, collection, name):
        self.collection = collection
        self.collectionName = name
        self._buildDataFrame()
        self.df = self._buildDataFrame()

    def _getSpecificFieldList(self, modelList:list, fieldName:str):
        if fieldName == 'price':
            return [int(model[fieldName]) for model in modelList]
        else:
            return [model[fieldName] for model in modelList]

    def _buildDataFrame(self):
        return pd.DataFrame({
            'year': self._getSpecificFieldList(self.collection.getModelList(), 'year'),
            'price': self._getSpecificFieldList(self.collection.getModelList(), 'price'),
            'model': self._getSpecificFieldList(self.collection.getModelList(), 'model')
        })

    def getDataFrame(self):
        return self.df

    def addToPlot(self, ax, allYearList):
        for labelModel, dfModel in self.df.groupby('model'):
            yearList = allYearList
            for labelYear, dfYear in dfModel.groupby('year'):
                yearList[labelYear] = dfYear['price'].mean()
            ax.plot(list(yearList.keys()), list(yearList.values()), label=labelModel + ' (' + self.collectionName + ')')

    
connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
db = connection[settings['MONGODB_DB']]

# Add collections to compare
collections = [
    ItemCollection(CarBrand(db, 'bmw', [
        '320'
    ]), 'SS.COM'),
    ItemCollection(CarBrand(db, 'bmw_autoplius', [
        '320'
    ]), 'Autoplius.lt')
]

# Concatinate every year data
yearList = {}

for year, data in pd.concat([collection.getDataFrame() for collection in collections]).groupby('year'):
    yearList[year] = None

fig, ax = plt.subplots()
for collection in collections:
    collection.addToPlot(ax, yearList)
    
plt.xlabel('Year')
plt.ylabel('Price')
plt.grid(True)
plt.legend(title='Models')
plt.show()


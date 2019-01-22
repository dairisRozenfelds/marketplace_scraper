class CarBrand:
    _modelList = []

    def __init__(self, database, collectionName, modelList:list = []):
        self.db = database
        self.collectionName = collectionName
        self.filterEntryModels(modelList)

    def filterEntryModels(self, modelList:list):   
        if len(modelList):
            self._modelList = [model for model in self.db[self.collectionName].find({'model': {'$in': modelList}})]
        else:
            self._modelList = [model for model in self.db[self.collectionName].find()]
        
    def getModelList(self):
        return self._modelList
import pandas as pd
import numpy as np

class MockDB:
    def __init__(self):
        self.data = {
            "ALeRCE_microlensing": None,
            "Zooniverse": None,
            "AstroColibri":None,
            "Lasair_categories":None,
            "ANTARES_microlensing_filter":None,            
            "FINK_microlensing":None, 
            "AMPEL_microlensing_filter":None 
        }

    def create_alerce_data(self, mean=0, std_dev=1, size=10):
        data = np.random.normal(mean, std_dev, size)
        df = pd.DataFrame(data, columns=['value'])
        self.data["ALeRCE_microlensing"] = df

    def create_fink_data(self, min_val=0, max_val=100, size=10):
        #needs more realistic distribution
        data = np.random.uniform(min_val, max_val, size)
        df = pd.DataFrame(data, columns=['value'])
        self.data["FINK_microlensing"] = df

    
    def create_lasair_data(self,size=10):
        #Variable star VS, Cataclysmic Variable CV, Bright Star BS, Active Galactive Nucleus AGN, Nuclear Transient NT, Supernova SN, Orphan O
        category_labels = np.array(["VS","CV","BS","AGN","NT","SN","O"])
        categories = pd.Series(category_labels[np.random.randint(0,6,size)]).astype('category')
        self.data["Lasair_categories"] = categories

db = MockDB()

# need to be adjusted to actual distribution, e.g. resampled from broker stream
db.create_alerce_data(mean=10, std_dev=2)
db.create_fink_data(0,100)
db.create_lasair_data(55)


#!/usr/bin/env python
# coding: utf-8

# In[29]:


import requests
from datetime import datetime
import pandas as pd


# In[387]:


class disney_park:
    API_BASE = "https://api.wdpro.disney.go.com/"
    
    def __init__(self):
        self.tokendata = self.__get_tokendata()
        self.token = self.tokendata['access_token']
        self.expirtime = self.tokendata['expires_in']
        self.parkid = self.get_parkid()
        self.resortid = self.get_resortid()
        self.rawwaitdata = self.__get_rawwaitdata()
        self.size = len(self.rawwaitdata['entries'])
        self.waitdata = self.__get_waitdata()
        self.timeretrieved = self.__get_time()
        self.__entertainment_indeces = self.__get_ent_indeces()
        self.__reverse_ent_indeces = list(set(range(0,self.size)) - set(self.__entertainment_indeces))
        self.waitdata_attractions = self.waitdata.iloc[:,self.__reverse_ent_indeces]
        self.waitdata_entertainement = self.waitdata.iloc[:,self.__entertainment_indeces]
        if self.can_get_fastpass(): 
            self.fastpass = self.get_fastpass()
            self.__truefastpassindex = self.get_fastpass(index = True)
            self.fastpasstrue = self.fastpass.iloc[:,self.__truefastpassindex]

    
    
    def refresh(self):
        self.tokendata = self.__get_tokendata()
        self.token = self.tokendata['access_token']
        self.expirtime = self.tokendata['expires_in']
        self.parkid = self.get_parkid()
        self.resortid = self.get_resortid()
        self.rawwaitdata = self.__get_rawwaitdata()
        self.size = len(self.rawwaitdata['entries'])
        self.waitdata = self.__get_waitdata()
        self.timeretrieved = self.__get_time()
        self.__entertainment_indeces = self.__get_ent_indeces()
        self.__reverse_ent_indeces = list(set(range(0,self.size)) - set(self.__entertainment_indeces))
        self.waitdata_attractions = self.waitdata.iloc[:,self.__reverse_ent_indeces]
        self.waitdata_entertainement = self.waitdata.iloc[:,self.__entertainment_indeces]
    
    def __get_tokendata(self):
        TOKEN_URL = 'https://authorization.go.com/token?grant_type=assertion&assertion_type=public&client_id=WDPRO-MOBILE.MDX.WDW.ANDROID-PROD'
        r = requests.post(url = TOKEN_URL)
        data = r.json()
        return(data)
    
    def __get_parkid(self):
        raise("Method Must Be Defined By Inherited Class")

        
    def __get_resortid(self):
        raise("Method Must Be Defined By Inherited Class")
        
    def __get_rawwaitdata(self):
        API_BASE = "https://api.wdpro.disney.go.com/"
        headers = {
        'Accept-Language' : 'en_US',
        'User-Agent': 'UIEPlayer/2.1 iPhone OS 6.0.1',
        'Accept' : 'application/json;apiversion=1',
        'Authorization' : "BEARER "+str(self.token),
        'X-Conversation-Id' : 'WDPRO-MOBILE.MDX.CLIENT-PROD',
        'X-Correlation-ID' : str(datetime.now().timestamp())

        }
        r = requests.get(url = API_BASE+'facility-service/theme-parks/{}/wait-times'.format(self.parkid),headers=headers)
        data = r.json()
        return(data)
    
    def __get_time(self):
        time = datetime.now()
        return(time)
    
    def __get_waitdata(self):
        rawdata = self.rawwaitdata
        names = []
        times = []
        for i in range(0,self.size):
            names.append(str(i) + rawdata['entries'][i]['name'])
            try:
                times.append([rawdata['entries'][i]['waitTime']['postedWaitMinutes']])
            except KeyError:
                times.append([rawdata['entries'][0]['waitTime']['status']])
                

        data = dict(zip(names,times))
        data = pd.DataFrame.from_dict(data)
        return(data)
    
    def __get_ent_indeces(self):
        types = []
        for i in range(0,len(self.rawwaitdata['entries'])):
            types.append(self.rawwaitdata['entries'][i]['type'])
            
        indeces = [i for i,x in enumerate(types) if x=='Entertainment']
        return(indeces)
        
    def get_fastpass(self,index = False):
        rawdata = self.rawwaitdata
        names = []
        times = []
        indeces = []
        for i in range(0,self.size):
            names.append(str(i) + rawdata['entries'][i]['name'])
            if rawdata['entries'][i]['waitTime']['fastPass']['available']:
                indeces.append(i)
                times.append([rawdata['entries'][i]['waitTime']['fastPass']['startTime']])
            else:
                times.append('Not Available')
                

        data = dict(zip(names,times))
        data = pd.DataFrame.from_dict(data)
        if index ==True:
            return(indeces)
        else:
            return(data)
        
    def can_get_fastpass(self):
        raise(("Method Must Be Defined By Inherited Class"))
        



# In[388]:


class Disneyland(disney_park):
        
    def get_parkid(self):
        return(330339)

        
    def get_resortid(self):
        return(80008297)
    
    def can_get_fastpass(self):
        return(True)

class CaliforniaAdventure(disney_park):
    def get_parkid(self):
        return(336894)

        
    def get_resortid(self):
        return(80008297)
    
    def can_get_fastpass(self):
        return(True)
    
class MagicKingdom(disney_park):
    
    def get_parkid(self):
        return(80007944)

        
    def get_resortid(self):
        return(80007798)
    
    def can_get_fastpass(self):
        return(False)


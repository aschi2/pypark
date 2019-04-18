
# coding: utf-8

# In[3]:


import requests
from datetime import datetime
import pandas as pd


# In[242]:


class disney_park:
        

    def __init__(self):
        self.__API_BASE = "https://api.wdpro.disney.go.com/"
        
        self.tokendata = self.__get_tokendata()
        self.token = self.tokendata['access_token']
        self.expirtime = self.tokendata['expires_in']
        self.parkid = self.get_parkid()
        self.resortid = self.get_resortid()
        self.__headers = {
        'Accept-Language' : 'en_US',
        'User-Agent': 'UIEPlayer/2.1 iPhone OS 6.0.1',
        'Accept' : 'application/json;apiversion=1',
        'Authorization' : "BEARER "+str(self.token),
        'X-Conversation-Id' : 'WDPRO-MOBILE.MDX.CLIENT-PROD',
        'X-Correlation-ID' : str(datetime.now().timestamp())
        }
        self.rawwaitdata = self.__get_rawwaitdata()
        self.size = len(self.rawwaitdata['entries'])
        self.waitdata,self.names = self.__get_waitdata()
        self.timeretrieved = self.__get_time()
        self.__entertainment_indeces,self.__reverse_ent_indeces = self.__get_ent_indeces()
        self.waitdata_attractions = self.waitdata.iloc[:,self.__reverse_ent_indeces]
        self.waitdata_entertainement = self.waitdata.iloc[:,self.__entertainment_indeces]
        if self.can_get_fastpass(): 
            self.fastpass,self.__truefastpassindex = self.get_fastpass()
            self.fastpasstrue = self.fastpass.iloc[:,self.__truefastpassindex]
        self.isopen,self.__op_index = self.__get_isopen()
        self.openwaitdata = self.waitdata.iloc[:,self.__op_index]
        self.rawscheduledata = self.__get_rawscheduledata()
        self.todays_hours = self.get_scheduledata()

    
    
    def refresh(self):
        
        self.tokendata = self.__get_tokendata()
        self.token = self.tokendata['access_token']
        self.expirtime = self.tokendata['expires_in']
        self.parkid = self.get_parkid()
        self.resortid = self.get_resortid()
        self.rawwaitdata = self.__get_rawwaitdata()
        self.size = len(self.rawwaitdata['entries'])
        self.waitdata,self.names = self.__get_waitdata()
        self.timeretrieved = self.__get_time()
        self.__entertainment_indeces,self.__reverse_ent_indeces = self.__get_ent_indeces()
        self.waitdata_attractions = self.waitdata.iloc[:,self.__reverse_ent_indeces]
        self.waitdata_entertainement = self.waitdata.iloc[:,self.__entertainment_indeces]
        if self.can_get_fastpass(): 
            self.fastpass,self.__truefastpassindex = self.get_fastpass()
            self.fastpasstrue = self.fastpass.iloc[:,self.__truefastpassindex]
        self.isopen,self.__op_index = self.__get_isopen()
        self.openwaitdata = self.waitdata.iloc[:,self.__op_index]
        
        
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
        
    
        r = requests.get(url = self.__API_BASE+'facility-service/theme-parks/{}/wait-times'.format(self.parkid),headers=self.__headers)
        data = r.json()
        return(data)
    
    def __get_rawscheduledata(self,startDate =datetime.now().strftime('%Y-%m-%d'),endDate = False ):
        if not endDate:
            endDate = startDate
        r = requests.get(url = self.__API_BASE + 'mobile-service/public/ancestor-activities-schedules/{};entityType=destination?filters=theme-park&startDate={}&endDate={}&region=us'.format(self.resortid,startDate,endDate),headers=self.__headers)
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
            names.append(rawdata['entries'][i]['name'].replace('"','') + ' '+ str(i))
            try:
                times.append([rawdata['entries'][i]['waitTime']['postedWaitMinutes']])
            except KeyError:
                times.append([rawdata['entries'][i]['waitTime']['status']])
                

        data = dict(zip(names,times))
        data = pd.DataFrame.from_dict(data)
        data = data[names]
        return(data,names)
    
    def __get_ent_indeces(self):
        types = []
        for i in range(0,len(self.rawwaitdata['entries'])):
            types.append(self.rawwaitdata['entries'][i]['type'])
            
        indeces = [i for i,x in enumerate(types) if x=='Entertainment']
        reverse_indeces= list(set(range(0,self.size)) - set(indeces))
        return((indeces,reverse_indeces))
        
    def get_fastpass(self):
        rawdata = self.rawwaitdata
        times = []
        indeces = []
        for i in range(0,self.size):
            if rawdata['entries'][i]['waitTime']['fastPass']['available']:
                try:
                    indeces.append(i)
                    times.append([rawdata['entries'][i]['waitTime']['fastPass']['startTime']])
                except KeyError:
                    times.append('Not Available')
            else:
                times.append('Not Available')
                

        data = dict(zip(self.names,times))
        data = pd.DataFrame.from_dict(data)
        return((data,indeces))
        
    def can_get_fastpass(self):
        raise(("Method Must Be Defined By Inherited Class"))
        
    def __get_isopen(self):
        rawdata = self.rawwaitdata
        operating_or_not = []
        op_index = []
        for i in range(0,self.size):
            if rawdata['entries'][i]['waitTime']['status'] == 'Operating':
                operating_or_not.append('Operating')
                op_index.append(i)
            else:
                operating_or_not.append('Closed')
        return(operating_or_not,op_index)
    
    def get_scheduledata(self,startDate = False,endDate = False):
        if startDate:
            rawdata = self.__get_rawscheduledata(startDate=startDate,endDate = endDate)
        else:
            rawdata = self.rawscheduledata
        for i in range(0,len(rawdata['activities'])):
            if rawdata['activities'][i]['id'].split(';')[0] == str(self.parkid):
                rightdata = rawdata['activities'][i]['schedule']['schedules']
                
        for j in range(0,len(rightdata)):
            if rightdata[j]['type']=='Operating':
                tempdata = pd.DataFrame(rightdata[j],index=[0])
                try:
                    data = data.append(tempdata)
                except:
                    data = tempdata

                    
        
        return(data.reset_index(drop=True))
                
            
        
         
        



# In[243]:


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
    #Doesn't Have FastPass Return (yet)
    def can_get_fastpass(self):
        return(True)


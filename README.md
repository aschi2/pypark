# pyparks
Theme Parks API from Python (Unofficial)

An Unofficial ThemeParks API for Python.

Based on themeparks by cubehouse and amusement by rambleraptor.

In Early Stages, not yet ready for distribution.

Currently Disneyland Resort (Disneyland and California Adventure) Wait Times and Fast Pass Times are Supported, as well as schedules

## Installation

Just drop the script in your folder and import it as pypark


## Usage

import pypark

DL = pypark.Disneyland()

DL.waitdata  //Outputs wait time at time accessed in the form of a pandas dataframe

DL.openwaitdata //Outputs wait times of rides that are open only

DL.timeretrieved //datetime of time accessed

DL.waitdata_attractions // Wait time of attractions (rides) in the form of a pandas dataframe

DL.waitdata_entertainement // Wait time for shows/meet and greets in the form of a pandas dataframe

DL.rawwaitdata //raw output from disney api (will be deprecated) 

DL.refresh() //refresh information from disney api 

DL.fastpass //Outputs fastpass start times at time accessed in the form of a pandas dataframe

DL.fastpasstrue // Same as .fastpass with rides and attractions without fastpass dropped

Fastpass -1 out -2 doesn't offer

Waittime -1 down -2 closed

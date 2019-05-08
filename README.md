# pyparks
Theme Parks API from Python (Unofficial)

An Unofficial ThemeParks API for Python.

Based on themeparks by cubehouse and amusement by rambleraptor.

In Early Stages, not yet ready for distribution.

Currently Disneyland Resort (Disneyland and California Adventure) Wait Times and Fast Pass Times are Supported


## Installation

    pip install pyparks

## Usage

    import pypark

    DL = pypark.Disneyland()

Creates Disneyland Object, Alternatively use CaliforniaAdventure or MagicKingdom (NOT FULLY TESTED)

    DL.waitdata

Outputs wait time at time accessed in the form of a pandas dataframe

    DL.openwaitdata

Outputs wait times of rides that are open only

    DL.timeretrieved

datetime of time accessed

    DL.waitdata_attractions

Wait time of attractions (rides) in the form of a pandas dataframe

    DL.waitdata_entertainement

Wait time for shows/meet and greets in the form of a pandas dataframe

    DL.rawwaitdata
raw output from disney api (will be deprecated) 

    DL.refresh()
refresh information from disney api 

    DL.fastpass

Outputs fastpass start times at time accessed in the form of a pandas dataframe

    DL.fastpasstrue 

Same as .fastpass with rides and attractions without fastpass dropped


Fastpass -1 out -2 doesn't offer

Waittime -1 down -2 closed



Data is returned as Pandas Dataframes. Information is staight from the Disney API therefore rides returned may be inconsistent depending on if new rides are added or taken away.

# WARNING

This is an unofficial package, not endorced by any of the supported themeparks. Any support could be broken without warning.

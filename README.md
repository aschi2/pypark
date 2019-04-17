# pypark
Theme Parks API from Python (Unofficial)

An Unofficial ThemeParks API for Python.

Based on themeparks by cubehouse and amusement by rambleraptor.

In Early Stages, not yet ready for distribution.

Currently Disneyland Wait Times Supported

import parkpy

DL = parkpy.Disneyland()

DL.waitdata  //Outputs wait time at time accessed
DL.timeretrieved //datetime of time accessed
DL.waitdata_attractions // Wait time of attractions (rides)
DL.waitdata_entertainement // Wait time for shows/meet and greets
DL.rawwaitdata //raw output from disney api (will be deprecated)

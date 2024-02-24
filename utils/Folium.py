import os
import json
import pandas as pd
import random
import folium
import base64
from folium.plugins import MarkerCluster, Search, MeasureControl, LocateControl, MiniMap, FeatureGroupSubGroup, Fullscreen, AntPath, PolyLineOffset, HeatMap, StripePattern, Geocoder


class Folium:
    def __init__(self):
        i = 0
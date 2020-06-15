from GminaClass import GminaClass
import pandas as pd
from sys import getsizeof
import time

initial_state = pd.read_csv("gminas_pops_python2005.csv", dtype={'TERYT':str})

gminas_dict = {}

for idx, row in initial_state.iterrows():
    gminas_dict[row['TERYT']] = GminaClass(teryt_code=row['TERYT'],population=row['POPULACJA'],conservatism_support=row['APPROX_PERCENTAGE'], downscale_factor=38)



from GminaClass import GminaClass
import pandas as pd
from sys import getsizeof
import time

start = time.time()

initial_state = pd.read_csv("gminas_pops_python2005.csv", dtype={'TERYT':str})
travellers = pd.read_csv("tabela_przeplywy2016_python.csv",dtype={'FROM':str, 'TO':str})
print(travellers)
gminas_dict = {}

for idx, row in initial_state.iterrows():
    gminas_dict[row['TERYT']] = GminaClass(teryt_code=row['TERYT'],population=row['POPULACJA'],conservatism_support=row['APPROX_PERCENTAGE'], downscale_factor=38)
    gminas_dict[row['TERYT']].initialize_workplaces(travellers)

end  = time.time()

print(end - start)

import numpy as np
import pandas as pd
df = pd.read_excel("RO_Hole_Diameter_Inspection.xlsx")

for idx in df.index:
    print(df.iloc[idx, 1], type(df.iloc[idx, 1]))

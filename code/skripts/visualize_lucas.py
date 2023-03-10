import mvnx
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# file path

fp = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings\P6\MVNX\medium_round.mvnx')

data = mvnx.load(fp)

com = pd.DataFrame(data.centerOfMass, columns = )
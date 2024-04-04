
import numpy as np
import pandas as pd

macleod = pd.read_csv("population_histories/macleod2013_raw.csv")
history = macleod[::-1].reset_index()
history.loc[:,"generations_ago"] = np.cumsum(history["number_of_generations"])

history["generations_ago"] = history["generations_ago"].shift(1)
history.loc[0, "generations_ago"] = 0

history[["generations_ago", "Ne"]].to_csv("population_histories/macleod2013.txt", sep = "\t", index = False)

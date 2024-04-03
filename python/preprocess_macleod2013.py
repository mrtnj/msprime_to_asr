
import numpy as np
import pandas as pd

macleod = pd.read_csv("population_histories/macleod2013_raw.csv")
history = macleod[::-1].reset_index()
history.loc[:,"generations_ago"] = np.cumsum(history["number_of_generations"]) - 3


history[["generations_ago", "Ne"]].to_csv("population_histories/macleod2013.txt", sep = "\t", index = False)

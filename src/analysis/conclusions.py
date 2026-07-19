import pandas as pd
import numpy as np
from src.processing.all_csv import df_combined


print("=====================================================================================================")
print("================================  Analysis And Final Conclusion =====================================")
print("=====================================================================================================")
filtered_df = df_combined[df_combined["category"] == "Weak"]
table4 = filtered_df.groupby("source").size()
print(table4)
print("JAPAN_EMSC is the only source that includes information about earthquakes with magnitudes below 4.0.")
print("=====================================================================================================")

table5 = df_combined[df_combined["category"] == "Severe"]
print(table5)
print("The only Severe earthquake above magnitude 6 was reported in the JAPAN_EMSC source. The earthquake had a magnitude of 6.0 and is located in row 164 of the df_combined table.\
Since the output of this task contains only a single record, for better analysis we consider a scenario in which we examine the depths at which Average earthquakes typically occur.")
filtered_df = df_combined[df_combined["category"] == "Average"]
table6 = filtered_df['depth'].describe()
print(table6)

print("As can be seen, the distribution of Average earthquake data does not follow a normal distribution. Therefore, the data are not concentrated around the mean, and the median provides a better estimate for our analysis.")
print("=====================================================================================================")

filtered_df = df_combined[df_combined["category"].isin(["Average", "Severe"])]
table7 = filtered_df.sort_values(by="depth", ascending=True).head(10)
print(table7)

print("By displaying the first 10 most dangerous earthquakes, it appears that these events occurred more frequently during September and October (the autumn season) and were concentrated in the OFF EAST COAST OF HONSHU region.")
print("=====================================================================================================")

table8 = df_combined[df_combined["category"].isin(["Average", "Severe"])].groupby(["source", "category"]).size() 
print(table8)
print("Since there is only one Severe earthquake in our data sources, we measure the number of both Severe and Average earthquakes. As shown, Severe and Average earthquakes were reported more frequently by the JAPAN_EMSC source.")
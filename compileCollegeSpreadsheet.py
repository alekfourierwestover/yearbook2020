# @David run this and compile the map again!
import pandas as pd
import json

with open("users.json", "r") as f:
    data = json.load(f)

names = []
institutions = []

for uuid in data:
    names.append(data[uuid]["name"])
    institutions.append(data[uuid]["institution"])

data_frame_dict = {"names": names, "institutions": institutions}
df = pd.DataFrame.from_dict(data_frame_dict)
df.to_csv("colleges.csv")


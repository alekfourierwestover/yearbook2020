# @David run this and compile the map again!
import pandas as pd
import json

with open("users.json", "r") as f:
    data = json.load(f)

names = []
institutions = []

for uuid in data:
    if data[uuid]["verified"] and data[uuid]["senior"]:
        if data[uuid]["institution"] in institutions:
            names[institutions.index(data[uuid]["institution"])] += ", " +data[uuid]["name"]

        else:
            names.append(data[uuid]["name"])
            institutions.append(data[uuid]["institution"])

for i in range(len(names)):
    temp=names[i].split(", ")
    temp.sort(key=lambda x: x.split(" ")[1].lower())
    names[i]= ", ".join(temp)

data_frame_dict = {"names": names, "institutions": institutions}
df = pd.DataFrame.from_dict(data_frame_dict)
df.to_csv("colleges.csv", "\t", columns=["institutions", "names"])

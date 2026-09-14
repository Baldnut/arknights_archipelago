import yaml
from icecream import ic

with open("stories.yaml", "r") as f:
    data = yaml.full_load(f)

ic(data)

locations = []

for story in data:
    for part in data[story]:
        region = f"{story} {part}"
        for stage in data[story][part]:
            location = {}

            location["name"] = f"{stage["id"]} Clear"

            location["category"] = [story, part]
            location["region"] = region

            if "boss" in stage.keys() and stage["boss"] == True:
                location["victory"] = True

            locations.append(location)

ic(locations)
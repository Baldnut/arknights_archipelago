import yaml, json
from pathlib import Path
from icecream import ic

with open("stories.yaml", "r") as f:
    data = yaml.full_load(f)

base = Path(__file__).resolve().parent
locations_path = base / "src" / "data" / "locations.json"
categories_path = base / "src" / "data" / "categories.json"
items_path = base / "src" / "data" / "items.json"
regions_path = base / "src" / "data" / "regions.json"

with locations_path.open("r", encoding="utf-8") as f:
    locationdata = json.load(f)

with categories_path.open("r", encoding="utf-8") as f:
    categories = json.load(f)

with items_path.open("r", encoding="utf-8") as f:
    itemdata = json.load(f)

with regions_path.open("r", encoding="utf-8") as f:
    regions = json.load(f)

locations = [loc for loc in locationdata["data"] if "Stage" not in loc["category"]]

items = [item for item in itemdata["data"] if "category" not in item.keys() or "Stages" not in item["category"]]

for act in data:
    categories[act] = {"hidden": True}
    for story in data[act]:
        prevRegion = None
        for part in data[act][story]:
            categories[part] = {"hidden": True}

            region = f"{story} {part}"
            regions[region] = {}

            items.append({
                "name": region,
                "caregory": ["Stages", act, story],
                "progression": True
            })

            if prevRegion == None:
                regions[region]["starting"] = True
                regions[region]["requires"] = f"|{region}|"
            else:
                regions[prevRegion]["connects_to"] = [region]
                regions[prevRegion]["exit_requires"] = {region: f"|{region}|"}

            prevRegion = region
            for stage in data[act][story][part]:
                location = {}

                location["name"] = f"{stage["id"]} Clear"

                location["category"] = ["Stage", act, story, part]
                location["region"] = region

                if "air" in stage.keys():
                    if type(stage["air"]) != int:
                        print(f"value 'air' of {stage["id"]} is not an integer")
                    location["requires"] = f"|@Ranged:{stage["air"]}|"
                    
                if stage["id"].startswith("TR"):
                    location["category"].append("Training")

                locations.append(location)

                stars = location.copy()
                stars["name"] = f"{stage["id"]} 3-Star"

                if "boss" in stage.keys() and stage["boss"] == True:
                    stars["victory"] = True

                locations.append(stars)

locationdata["data"] = locations

with locations_path.open("w", encoding="utf-8") as f:
    json.dump(locationdata, f, ensure_ascii=False, indent=4)

with categories_path.open("w", encoding="utf-8") as f:
    json.dump(categories, f, ensure_ascii=False, indent=4)

itemdata["data"] = items

with items_path.open("w", encoding="utf-8") as f:
    json.dump(itemdata, f, ensure_ascii=False, indent=4)

with regions_path.open("w", encoding="utf-8") as f:
    json.dump(regions, f, ensure_ascii=False, indent=4)
import json, sys
from pathlib import Path
from icecream import ic

class_names = {"WARRIOR": "Guard",
               "MEDIC": "Medic",
               "SPECIAL": "Specialist",
               "SNIPER": "Sniper",
               "SUPPORT": "Supporter",
               "TANK": "Defender",
               "PIONEER": "Vanguard",
               "CASTER": "Caster"}

char_table_path = Path(sys.argv[1])

with char_table_path.open("r", encoding="utf-8") as f:
    chars = json.load(f)

base = Path(__file__).resolve().parent
items_path = base / "src" / "data" / "items.json"

with items_path.open("r", encoding="utf-8") as f:
    itemdata = json.load(f)

items = [item for item in itemdata["data"] if "category" not in item.keys() or "Operators" not in item["category"]]

for id in chars.keys():
    if chars[id]["itemObtainApproach"] == None:
        continue

    char = {}
    char["name"] = "Unlock " + chars[id]["name"]
    char["category"] = ["Operators",
                        chars[id]["name"],
                        f"{chars[id]["rarity"][5]} Star",
                        class_names[chars[id]["profession"]],
                        chars[id]["position"].capitalize()]
    char["progression"] = True

    items.append(char)

itemdata["data"] = items

with items_path.open("w", encoding="utf-8") as f:
    json.dump(itemdata, f, ensure_ascii=False, indent=4)

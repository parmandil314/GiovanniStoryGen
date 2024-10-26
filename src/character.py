# Trait acronym mappings:
#    LIT: Love Is Transactional
#    LYP: Loves Younger People
#    LINT: Love Is Not Transactional
#    WGR: Wants a Good Relationship
#    CD: Cares about Dignity
#    NAI: Not Afraid of their Identity
#    WNTL: Wants Non-Transactional Love
#    RAP: Runs Away from Problems
#    WPC: Wants to Prove Conventionality
# Relationship acronym mappings:
#    OL: Official Lover
#    PL: Private Lover
#    Relationship acronym mappings:
#    SAP: Sexually Abusive (Perpetrator)
#    SAV: Sexually Abusive (Victim)
#    A: Associate (friendly, but not friends exactly)

import json
import os

def load_directory(path):
    files = os.listdir(path)
    characters = []
    for i in files:
        if i[:-5] == ".json":
            characters.append(load_json_character(path + i))
    return characters

def load_json_character(filename):
    with open(filename, "r") as file:
        json_string = file.read()
        file.close()
    json_contents = json.loads(json_string)
    name = json_contents["Name"]
    location = json_contents["Location"]
    goal = json_contents["Goal"]
    self_hatred = json_contents["Self-Hatred"]
    traits = json_contents["Traits"]
    relationships = json_contents["Relationships"]
    return Character(name, location, goal, self_hatred, traits, relationships)

class Character:
    def __init__(self, name, location, goal, self_hatred, traits, relationships):
        self.name = name
        self.location = location
        self.goal = goal
        self.hatred = self_hatred
        self.traits = traits
        self.relations = relationships

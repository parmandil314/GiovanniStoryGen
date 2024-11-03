import pickle

# Traits:
#    LIT: Love Is Transactional
#    LINT: Love Is Not Transactional
#    Straight
# Relationship acronym mappings:
#    EPL: Ex-Private Lover
#    EOL: Ex-Official Lover
#    OL: Official Lover
#    PL: Private Lover
#    SAP: Sexually Abusive (Perpetrator)
#    SAV: Sexually Abusive (Victim)

import json
import os

VALID_TRAITS = ("LIT", "LYP", "LINT", "WGR", "CD", "NAI", "WNTL", "RAP", "WPC")
VALID_RELATIONS = ("OL", "PL", "SAP", "SAV", "A", "EOL", "EPL", "ESAP", "ESAV")

def load_directory(path):
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        print("Invalid directory path specified.")
        return []
    characters = []
    for i in files:
        if not path[-1] == "/":
            characters.append(load_json_character(path + "/" + i))
        else:
            characters.append(load_json_character(path + i))
    return characters


def load_json_character(filename):
    try:
        with open(filename, "r") as file:
            json_string = file.read()
            file.close()
    except FileNotFoundError:
        return None
    json_contents = json.loads(json_string)
    name = json_contents["Name"]
    location = json_contents["Location"]
    goal = json_contents["Goal"]
    self_hatred = json_contents["Self-Hatred"]
    traits = json_contents["Traits"]
    relationships = json_contents["Relationships"]
    is_alive = json_contents["Alive"]
    is_available = json_contents["Available"]
    return Character(name, location, goal, self_hatred, traits, relationships, is_alive, is_available)


class Character:
    def __init__(self, name, location, goal, self_hatred, traits, relationships, is_alive, is_available):
        self.name = name
        self.location = location
        self.goal = goal
        self.hatred = self_hatred
        self.traits = traits
        self.relations = relationships
        self.alive = is_alive
        self.available = is_available


def run_repl():
    print("Welcome to the Giovanni's Room Story Generator!")
    print("For a complete program specification, ")
    print("view README.md in the project root directory.")
    print("To learn how to navigate this interface, input 'help'")
    print("or look at the README.")
    story = None
    inp = ""
    while not inp == "quit":
        inp = input(">>> ")
        command = inp.split()
        match command[0]:
            case "help":
                print("load-chars <folder> : loads all of the characters in a folder, replacing any previous characters.")
                print("save <filepath> : opens or creates the file at <filepath> and saves the current session to it.")
                print("load <filepath> : loads a session saved with the 'save' command.")
                print("quit : exits the session, losing any unsaved data")
                print("round : runs a round of story simulation")
                print("rounds <number> : equivalent to running 'round' a number of times equal to <number>.")
            case "quit":
                final = input("This command will exit the program.\nUnsaved data will be lost!\nAre you sure you want to do this? (y/n): ")
                if final.lower() == "y":
                    print("Exiting the REPL")
                else:
                    inp = ""
            case "save":
                with open(command[1], "wb") as file:
                    pickle.dump(story, file)
                    file.close()
            case "load":
                with open(command[1], "rb") as file:
                    story = pickle.load(file)
                    file.close()
            case "load-chars":
                try:
                    story = Story(load_directory(command[1]))
                except IndexError:
                    print("Invalid command syntax.")
            case "round":
                try:
                    story.tick()
                except AttributeError:
                    print("No characters have been loaded.")
            case "rounds":
                try:
                    for _ in range(int(command[1])):
                        story.tick()
                except IndexError:
                    print("No characters have been loaded.")
            case "inspect":
                story.print_char(command[1])
            case _:
                print("Invalid command.")

def check(lis):
    return all(i == lis[0] for i in lis)

class Story:
    def print_char(self, name):
        character = self.find_char(name)
        print(f"Name: {character.name}")
        print(f"Location: {character.location[-1]}")
        if not character.goal == "" and not character.goal == "None":
            print(f"Goal: {character.goal}")
        else:
            print("Goal: None")
        print(f"Alive: {character.alive}")
        print(f"Available: {character.available}")
        print(f"Self-Hatred: {character.hatred}/10")
        print("Traits:")
        for i in character.traits:
            print(f"\t{i}")
        print("Relationships:")
        for i in character.relations.keys():
            print(f"\tName: {i}")
            print(f"\t\tHas met: {character.relations[i]["met"]}")
            print(f"\t\tRelationship Type: {character.relations[i]["relationship"][-1]}")
            print(f"\t\tExternal Romantic Love: {character.relations[i]["romantic love"][0]}/10")
            print(f"\t\tInternal Romantic Love: {character.relations[i]["romantic love"][1]}/10")
            print(f"\t\tExternal Sexual Interest: {character.relations[i]["sexual interest"][0]}/10")
            print(f"\t\tInternal Sexual Interest: {character.relations[i]["sexual interest"][1]}/10")
            print(f"\t\tExternal Platonic Love: {character.relations[i]["platonic love"][0]}/10")
            print(f"\t\tInternal Platonic Love: {character.relations[i]["platonic love"][1]}/10")

    def set_names(self):
        self.names = []
        for character in self.characters:
            self.names.append(character.name)

    def find_char(self, name):
        for character in self.characters:
            if character.name == name:
                return character
        return None

    def modify_relation(self, name, relation_name, relation_type=None, rl=(0,0), si=(0,0), pl=(0,0)):
        character = self.find_char(name)
        if character.alive and character.available:
            character.relations[relation_name]["romantic love"][0] += rl[0]
            character.relations[relation_name]["romantic love"][1] += rl[1]

            character.relations[relation_name]["sexual interest"][0] += si[0]
            character.relations[relation_name]["sexual interest"][1] += si[1]

            character.relations[relation_name]["platonic love"][0] += pl[0]
            character.relations[relation_name]["platonic love"][1] += pl[1]

            if not relation_type is None and relation_type in VALID_RELATIONS:
                character.relations[relation_name]["relationship"].append(relation_type)

            print(f" | {name}'s love for {relation_name} has been modified:")
            if not relation_type is None and relation_type in VALID_RELATIONS:
                print(f" |  relationship type: {relation_type}")
            else:
                print(f" |  relationship type: {character.relations[relation_name]["relationship"][-1]} (no change)")
            print(f" | \tromantic love: {character.relations[relation_name]["romantic love"]}", end="")
            if rl[0] > 0:
                print(" (external increase)", end="")
            elif rl[0] == 0:
                print(" (no external change)", end="")
            else:
                print(" (external decrease)", end="")

            if rl[1] > 0:
                print(" (internal increase)")
            elif rl[1] == 0:
                print(" (no internal change)")
            else:
                print(" (internal decrease)")

            print(f" | \tsexual interest: {character.relations[relation_name]["sexual interest"]}", end="")
            if si[0] > 0:
                print(" (external increase)", end="")
            elif si[0] == 0:
                print(" (no external change)", end="")
            else:
                print(" (external decrease)", end="")

            if si[1] > 0:
                print(" (internal increase)")
            elif si[1] == 0:
                print(" (no internal change)")
            else:
                print(" (internal decrease)")

            print(f" | \tplatonic love: {character.relations[relation_name]["platonic love"]}", end="")
            if pl[0] > 0:
                print(" (external increase)", end="")
            elif pl[0] == 0:
                print(" (no external change)", end="")
            else:
                print(" (external decrease)", end="")

            if pl[1] > 0:
                print(" (internal increase)")
            elif pl[1] == 0:
                print(" (no internal change)")
            else:
                print(" (internal decrease)")

    def set_relation(self, name, relation_name, relation_type=None, rl=(0,0), si=(0,0), pl=(0,0)):
        character = self.find_char(name)
        if character.alive and character.available:
            character.relations[relation_name]["romantic love"] = list(rl)
            character.relations[relation_name]["sexual interest"] = list(si)
            character.relations[relation_name]["platonic love"] = list(pl)

            if not relation_type is None and relation_type in VALID_RELATIONS:
                character.relations[relation_name]["relationship"][-1] = relation_type

            print(f" | {name}'s love for {relation_name} has been modified:")

            if not relation_type is None and relation_type in VALID_RELATIONS:
                print(f" | relationship type: {relation_type}")
            else:
                print(f" | relationship type: {character.relations[relation_name]["relationship"][-1]} (no change)")

            print(f" | \tromantic love: {character.relations[relation_name]["romantic love"]}")
            print(f" | \tsexual interest: {character.relations[relation_name]["sexual interest"]}")
            print(f" | \tplatonic love: {character.relations[relation_name]["platonic love"]}")

    def in_rel(self, names, rel):
        char_1 = self.find_char(names[0])
        char_2 = self.find_char(names[1])
        try:
            if char_1.relations[char_2.name]["relationship"][-1] == rel and char_2.relations[char_1.name]["relationship"][-1] == rel:
                return True
        except KeyError:
            pass
        return False

    def in_ol(self, name):
        character = self.find_char(name)
        if character.alive and character.available:
            for i in character.relations.keys():
                if character.relations[i]["relationship"][-1] == "OL":
                    return True
        return False

    def find_ol(self, name):
        character = self.find_char(name)
        if character.alive and character.available:
            for i in character.relations.keys():
                if character.relations[i]["relationship"][-1] == "OL":
                    return i
        return None

    def have_all_met(self):
        all_met = True
        for i in self.characters:
            if i.alive and i.available:
                for j in self.characters:
                    if j == i:
                        continue
                    try:
                        not_met = i.relations[j.name]["met"] is False
                    except KeyError:
                        not_met = False
                    if not_met and i.location[-1] == j.location[-1]:
                        all_met = False
        return all_met

    def tell_about_competition(self):
        return_val = "learn_comp"
        should_return = False
        has_triggered = []
        for i in self.characters:
            if i.alive and i.available:
                for j in self.characters:
                    if i == j or has_triggered == [i.name, j.name]:
                        continue
                    if self.in_ol(i.name) and self.in_rel((i.name, j.name), "PL") and self.prev_action[:5] == "sleep":
                        print(f" | {j.name} learns about {i.name}'s lover {self.find_ol(i.name)}!")
                        self.modify_relation(i.name, j.name, rl=(0,-1), si=(0,-1), pl=(0,-1))
                        self.modify_relation(j.name, i.name, rl=(0, -1), si=(0, -1), pl=(0, -1))
                        return_val = return_val + " " + i.name + " " + j.name + " "
                        has_triggered.append([j.name, i.name])
                        should_return = True
        if should_return:
            self.prev_action = return_val
            return return_val
        else:
            return ""

    def prove_conventionality(self):
        return_val = "pc"
        triggered = False
        for i in self.characters:
            if i.goal == "PC" and i.alive and i.available:
                triggered = True
                print(f" | {i.name}'s need to prove their conventionality has reached a peak!")
                print(f" | {i.name} sleeps with someone they have no interest in!")
                i.goal = ""
        if triggered:
            self.prev_action = return_val
            return return_val
        else:
            return ""

    def meet_all(self):
        triggered = False
        have_all_met = self.have_all_met()
        if not have_all_met:
            triggered = True
            return_val = "meet"
            for i in self.characters:
                if i.alive and i.available:
                    for j in self.characters:
                        if j == i:
                            continue
                        i_location = i.location[-1]
                        j_location = j.location[-1]
                        try:
                            if i_location == j_location and i.relations[j.name]["met"] is False and j.relations[i.name]["met"] is False:
                                print(f" | {i.name} and {j.name} meet each other.")
                                i.relations[j.name]["met"] = True
                                j.relations[i.name]["met"] = True
                                return_val = return_val + " " + i.name + " " + j.name
                        except KeyError:
                            pass
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def sleep(self):
        prev = self.prev_action.split()
        return_val = "sleep "
        has_happened = False

        met = []
        if prev[0] == "meet":
            prev = prev[1:]
            while len(prev) > 0:
                met.append([prev.pop(0), prev.pop(0)])

        for i in met:
            if self.find_char(i[0]).alive and self.find_char(i[0]).available and self.find_char(i[1]).alive and self.find_char(i[1]).available:
                if self.in_rel(i, "PL"):
                    has_happened = True
                    print(f" | {i[0]} and {i[1]} sleep with each other.")
                    return_val = return_val + i[0] + " " + i[1] + " "
                    if "LINT" in self.find_char(i[0]).traits:
                        self.modify_relation(i[0], i[1], rl=(0, 1), si=(0, 1), pl=(2, 1))
                    else:
                        self.modify_relation(i[0], i[1], rl=(0,-1), si=(0,-1), pl=(0,-1))

                    if "LINT" in self.find_char(i[1]).traits:
                        self.modify_relation(i[1], i[0], rl=(0, 1), si=(0, 1), pl=(2, 1))
                    else:
                        self.modify_relation(i[1], i[0], rl=(0,-1), si=(0,-1), pl=(0,-1))

        if has_happened:
            self.prev_action = return_val
            return return_val
        return ""

    def met_x_turns_ago(self, names, turns):
        log_then = self.log[-turns]
        met_action = log_then[:4] == "meet"
        did_meet = False
        who_met = log_then.split()[1:]
        met = []
        while len(who_met) > 1:
            met.append((who_met.pop(0), who_met.pop(0)))
        for i in met:
            if names == i:
                did_meet = True
        if met_action and did_meet:
            return True
        else:
            return False

    def change_self_hatred(self, name, hatred):
        if self.find_char(name).alive and self.find_char(name).available:
            self.find_char(name).hatred += hatred
            if hatred > 0:
                print(f" | {name}'s self-hatred has increased to {self.find_char(name).hatred}!")
            elif hatred < 0:
                print(f" | {name}'s self-hatred has decreased to {self.find_char(name).hatred}!")

    def make_or_break(self):
        return_val = "m_or_b"
        triggered = False
        for i in self.characters:
            if i.alive and i.available:
                for j in self.characters:
                    if i == j:
                        continue
                    if self.in_rel((i.name, j.name), "PL") and self.met_x_turns_ago((i.name, j.name), 3):
                        triggered = True
                        print(f" | {i.name} and {j.name} encounter a 'cherry-pit throwing' moment!")
                        print(" | This is a seemingly insignificant moment that fundamentally affects their relationship.")
                        print(" | Their relationship will be dramatically strengthened or weakened by this event!")
                        if i.hatred >= 5:
                            self.change_self_hatred(i.name, 1)
                            self.modify_relation(i.name, j.name, rl=(-1,-1), si=(-1,-1), pl=(-1,-1))
                        else:
                            self.modify_relation(i.name, j.name, rl=(1,1), si=(1,1), pl=(1,1))

                        if j.hatred >= 5:
                            j.hatred += 1
                            self.change_self_hatred(j.name, 1)
                            self.modify_relation(j.name, i.name, rl=(-1,-1), si=(-1,-1), pl=(-1,-1))
                        else:
                            self.modify_relation(j.name, i.name, rl=(1,1), si=(1,1), pl=(1,1))
                        return_val = return_val + " " + i.name + " " + j.name
        if triggered:
            self.prev_action = return_val
            return return_val
        else:
            return ""

    def letters(self):
        return_val = "letters"
        triggered = False
        for i in self.characters:
            if i.alive and i.available:
                for j in self.characters:
                    if i == j:
                        continue
                    if self.in_rel((i.name, j.name), "PL") and self.met_x_turns_ago((i.name, j.name), 4):
                        triggered = True
                        if i.hatred > j.hatred:
                            return_val = return_val + " " + i.name
                            print(f" | {i.name} received a letter from their official lover {self.find_ol(i.name)}!")
                            if not "Straight" in i.traits:
                                print(f" | {i.name} wants desperately to prove their conventionality!")
                                i.goal = "PC" # Prove Conventionality
                            else:
                                self.change_self_hatred(i.name, 1)
                        elif j.hatred > i.hatred:
                            return_val = return_val + " " + j.name
                            print(f" | {j.name} received a letter from their official lover {self.find_ol(j.name)}!")
                            if not "Straight" in j.traits:
                                print(f" | {i.name} wants desperately to prove their conventionality!")
                                j.goal = "PC" # Prove Conventionality
                            else:
                                self.change_self_hatred(j.name, 1)
                        else:
                            return_val = return_val + " " + i.name + " " + j.nme
                            print(f" | {i.name} received a letter from their official lover {self.find_ol(i.name)}!")
                            if not "Straight" in i.traits:
                                print(f" | {i.name} wants desperately to prove their conventionality!")
                                i.goal = "PC"  # Prove Conventionality
                            else:
                                self.change_self_hatred(i.name, 1)

                            print(f" | {j.name} received a letter from their official lover {self.find_ol(j.name)}!")
                            if not "Straight" in j.traits:
                                print(f" | {i.name} wants desperately to prove their conventionality!")
                                j.goal = "PC"  # Prove Conventionality
                            else:
                                self.change_self_hatred(j.name, 1)
        if triggered:
            self.prev_action = return_val
            return return_val
        else:
            return ""
    
    def has_been_in_rel_x_turns(self, names, relation, rounds=0):
        char1 = self.find_char(names[0])
        char2 = self.find_char(names[1])
        if char1.alive and char1.available and char2.alive and char2.available:
            try:
                check(char1.relations[char2.name]["relationship"][-rounds:])
                if char1.relations[char2.name]["relationship"][-1] == relation:
                    return True
            except KeyError:
                return False
        return False

    def fire_esav(self):
        triggered = False
        return_val = "fire_esav"
        for i in self.characters:
            if i.alive and i.available:
                for j in self.characters:
                    if i == j:
                        continue
                    if self.has_been_in_rel_x_turns((i.name, j.name), "ESAV", 6) and not self.log[-1][:9] == "fire_esav":
                        triggered = True
                        return_val = return_val + " " + i.name + " " + j.name
                        print(f" | {j.name} dramatically fires {i.name} from their business!")
                        self.change_self_hatred(i.name, 2)
                        self.modify_relation(j.name, i.name, "SAP", (-1,-1), (-1,-1), (-1,-1))
                        self.modify_relation(i.name, j.name, "SAV", (-1, -1), (-1, -1), (-1, -1))
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def in_pl(self, name):
        if self.find_char(name).alive and self.find_char(name).available:
            for i in self.find_char(name).relations:
                if self.find_char(name).relations[i]["relationship"][-1] == "PL":
                    return True
        return False

    def update_locs(self):
        triggered = False
        return_val = "update_locs"
        for i in self.characters:
            if i.alive and i.available:
                prev_7_locs = i.location[-7:]
                same = check(prev_7_locs)
                if self.in_ol(i.name):
                    if same and not self.in_pl(i.name) and not self.find_char(self.find_ol(i.name)).location[-1] == i.location[-1]:
                        new_location = self.find_char(self.find_ol(i.name)).location[-1]
                        print(f" | {i.name} is moving to {new_location}.")
                        triggered = True
                        return_val = return_val + " " + i.name + " " + new_location
                        self.change_loc(i.name, new_location)
                        if self.in_pl(self.find_ol(i.name)):
                            self.change_self_hatred(self.find_ol(i.name), 1)
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def change_loc(self, name, location):
        print(f" | {name} has changed location to {location}.")
        if self.find_char(name).alive and self.find_char(name).available:
            self.find_char(name).location.append(location)

    def find_pls(self, name):
        names = []
        for i in self.find_char(name).relations:
            if self.find_char(name).relations[i]["relationship"][-1] == "PL":
                names.append(self.find_char(name).relations[i]["name"])
        return names

    def has_met(self, name1, name2):
        if self.find_char(name1).relations[name2]["met"] and self.find_char(name1).alive and self.find_char(name2).alive:
            return True
        return False

    def met_last_turn(self, name1, name2):
        last_log = self.log[-1].split()
        if last_log[0] == "meet":
            last_log.pop(0)
            while len(last_log) > 0:
                if name1 in last_log[0:2] and name2 in last_log[0:2]:
                    return True
                last_log.pop(0)
                last_log.pop(0)
        else:
            return False

    def ol_pl_met_stress(self):
        triggered = False
        return_val = "ol_pl_meet"
        for i in self.characters:
            if i.alive and i.available:
                pls = self.find_pls(i.name)
                ol = self.find_ol(i.name)
                for pl in pls:
                    if not ol is None:
                        if (self.has_met(ol, pl) or self.has_met(pl, ol)) and i.hatred < 10:
                            triggered = True
                            return_val = return_val + " " + ol + " " + pl
                            print(f" | Since {ol} has encountered {pl}, {i.name}'s stress and inner turmoil has been growing.")
                            self.change_self_hatred(i.name, 1)
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def break_up(self, name1, name2):
        char1 = self.find_char(name1)
        char2 = self.find_char(name2)
        if char1.alive and char1.available and char2.alive and char2.available:
            if char1.relations[char2.name]["relationship"][-1] == "OL":
                self.modify_relation(char1.name, char2.name, "EOL", rl=(-5, -5), si=(-5, -5), pl=(-5, -5))
            elif char1.relations[char2.name]["relationship"][-1] == "PL":
                self.modify_relation(char1.name, char2.name, "EPL", rl=(-5, -5), si=(-5, -5), pl=(-5, -5))

            if char2.relations[char1.name]["relationship"][-1] == "OL":
                self.modify_relation(char2.name, char1.name, "EOL", rl=(-5, -5), si=(-5, -5), pl=(-5, -5))
            elif char2.relations[char1.name]["relationship"][-1] == "PL":
                self.modify_relation(char2.name, char1.name, "EPL", rl=(-5, -5), si=(-5, -5), pl=(-5, -5))

    def pl_break_up_test(self):
        triggered = False
        return_val = "break_up"
        for i in self.characters:
            if i.hatred >= 10 and len(self.find_pls(i.name)) > 0 and i.alive and i.available:
                triggered = True
                for j in self.find_pls(i.name):
                    print(f" | {i.name} dramatically breaks up with {j}!")
                    self.break_up(i.name, j)
                    return_val = return_val + " " + i.name + " " + j
                self.change_self_hatred(i.name, -2)
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def ol_break_up_test(self):
        triggered = False
        return_val = "break_up"
        for i in self.characters:
            if self.in_ol(i.name) and i.alive and i.available:
                if i.relations[self.find_ol(i.name)]["sexual interest"][1] < 7:
                    triggered = True
                    print(f" | {i.name} has an affair and is caught by {self.find_ol(i.name)}!")
                    self.break_up(i.name, self.find_ol(i.name))
                    self.change_self_hatred(i.name, 2)
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def is_in_sav(self, name):
        character = self.find_char(name)
        for i in character.relations.keys():
            if character.relations[i]["relationship"][-1] == "SAV" and self.find_char(i).alive:
                return True
        return False

    def find_sav(self, name):
        character = self.find_char(name)
        for i in character.relations.keys():
            if character.relations[i]["relationship"][-1] == "SAV":
                return i
        return ""

    def were_ever_pls(self, names):
        char1 = self.find_char(names[0])
        char2 = self.find_char(names[1])
        if "PL" in char1.relations[char2.name]["relationship"] and "PL" in char2.relations[char1.name]["relationship"]:
            return True
        return False

    def die(self, name):
        character = self.find_char(name)
        for i in character.relations.keys():
            if self.find_char(i).alive and self.find_char(i).available and self.were_ever_pls((i, character.name)):
                self.change_self_hatred(i, 2)
        character.alive = False
        print(f" | {name} dies!")

    def murder(self, name, char_to_murder):
        print(f" | {name} murders their sexual abuser {char_to_murder}!")
        self.die(char_to_murder)
        if not "Straight" in self.find_char(name).traits:
            print(f" | As a result, {name} is apprehended, put on trial, and sentenced to death!")
            self.change_loc(name, "Death Row")
            self.remove_char(name)
        else:
            print(f" | Someone else is unjustly sentenced for the murder, and {name} is safe from any consequences.")
            self.change_self_hatred(name, 3)

    def suicides(self):
        triggered = False
        return_val = "suicide"
        for i in self.characters:
            if i.hatred > 10 and i.alive and i.available:
                triggered = True
                print(f" | {i.name} cannot bear the misery caused by their own self-hatred!")
                print(f" | {i.name} commits suicide!")
                self.die(i.name)
                return_val = return_val + " " + i.name
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def remove_char(self, name):
        character = self.find_char(name)
        character.available = False

    def drastic_event(self):
        triggered = False
        return_val = "drastic_event"
        last_event = self.log[-1].split()
        for i in self.characters:
            if i.alive and i.available:
                try:
                    if last_event[0] == "break_up" and last_event[2] == i.name:
                        triggered = True
                        if self.is_in_sav(i.name):
                            char_to_murder = self.find_sav(i.name)
                            return_val = return_val + " " + "murder" + " " + i.name + " " + char_to_murder
                            print(f" | The losses of dignity caused by {i.name}'s breakup with {last_event[1]}")
                            print(f" | and sexual abuse by {char_to_murder}, push {i.name} over the edge!")
                            self.murder(i.name, char_to_murder)
                            for j in self.find_pls(i.name):
                                self.change_self_hatred(j, 2)
                except IndexError:
                    pass
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def execute(self, name):
        print(f" | {name} is executed after spending time on death row!")
        self.die(name)

    def executions(self):
        triggered = False
        return_val = "execute"
        for i in self.characters:
            if i.alive and not i.available and i.location[-1] == "Death Row" and not self.prev_action[:7] == "drastic":
                triggered = True
                self.execute(i.name)
                return_val = return_val + " " + i.name
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def update_rels(self):
        for i in self.characters:
            for j in i.relations.keys():
                i.relations[j]["relationship"].append(i.relations[j]["relationship"][-1])

    def __init__(self, characters):
        self.log = []
        self.prev_action = ""
        self.characters = characters
        self.names = None
        self.set_names()
        self.current_round = 0

    def tick(self):
        self.current_round += 1
        print("Round", self.current_round)
        self.update_rels()
        if not self.meet_all() == "":
            self.log.append(self.prev_action)
            return
        if not self.sleep() == "":
            self.log.append(self.prev_action)
            return
        if not self.tell_about_competition() == "":
            self.log.append(self.prev_action)
            return
        if not self.make_or_break() == "":
            self.log.append(self.prev_action)
            return
        if not self.letters() == "":
            self.log.append(self.prev_action)
            return
        if not self.prove_conventionality() == "":
            self.log.append(self.prev_action)
            return
        if not self.fire_esav() == "":
            self.log.append(self.prev_action)
            return
        if not self.update_locs() == "":
            self.log.append(self.prev_action)
            return
        if not self.ol_pl_met_stress() == "":
            self.log.append(self.prev_action)
            return
        if not self.pl_break_up_test() == "":
            self.log.append(self.prev_action)
            return
        if not self.drastic_event() == "":
            self.log.append(self.prev_action)
            return
        if not self.ol_break_up_test() == "":
            self.log.append(self.prev_action)
            return
        if not self.executions() == "":
            self.log.append(self.prev_action)
            return
        if not self.suicides() == "":
            self.log.append(self.prev_action)
            return
        print(" | Nothing significant happens this round.")
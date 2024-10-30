import pickle

import character as char

def run_repl():
    print("Welcome to the Giovanni's Room Story Generator!")
    print("For a detailed description of character creation,")
    print("as well as a complete program specification, ")
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
                    exit(0)
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
                    story = Story(char.load_directory(command[1]))
                except IndexError:
                    print("Invalid command syntax.")
            case "round":
                story.tick()
            case "rounds":
                for _ in range(int(command[1])):
                    story.tick()
            case _:
                print("Invalid command.")

def check(lis):
    return all(i == lis[0] for i in lis)

class Story:
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
        character.relations[relation_name]["romantic love"][0] += rl[0]
        character.relations[relation_name]["romantic love"][1] += rl[1]

        character.relations[relation_name]["sexual interest"][0] += si[0]
        character.relations[relation_name]["sexual interest"][1] += si[1]

        character.relations[relation_name]["platonic love"][0] += pl[0]
        character.relations[relation_name]["platonic love"][1] += pl[1]

        if not relation_type is None and relation_type in char.VALID_RELATIONS:
            character.relations[relation_name]["relationship"][-1] = relation_type

        print(f" | {name}'s love for {relation_name} has been modified:")
        if not relation_type is None and relation_type in char.VALID_RELATIONS:
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
        character.relations[relation_name]["romantic love"] = list(rl)
        character.relations[relation_name]["sexual interest"] = list(si)
        character.relations[relation_name]["platonic love"] = list(pl)

        if not relation_type is None and relation_type in char.VALID_RELATIONS:
            character.relations[relation_name]["relationship"][-1] = relation_type

        print(f" | {name}'s love for {relation_name} has been modified:")

        if not relation_type is None and relation_type in char.VALID_RELATIONS:
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
        for i in character.relations.keys():
            if character.relations[i]["relationship"][-1] == "OL":
                return True
        return False

    def find_ol(self, name):
        character = self.find_char(name)
        for i in character.relations.keys():
            if character.relations[i]["relationship"][-1] == "OL":
                return i
        return None

    def have_all_met(self):
        is_true = True
        for i in self.characters:
            for j in self.characters:
                if j == i:
                    continue
                try:
                    met = i.relations[j.name]["met"] is False
                except KeyError:
                    met = False
                if met and i.location[-1] == j.location[-1]:
                    is_true = False
        return is_true

    def tell_about_competition(self):
        return_val = "learn_comp"
        should_return = False
        has_triggered = []
        for i in self.characters:
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
            if i.goal == "PC":
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
        have_all_met = self.have_all_met()
        if not have_all_met:
            self.prev_action = "meet"
            for i in self.characters:
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
                            self.prev_action = self.prev_action + " " + i.name + " " + j.name
                    except KeyError:
                        pass
            return self.prev_action
        else:
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
            if self.in_rel(i, "PL"):
                has_happened = True
                print(f" | {i[0]} and {i[1]} sleep with each other.")
                return_val = return_val + i[0] + " " + i[1] + " "
                if "LINT" in self.find_char(i[0]).traits:
                    self.modify_relation(i[0], i[1], (0, 1), (0, 1), (2, 1))
                else:
                    self.modify_relation(i[0], i[1], (0,-1), (0,-1), (0,-1))

                if "LINT" in self.find_char(i[1]).traits:
                    self.modify_relation(i[1], i[0], (0, 1), (0, 1), (2, 1))
                else:
                    self.modify_relation(i[1], i[0], (0,-1), (0,-1), (0,-1))

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
        self.find_char(name).hatred += hatred
        if hatred > 0:
            print(f" | {name}'s self-hatred has been increased to {self.find_char(name).hatred}!")
        elif hatred < 0:
            print(f" | {name}'s self-hatred has been decreased to {self.find_char(name).hatred}!")

    def make_or_break(self):
        return_val = "m_or_b"
        triggered = False
        for i in self.characters:
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

        try:
            for i in char1.relations[char2.name]["relationship"][-rounds:]:
                if not i == relation:
                    return False
        except KeyError:
            return False
        return True

    def fire_esav(self):
        triggered = False
        return_val = "fire_esav"
        for i in self.characters:
            for j in self.characters:
                if i == j:
                    continue
                if self.has_been_in_rel_x_turns((i.name, j.name), "ESAP", 6) and not self.log[-1][:9] == "fire_esav":
                    triggered = True
                    return_val = return_val + " " + i.name + " " + j.name
                    print(f" | {i.name} dramatically fires {j.name} from his business!")
                    self.modify_relation(j.name, i.name, "SAV", (-1,-1), (-1,-1), (-1,-1))
                    self.modify_relation(i.name, j.name, "SAP", (-1, -1), (-1, -1), (-1, -1))
        if triggered:
            self.prev_action = return_val
            return return_val
        return ""

    def in_pl(self, name):
        for i in self.find_char(name).relations:
            if self.find_char(name).relations[i]["relationship"][-1] == "PL":
                return True
        return False

    def update_locs(self):
        triggered = False
        return_val = "update_locs"
        for i in self.characters:
            prev_7_locs = i.location[-7:]
            same = check(prev_7_locs)

            if same is True and self.in_ol(i.name) and not self.in_pl(i.name):
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
        print(f" | {name} has changed their location to {location}.")
        self.find_char(name).location.append(location)

    def find_pls(self, name):
        names = []
        for i in self.find_char(name).relations:
            if self.find_char(name).relations[i]["relationship"][-1] == "PL":
                names.append(self.find_char(name).relations[i]["name"])
        return names

    def has_met(self, name1, name2):
        if self.find_char(name1).relations[name2]["met"]:
            return True

    def ol_pl_meet(self):
        triggered = False
        return_val = "ol_pl_meet"
        for i in self.characters:
            pls = self.find_pls(i.name)
            ol = self.find_ol(i.name)
            for pl in pls:
                if self.has_met(ol, pl) or self.has_met(pl, ol):
                    triggered = True
                    return_val = return_val + " " + ol + " " + pl
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
        print(" | Nothing significant happens this round.")
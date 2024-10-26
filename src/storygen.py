import character as char

def run(characters, rounds):
    story = Story(characters, rounds)
    while story.current_round <= story.max_rounds:
        story.tick()

class Story:
    def __init__(self, characters, max_rounds):
        self.prev_action = ""
        self.characters = characters
        self.current_round = 0
        self.max_rounds = max_rounds

    def tick(self):
        self.current_round += 1
        print("Round", self.current_round)
        have_all_met = True

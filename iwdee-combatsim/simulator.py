class Unit:
    def __init__(self, hp: int, thac0: int, ac: int, apr: float, dam: str):
        self.hp = hp # hit points
        self.thac0 = thac0 # "to hit armor class 0"
        self.ac = ac # armor class
        self.apr = apr # Attacks per round, 5/2 means 5 attacks every two
        self.dam = dam

    def computeDamage(dam: str):
        # Compute the damage a unit does in a swing if it hits 

def combat_round():
    # Fight a round of combat
    return

def combat():
    # Take in two lists of units, and fight to the death
    return

if __name == "__main__":
    # Create the lists of units, and fight to the death many times
    # Obtain statistics on the outcome

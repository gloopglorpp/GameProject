# Function to deal damage to a target
def attack(target, damage):

    # Reduce the target's health by the damage amount
    target["health"] -= damage

    # Prevent health from becoming negative
    target["health"] = max(target["health"], 0)

    # Return information about the attack
    return {

        # How much damage was dealt
        "damage": damage,

        # The target's remaining health
        "target_health": target["health"],

        # True if the target has been defeated, otherwise False
        "target_defeated": target["health"] == 0
    }
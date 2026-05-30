# Import the player dictionary
from player import player

# Import the enemy dictionary
from enemy import enemy

# Import the attack function
from combat import attack

# Display a starting message
print("Game starting...\n")

# Show which enemy has appeared
print(f"A wild {enemy['name']} appears!")

# Continue combat while both characters are alive
while player["health"] > 0 and enemy["health"] > 0:

    # Display current health values
    print(f"\n{player['name']} Health: {player['health']}")
    print(f"{enemy['name']} Health: {enemy['health']}")

    # Wait for the player to press Enter
    input("\nPress Enter to attack...")

    # Player attacks the enemy
    result = attack(enemy, player["damage"])

    # Display the attack result
    print(
        f"\nYou attacked the {enemy['name']} "
        f"for {result['damage']} damage!"
    )

    # Check if the enemy died
    if result["target_defeated"]:

        # Announce victory
        print(f"{enemy['name']} has been defeated!")

        # Award XP to the player
        player["xp"] += enemy["xp_reward"]

        # Show XP gained
        print(f"You gained {enemy['xp_reward']} XP!")

        # Show total XP
        print(f"Your XP: {player['xp']}")

        # Exit the combat loop
        break

    # Enemy attacks the player
    result = attack(player, enemy["damage"])

    # Display the enemy's attack
    print(
        f"The {enemy['name']} attacked you "
        f"for {result['damage']} damage!"
    )

    # Check if the player died
    if result["target_defeated"]:

        # Display game over message
        print("You have been defeated!")

        # Exit the combat loop
        break
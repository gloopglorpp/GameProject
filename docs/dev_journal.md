# Development Journal

## 2026-05-30 — Created Project Structure

Before writing any significant code, I spent some time thinking about what I was actually trying to build. My initial instinct was to jump straight into programming, but I realised that even a simple game needs some direction. I wrote down a rough game concept and created a task list containing the smallest features required to get a playable version working.

One of the first things I noticed is that software projects are different from coding exercises. A coding exercise can live entirely inside a single file, but a project quickly becomes difficult to manage if everything is thrown together. To avoid this, I created a basic folder structure for the project.

The project was divided into separate areas for source code, assets, and documentation. Although the folders were mostly empty at the beginning, creating them helped establish a clear place for future work. Instead of constantly asking where new files should go, there was already a structure in place.

This was also my first introduction to the difference between a script and a project. A script is usually written to perform one task and can often fit comfortably into a single file. A project is larger and tends to consist of many connected pieces that work together. Even though the game is still extremely simple, organising it from the start made it feel more like a real software project than an experiment.

Looking back, this step did not produce anything visible on screen, but it laid the foundation for everything that followed. The project became easier to navigate, easier to expand, and easier to think about. It was the point where the idea stopped being something in my head and started becoming something tangible.

### Current Structure

- `src/` for game code
- `assets/` for images, sounds, and other resources
- `docs/` for planning, notes, and development journals

### Lessons Learned

- A project benefits from planning before coding begins.
- Breaking work into small tasks makes large goals feel manageable.
- Organised folder structures reduce confusion as a project grows.
- A script and a software project are not the same thing.
- Good organisation may not be visible to the player, but it makes development significantly easier.

## 2026-05-30 — First Steps in Python

After setting up the project structure, I wrote my first Python program and successfully ran it from within the project. Although the program only displayed a simple message, it was an important milestone because it confirmed that Python was installed correctly and that I could create, save, and execute code from my own project.

From there, I started learning about variables. Variables act as containers that store information which can be used later in a program. Instead of hardcoding every value directly into the code, variables make it possible to store and update information as the program runs.

I then learned how to collect input from the user. This was the first time the program felt interactive rather than static. Instead of displaying the same output every time, the program could ask a question, wait for a response, and use the answer in later calculations or messages.

Another important concept was data types. I learned that although two values may look similar, Python can treat them very differently. For example, the number `29` and the text `"29"` are not the same thing. One is a number that can be used in calculations, while the other is a string of characters.

This naturally led to learning about type conversion. I discovered that Python can convert values between different data types when instructed to do so. Converting a string such as `"29"` into an integer allows mathematical operations to be performed on it. Understanding this helped explain why some expressions work while others produce errors.

One of the most valuable habits I began developing was predicting what code would do before running it. Rather than treating programming as trial and error, I started reading code and mentally stepping through it line by line. When my prediction matched the result, it confirmed my understanding. When it did not, it revealed something new that I needed to learn.

Although these concepts seem simple on their own, they form the foundation of nearly every program. User input, variables, data types, and type conversion are all ideas that will continue to appear throughout the development of the game.

### Lessons Learned

- Variables allow information to be stored and reused throughout a program.
- User input makes a program interactive rather than static.
- Numbers and text may look similar but are treated as different data types.
- Type conversion allows values to be transformed between compatible data types.
- Predicting code before running it is one of the fastest ways to build understanding.
- Error messages are often useful clues rather than signs of failure.

## 2026-05-30 — Breaking a Program Into Multiple Files

As the project began to grow, I reached a point where keeping everything inside a single file no longer made sense. Up until then, I had mostly thought of a program as one script containing all of the code. While that works for small examples, it quickly becomes difficult to manage once different systems begin interacting with each other.

To make the project more organised, I started separating responsibilities into different files. The player data was moved into `player.py`, enemy data was moved into `enemy.py`, and combat-related functionality was placed inside `combat.py`. The main game file was then responsible for bringing these pieces together.

This introduced me to Python imports. Instead of defining everything in one place, I could create code in one file and use it elsewhere. At first this felt a little strange, but it quickly became clear why larger software projects are built this way. Each file has a specific purpose and can be understood independently of the others.

One of the first bugs I encountered during this process was surprisingly simple. Python reported that it could not find the variables I was trying to import from another file. After checking the code several times, I eventually discovered that the problem was not the code at all—I had forgotten to save the file before running the program. Because the changes only existed in the editor and not on disk, Python was reading an older version of the file.

Although the bug was minor, it taught an important lesson. Not every problem is caused by complicated code. Sometimes the issue comes from the development process itself. Learning to check simple possibilities first can save a lot of time when debugging.

The most important lesson from this stage was understanding why software is divided into modules. Instead of one giant file trying to do everything, different parts of the program can focus on specific responsibilities. This makes code easier to read, easier to maintain, and easier to expand as the project grows.

Looking back, this was one of the first moments where the project began to feel like real software development rather than a collection of Python exercises. The game was no longer just a script—it was becoming a system of connected components working together.

### Lessons Learned

- Large programs become easier to manage when responsibilities are separated into different files.
- Imports allow code to be reused across multiple parts of a project.
- Modules help keep related functionality organised and easier to understand.
- Not all bugs are caused by bad code; some are caused by simple development mistakes.
- Saving files before running a program is an important habit.
- Breaking a project into smaller pieces makes future development much easier.
- Software projects are often built from many connected modules rather than a single script.

## 2026-05-30 — Building the First Combat System

With the project structure in place and the code split across multiple files, I began building the first actual game mechanic: combat. Up until this point, the project was mostly about learning Python and organising code. Combat was the first feature that felt like a game.

To represent the player and enemy, I was introduced to dictionaries. Rather than storing individual variables for every piece of information, a dictionary allows related data to be grouped together. This made it possible to store things such as health, experience points, damage, and names in a single structure.

The player was given properties such as health, experience points, and damage, while the enemy was given health, damage, and an experience reward. Having both the player and enemy represented in a similar way made it easier to create systems that could work with either one.

One of the first progression mechanics added to the project was experience points, or XP. Defeating an enemy would reward the player with XP, creating a simple feedback loop where success led to progression. Although the system was basic, it introduced the idea that actions within the game could permanently change the state of the player.

To handle combat, I created an attack function. Instead of repeatedly writing the same damage calculations in multiple places, the logic was placed inside a reusable function. The function reduced the target's health, prevented it from dropping below zero, and returned information about the result of the attack.

This was my first real exposure to the idea of reusable code. Rather than writing separate code for every attack, the same function could be used whenever one game object damaged another. The player could attack the enemy, and the enemy could attack the player using the same underlying logic.

The next major concept was the combat loop. Instead of attacking once and ending the program, the game repeatedly checked whether the player and enemy were still alive. If both had health remaining, combat continued. If either reached zero health, the loop ended and the appropriate outcome was displayed.

This introduced a new way of thinking about games. Rather than executing a fixed list of instructions from top to bottom, the program could repeatedly evaluate conditions and react to changing game state. Health values changed, XP increased, and the outcome depended on what happened during the loop.

Looking back, this was the first time the project felt like it contained an actual gameplay system. There were now rules, consequences, progression, and state changes. The game was beginning to move beyond simple demonstrations of Python concepts and toward something interactive.

### Lessons Learned

- Dictionaries provide a convenient way to group related data together.
- Player and enemy data can be represented using similar structures.
- XP creates a simple progression system that rewards success.
- Functions help avoid repeating the same code in multiple places.
- Reusable code is easier to maintain and expand.
- Loops allow game systems to continue running until specific conditions are met.
- Game state changes over time and must be tracked by the program.
- Combat systems are built from simple rules interacting with one another.

## 2026-05-30 — Entering Game Development

After building the text-based combat system, I took my first step into graphical game development by installing Pygame. Up until this point, everything had taken place in the terminal using text. While this was useful for learning programming concepts, I wanted to begin creating something visual that more closely resembled a game.

Installing Pygame introduced me to the idea of external libraries. Rather than building every tool from scratch, developers can use libraries created by other programmers to solve common problems. In this case, Pygame provided everything needed to create windows, handle input, draw graphics, and build interactive applications.

The first major milestone was creating a game window. Although it only displayed a blank screen, it represented a significant shift in the project. For the first time, the game existed in its own graphical space rather than inside a terminal window.

I then learned about rendering, which is the process of drawing objects onto the screen. Every visual element in a game must be rendered before it can be seen by the player. Initially, the screen was simply filled with a dark background colour, but even this basic step introduced the idea that games must constantly redraw their visuals.

One of the most important concepts I encountered was the game loop. Unlike a traditional script that runs from top to bottom and then exits, a game must continuously run while the player is interacting with it. The game loop repeatedly checks for input, updates the game world, and redraws the screen.

At first, the game loop seemed almost invisible because very little was happening inside it. However, I quickly realised that this loop forms the foundation of nearly every game. Everything that happens during gameplay eventually becomes part of this repeating cycle.

The process of creating a window, rendering graphics, and maintaining a game loop changed the way I thought about programming. Instead of writing a sequence of instructions that execute once, I was now creating a system that continuously updates itself many times every second.

Looking back, the graphical output was extremely simple, but it marked a major turning point in the project. This was the moment where the project began to feel less like a collection of Python exercises and more like the beginnings of an actual game.

### Lessons Learned

- Pygame provides tools for creating graphical applications and games.
- External libraries can significantly accelerate development.
- A game window is the foundation for all graphical output.
- Rendering is the process of drawing objects onto the screen.
- Games constantly redraw their visuals rather than drawing them once.
- The game loop is one of the most important concepts in game development.
- Most games repeatedly perform three tasks: process input, update the world, and render the result.
- Graphical game development requires a different mindset than writing terminal-based programs.

## 2026-05-30 — First Player Movement

After successfully creating a game window, the next goal was to place something visible on the screen and make it move. I started by drawing a simple green square. Although it was only a rectangle, it represented the first object that could eventually become a player character.

To make movement possible, I needed to understand coordinates. Pygame uses a coordinate system where the top-left corner of the screen is `(0, 0)`. Moving to the right increases the x-coordinate, while moving downward increases the y-coordinate. This was slightly different from how I intuitively imagined a graph, where increasing values often move upward.

Instead of drawing the square at a fixed location, I introduced position variables to store its coordinates. By keeping track of the player's x and y positions separately, the game could update those values and redraw the player in a new location.

I then implemented movement using the WASD keys. Pressing A moved the player left, D moved the player right, W moved the player up, and S moved the player down. The movement itself was surprisingly simple. Rather than physically moving an object, the program simply adjusted the coordinate values being used when the player was drawn.

One of the most interesting concepts I encountered was continuous input. The game was not checking whether a key had been pressed once. Instead, it was checking every frame whether a key was currently being held down. This allowed the player to move smoothly while a key remained pressed.

This led to another important realization about how games work. The square was not actually moving across the screen in the way I had imagined. What was really happening was that the screen was being cleared, the coordinates were being updated, and the square was being drawn again in a slightly different position. This process repeated many times per second, creating the illusion of movement.

The idea of redrawing the entire screen every frame initially seemed inefficient, but it helped me understand one of the core principles of real-time graphics. The player, enemies, backgrounds, and user interface are constantly being redrawn. The game is effectively creating a new image every frame and displaying it so quickly that it appears seamless to the player.

Looking back, this was one of the most satisfying milestones so far. Seeing a shape respond to keyboard input made the project feel significantly more interactive. It was the first time I could directly control something inside the game world.

### Lessons Learned

- Pygame uses a coordinate system with `(0, 0)` in the top-left corner.
- The x-coordinate controls horizontal movement.
- The y-coordinate controls vertical movement.
- Position variables allow objects to be moved by updating their coordinates.
- WASD controls are implemented by checking keyboard input and adjusting position values.
- Continuous movement comes from checking keys every frame rather than once.
- Objects are not truly moving; they are being redrawn at different positions.
- Real-time graphics rely on repeatedly clearing and redrawing the screen.
- Small changes to coordinates can create the illusion of smooth movement.

## 2026-05-30 — Learning Git and GitHub

As the project began to take shape, I wanted a way to track changes and keep a history of my progress. This led me to Git and GitHub, two tools that are used throughout the software industry for version control and collaboration.

The first step was creating a Git repository inside the project folder. Before this, my files only existed on my computer. Once the repository was created, Git began tracking changes made to the project. This meant I could see what had been modified, what was new, and what had been removed.

I then created my first commit. A commit acts as a snapshot of the project at a specific point in time. Rather than simply saving files, a commit records the state of the project so it can be revisited later if needed. This introduced the idea that software development is often a series of small, incremental improvements rather than one continuous block of work.

After creating local commits, I connected the project to GitHub. This allowed me to push the repository online and store a copy outside of my computer. Seeing the project appear on GitHub for the first time was an important milestone because it transformed the project from a private collection of files into something that could be shared, backed up, and developed over time.

While learning Git, I encountered a common issue involving automatically generated files. Python had created cache files and macOS had created system files such as `.DS_Store`. These files were not part of the game itself, but Git tracked them because they existed inside the project folder.

To solve this problem, I learned about `.gitignore`. This file tells Git which files and folders should be ignored. By adding cache files and system files to `.gitignore`, I was able to prevent unnecessary files from cluttering the repository.

I also learned that adding a file to `.gitignore` does not automatically remove it from Git if it has already been committed. Because some cache files had already been tracked, I needed to explicitly remove them from version control before GitHub would stop displaying them. This was my first experience cleaning up a repository and understanding how Git manages tracked files.

The most important lesson from this stage was understanding why version control exists. At first, Git seemed like an additional layer of complexity. However, I quickly realised that it provides a complete history of a project's development. Every meaningful change can be recorded, described, and revisited later. Instead of being afraid to experiment, I now have a system that allows me to make changes while maintaining a record of previous versions.

Looking back, Git and GitHub felt like a completely separate skill from programming, but I can already see how important they are. Writing code is only part of software development. Managing, tracking, and preserving that code is equally important.

### Lessons Learned

- Git tracks changes made to files over time.
- A repository is the container that stores a project's version history.
- Commits act as snapshots of a project at a specific moment.
- GitHub provides online storage and sharing for Git repositories.
- `.gitignore` prevents unnecessary files from being tracked.
- Cache files and operating system files should generally not be included in repositories.
- Files already tracked by Git must be removed manually even after being added to `.gitignore`.
- Version control makes it easier to experiment and recover from mistakes.
- Software development involves managing code as well as writing it.

## 2026-06-09 — Connecting the Visual Game Entry Point

After building several separate pieces of the project, I reached a point where the repository contained two different versions of the game. The older version was a text-based combat loop that ran in the terminal, while the newer version was a Pygame window with movement, collision, enemy health, and simple attacking.

The main problem was that `main.py` still started the terminal version. This meant the project did not immediately launch the most recent playable version when run. To fix this, I changed the project so that `main.py` starts the Pygame game instead.

I also reorganised the Pygame code into a `run_game()` function. Before this, the game loop lived directly at the top level of the file. That works when the file is run by itself, but it is less flexible because importing the file can immediately start the game. By placing the game loop inside a function, the project can choose when to start the game more clearly.

This introduced a useful Python pattern:

```python
if __name__ == "__main__":
    run_game()
```

This check means the game starts when the file is run directly, but the code can still be imported by another file without immediately opening the game window. It is a small change, but it makes the project easier to grow as more systems are added.

While updating the entry point, I also improved the current playable loop. Attacking can now be done with either the Space key or the left mouse button while touching the enemy. The Escape key can close the game, and the R key can respawn the enemy after it has been defeated. Small control hints were added on screen so the current controls are visible while testing.

I also updated the README and task list so the documentation matches the actual state of the game. This was a good reminder that a project is not only the code itself. The notes, task list, and run instructions all help explain what exists, what has changed, and what should come next.

Looking back, this stage was less about adding a brand-new mechanic and more about connecting the project properly. The game already had movement and enemy combat, but the project needed a clear starting point. Now running the project opens the visual game directly, which makes future development feel much more natural.

### Lessons Learned

- A project can contain working code that is not actually connected to the main entry point.
- `main.py` is often used as the clear starting place for a Python program.
- Putting a game loop inside a function makes the code easier to reuse and test.
- The `if __name__ == "__main__"` pattern controls what happens when a file is run directly.
- Small controls such as quit, attack, and respawn make testing faster.
- Documentation should be updated when the playable state of the game changes.
- A good entry point makes a project easier to run, understand, and continue developing.

## 2026-06-09 — Adding a First Sense of Place

The next step was to make the game feel less like objects floating in an empty window. Instead of jumping straight into detailed art assets, I added a simple background made from basic Pygame shapes. This keeps the project understandable while still moving it closer to the mood of a real side-scrolling game.

The background now has a soft blue sky, two faded mountain layers, and a strip of grass over darker ground. The mountains use transparent colours so they sit behind the playable area instead of competing with the player and enemy. This creates a sense of distance and setting without requiring finished artwork yet.

I also introduced a `GROUND_Y` value. This represents the height of the ground in the game world. The player and enemy are positioned so the bottom of their rectangles sits on this line. This is important because it gives the scene a clear floor and stops the characters from feeling like they are floating.

Because the characters are now fixed to the ground, player movement was changed from full WASD movement to left and right movement with A and D. This is closer to the kind of side-view adventure game I want to build. Jumping can be added later as its own feature, but for now the goal was simply to establish the world and make the characters belong inside it.

This step also helped separate two different ideas: background visuals and gameplay space. The sky and mountains create atmosphere, while the ground line controls where the characters stand. Keeping those ideas separate should make it easier to improve the art later without breaking movement.

### Lessons Learned

- A game can gain atmosphere before it has finished art assets.
- Transparent background layers can create a sense of distance.
- A ground line gives characters a believable place to stand.
- Shared values such as `GROUND_Y` make positioning easier to control.
- Side-view movement can start with simple left and right controls.
- It is better to add jumping later as its own clear mechanic.
- Visual polish can be introduced gradually without making the project harder to understand.


## 2026-06-09 — Adding Jump and a Pause Menu

After fixing the characters to the ground, the next natural movement feature was jumping. This was a good step because it builds directly on the ground line from the previous milestone. The player already had a clear place to stand, so jumping could be added as movement away from that line and then back down to it.

The jump uses two simple ideas: upward velocity and gravity. When the jump key is pressed while the player is on the ground, the player receives an upward velocity. Each frame, gravity pulls that velocity back down. When the bottom of the player reaches `GROUND_Y`, the player is placed back on the ground and the vertical velocity is reset.

I also added a pause menu. Before this, Escape immediately quit the game. That worked for testing, but it was not very game-like and it meant control hints had to stay on the main screen. Now Escape opens a pause state instead. The menu has Resume, Controls, and Quit options. This makes the game screen cleaner because the controls can live inside the menu instead of being drawn over the world all the time.

The pause menu introduced the idea of game states. When the game is in the playing state, movement, jumping, attacking, and enemy text timers update normally. When the game is paused, those gameplay updates stop, but the scene still draws behind the menu. This means the pause screen feels connected to the game world rather than replacing it completely.

This was also the first step toward proper interface controls. The pause menu can be used with the keyboard, and the buttons can also be clicked with the mouse. The actual layout is still simple, but the important idea is that menus are part of the game logic too.

### Lessons Learned

- Jumping can be built from velocity and gravity.
- A player should only start a jump when they are on the ground.
- Gravity can be applied every frame to pull the player back down.
- A pause menu needs its own game state.
- Pausing should stop gameplay updates without needing to stop drawing the screen.
- Moving controls into a menu keeps the main play screen cleaner.
- Menu buttons need shared positions so drawing and clicking use the same rectangles.


## 2026-06-09 — Refining Player Controls

After testing the jump and pause menu, I adjusted the controls to feel more natural. Space is now used for jumping, which is a common platformer control and feels better than using W for vertical movement. Attacking is now kept on the left mouse button, which avoids Space trying to do two different actions during gameplay.

I also kept menu selection simple. The pause menu can be navigated with W/S or the arrow keys, and options can be selected with Enter or by clicking them with the mouse. This keeps keyboard and mouse menu input working without making the gameplay controls confusing.

This was a small change, but it was an important reminder that controls are part of game design. A feature can work technically but still need adjustment once it is tested in the flow of the game.

### Lessons Learned

- Controls should be adjusted when they feel awkward in play.
- Space is a natural jump key for a side-view game.
- One key should avoid doing multiple gameplay actions at the same time.
- Menu controls and gameplay controls can use different input rules.
- Small control refinements are worth documenting because they explain design decisions.


## 2026-06-09 — Improving Pause Menu Feedback

After adding mouse support to the pause menu, I noticed that clicking worked but hovering did not visually highlight the option under the mouse. This made the menu feel less responsive, because the player could not easily tell which button the mouse was currently over.

To improve this, mouse movement now checks whether the cursor is over one of the pause menu buttons. When it is, the game updates the selected pause option to match the hovered button. This means the same highlight system works for both keyboard navigation and mouse movement instead of creating two separate selection systems.

### Lessons Learned

- Mouse input should usually provide visual feedback before a click happens.
- Hover feedback makes menus feel more responsive.
- Reusing one selected option keeps keyboard and mouse navigation consistent.
- Small interface polish can make a feature feel much more complete.


## 2026-06-09 — Adding a Simple Sword

The next step was to give the player a visible weapon. Instead of creating detailed character art, I added a simple sword made from basic rectangles: one rectangle for the blade and one for the hilt. This keeps the visual style simple while making the character read more clearly as a playable hero.

To make the sword feel attached to the player, the game now tracks which direction the player is facing. Moving right sets the facing direction to the right, and moving left sets it to the left. The sword is then drawn on that side of the player. This is a small change, but it introduces an important idea: the player can have state that affects how they are drawn.

The sword also changes combat slightly. Before this, the player had to overlap the enemy with their body to attack. Now the game creates a sword rectangle and checks whether that rectangle touches the enemy. This means the sword is not only visual; it also gives the attack its own range.

This is still a very simple combat system, but it is a better foundation. Later, the sword could be animated, given a timed swing, or replaced with a sprite. For now, it gives the player a weapon and makes attacking easier to understand on screen.

### Lessons Learned

- A weapon can start as simple shapes before becoming detailed art.
- Player direction can be stored as state.
- Drawing can change based on the player's current state.
- Attack range can use its own collision rectangle.
- A visual object becomes more meaningful when it also affects gameplay.


## 2026-06-09 — Drawing a Player Silhouette

The player started as a simple square, which was useful while learning movement and collision. Now that the game has a background, ground, jumping, and a sword, the square was starting to feel too abstract. The next visual step was to turn the player into a simple silhouette-style stick figure.

Instead of adding detailed sprite art, I used basic Pygame drawing tools. The head is a circle, and the body, arms, and legs are lines. This fits the current simple art approach while moving the player closer to the moody silhouette style I want.

Importantly, I kept the existing player rectangle for movement and collision. The rectangle still controls where the player is in the world, where they land, and how the sword position is calculated. Only the drawing changed. This keeps the code easier to understand because the visual appearance and the gameplay hitbox are separate ideas.

The sword is now drawn from the front hand of the figure. It still uses the same sword collision rectangle for attacks, but visually it feels more attached to the character. This makes the player read more like a character holding a weapon instead of a box with a rectangle sticking out of it.

### Lessons Learned

- A character can be improved visually without adding image files.
- Circles and lines can create a readable stick figure silhouette.
- The drawing of a character can be separate from its collision rectangle.
- Keeping the hitbox stable avoids breaking movement and combat while improving visuals.
- Small visual upgrades can make existing mechanics feel more intentional.


## 2026-06-09 — Adding World Progression

After the player had a clearer silhouette and sword, the next step was to make the world feel larger than one static screen. Instead of creating a full level system all at once, I added a single value called `world_x`. This value represents how far the player has travelled through the world.

The player now stays near a fixed position on the screen while movement changes `world_x`. This creates the feeling of travelling through the scene because the background and world objects move relative to that progress value. It also introduces an important game development idea: screen position and world position are not always the same thing.

The enemy now has a world position too. Its screen position is calculated from its world position and the player's current progress. This means the enemy can exist in the world ahead of the player, then appear on screen as the player moves forward.

I also made the background feel more alive. Clouds drift slowly, distant mountains move more slowly than closer mountains, and small grass highlights repeat along the ground. I also added a `background_time` value so some of the background motion can continue while the game is playing, even if the player is not currently moving. This is called parallax movement. It creates a sense of depth because far-away things move less than nearby things.

This step still keeps the art simple. The background is made from shapes, not image files, but the scene now feels more like a living place. It is a good foundation for later adding proper levels, more enemies, and background art assets.

### Lessons Learned

- A scrolling world can start with one progress value.
- Screen position is where something is drawn on the window.
- World position is where something exists in the larger game world.
- Parallax makes far-away layers move slower than nearby layers.
- Small moving details can make a background feel more alive.
- Time-based animation and movement-based scrolling can work together.
- World progression can be added before building a full level system.


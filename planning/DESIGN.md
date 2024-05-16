# Cowboy Cat Clash 

Yeehaw!

## Objective
- Beat the other player in this local two-player fighting game!

## Rules 
- Fighters do not have to be unique (Fighter Select Screen)
- 0 HP means defeat (Battle Screen)
- Stage has certain x,y bounds (Battle Screen)

## Mechanics
- Both players pick a fighter (Fighter Select Screen)
- Fight until one player reaches 0 HP (Battle Screen)
- Repeat

## Controls
Player 1 controls (Player 2 controls)
- W (^): jump
- A (<)/D (>): depends on orientation
  - Forward walk/backward walk
- S (v): Block
- Q (SHIFT): Heavy attack
- E (ENTER): Light attack

## Assets
Start Screen
- Title text
- Background
- Buttons
- Button click sounds
- Start music

Controls Screen
- Share background, music w Start Screen

Fighter Select Screen
- Share background w Start Screen
- Portrait of each fighter
- Fighter select music

Fighter Showcase Screen
- Background
- Fighter showcase music
- Announcer

Battle Screen
- Health bar
- Stage
- Background
- Fighter sprites per fighter
  - Idle
  - Run
  - Jump
  - Victory
  - Defeat
  - Heavy attack
  - Light attack
  - Block
  - Stunned
  
- Jump sounds
- Hit sounds

Fighters
-Ollie: gray tabby in cowboy hat
  -"Average" speed, dmg (the OG character/the beginner character in fighting games)
  -Baseline for other fighters
-Bowie: black blob cat
  -Wildcard, varying speed and dmg, possibly randomized
-Doodles: chunky calico
  -Slow speed, high dmg, slow startup + recovery but fast stun recovery
-Venturi's Cat: siamese with wheat
  -Fast speed, low dmg, fast startup + recovery but easily stunned

Victory Screen
- Victory music

## Screens
Start Screen
- Play button --> to Fighter Select Screen.
- Controls button --> to Controls Screen.
- Quit button --> quits game.

Controls Screen
- From Start Screen ESC --> to Start Screen.
- From Battle Screen ESC --> to Pause Screen.

Fighter Select Screen
- Players select fighters --> Fighter Showcase Screen
- Left click selects Player 1, right click selects Player 2

Fighter Showcase Screen
- Cutscene plays --> to Battle Screen.
- Could also be a part of Battle Screen overlayed on top

Battle Screen
- ESC --> to Pause Screen.
- One fighter hits 0 HP --> to Victory Screen.

Pause Screen
- ESC --> to Battle Screen.
- Controls button --> to Controls Screen.
- Quit button --> quits game.

Victory Screen
- Play victory cutscene.
- Rematch --> to Battle Screen.
- Fighter Select --> to Fighter Select Screen.

## Gameplay Flow
- No storyline
- Main gameplay loop is: pick fighters, battle, rematch or pick fighters again, repeat.
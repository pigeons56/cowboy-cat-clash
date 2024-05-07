# CAT FIGHTER

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
  - +Q (ENTER): up attack
- A (<)/D (>): depends on orientation
  - Forward walk/backward walk
  - Q+Forward: attack
  - Q+Backward: block
- S+Q (ENTER) down attack (midair only)
- E ('): special

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
  - Forward attack
  - Up attack
  - Block
  
- Jump sounds
- Hit sounds

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
- ESC --> to Start Screen.
- Players select fighters --> Fighter Showcase Screen

Fighter Showcase Screen
- Cutscene plays --> to Battle Screen.

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
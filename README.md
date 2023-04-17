# Dogfight
A little pygame-based game I made. Control a plane, shoot things, pretty straightforward.

### Controls
So far, a plane can be controlled as follows:

`A / LEFT` to turn left

`D / RIGHT` to turn right

`W / UP` to increase speed

`S / DOWN` to decrease speed

`SPACE / LEFT SHIFT` to shoot a single bullet, currently, there is no cooldown

### Mechanics
Several airships are spawned with random coordinates and rotation, once hit five times by a bullet, they explode. If the player crashes into an airship, the airship explodes as well, the player loses 2 HP (out of 5).

Once the player's HP drops to zero, the game loop stops. If any explosions are currently present, their time still runs, text 'GAME OVER' is displayed in the middle of the screen.

TODO: add an option to win/lose the game
hard TODO: add a semi-intelligent oponent plane or anti-aircraft gun
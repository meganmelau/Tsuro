##**TCP Message Syntax**

#### Player connect to game
Player connects to a game

client: `["tsuro-connect", <player name>]`

Server will send back player's avatar color right after they connect to game

server: `["setup", <player color>]`

Server will send back all players' colors in turn order at the beginning of the game

server: `["setup", <list of all players' colors>]`


#### Initial Round

Sending a hand for player to choose a move

player-proxy:`["initial move request", tile-index, tile-index, tile-index]`

Respond with 0/1/2 as the index, rotation, and position to place avatar

client: `["initial move respond", index, rotation, x, y, port]`

#### Intermediate Round

Sending a hand for player to choose a move

player-proxy: `["intermediate move request", tile-index, tile-index]`

Respond with 0/1 as the index, rotation, and position to place avatar

client: `["intermediate move respond", index, rotation, x, y]`

#### Updating board

Referee updates the board after each player's turn

player-proxy: `["board update", current-player-color, tile-index, rotation, x, y]`

Referee updates the players positions on the board after removing players who have lost

A player position is in JSON format: `{"color": <player color>, "position": [x, y, port]}`

player-proxy: `["board update", <list of player positions>]`

#### Disconnecting client

In the case client didn't respond in time to choose a move, the player proxy will return -1 as the index for choosing a 
move, causing the referee to remove the player as making invalid move.


```
Referee     Proxy     Client     Client N
   |          |          |           |
   |<---------|<---------|<----------| Players connect with name and strategy
   |          |          |           |
   |--------->|--------->|---------->| Players given color
   |          |          |           |
   |          |          |           | Wait 30 seconds
   .          .          .           . 
   |--------->|--------->|           | initial move request
   |<---------|<---------|           | initial move response
   |          |          |           |
   |--------->|--------->|---------->| board the placement updates
   |--------->|--------->|---------->| board player position update
   |          |          |           |
   |          |          |           | repeat for all players
   .          .          .           .
   |--------->|--------->|           | intermediate move request
   |<---------|<---------|           | intermediate move response
   |          |          |           |
   |--------->|--------->|---------->| board the placement updates
   |--------->|--------->|---------->| board player position update
   |          |          |           |
   |          |          |           | repeat for all players  
   .          .          .           .
   |--------->|--------->|---------->| game over

```

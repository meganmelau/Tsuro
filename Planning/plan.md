#### Part 1: Describes the identifiable components of your software system.

##### Pieces that make up an automated player:

-   Avatar
    

-   Name
    
-   Age(Connection time whoever is connected for the longest): the oldest person goes first
    
-   Request the game status
    
-   Receive, pick, rotate, and send back tiles from the server
    
-   Choose a port to start at
    

  

##### Pieces that make up the game software:

-   Board layout
    
-   Display the status of the board
    
-   Wait for 3 - 5 players to connect and start the game
    
-   Generate Tiles
    
-   Send hands to Players
    
-   Place tiles selected by Players
    
-   Move Player avatars after placing tiles
    
-   Check how many players are left
    
-   End the game when either one player is left or no players are left
    
-   Disconnect inactive players after 4ish minutes
    
-   Keep track of how many games a Player has won in this instance
    
-   Determine whether a move violates the rules
    
-   Remove players from the game that have lost
    

  

#### Part 2: Implementation Plan

Player:

-   A player has an age, position, color
    

-   Position: (Tile t, int port)
    
-   Age: int (based on connection time)
    
-   Color: string
    
-   renderPlayer()
    

Tile:

-   Each tile has 8 ports numbered 0-7.
    

-   North: 0, 1
    
-   East: 2, 3
    
-   South: 4, 5
    
-   West: 6, 7
    

-   Each tile has a list called paths, which contains 4 2-index arrays representing the 4 connections from one port to another.
    
-   When a clockwise rotation happens, for every 90 degrees, each of the numbers in the paths list is updated to represent same tile with different orientation: New Port# = (Old Port# + 2) mod 8.
    
-   A Tile has the following:
    

-   occupiedPorts: dictionary where port -> player
    
-   Paths: List((int, int) ... (int, int)) where (int,int) represents connections between ports
    
-   Constructor that randomly generates connections
    
-   removeAvatar(Avatar): void
    
-   addAvatar(Avatar, port): void
    
-   compare(Tile): bool
    
-   getPath(port): int
    
-   isOccupied(port): bool
    
-   rotate90Degrees(): list((int,int) ... (int,int))
    
-   renderTile()
    

Board:

-   A Board has a 2-D array of Tiles size 10x10
    
-   addTile(x,y): void
    
-   getTile(x,y): Tile
    
-   renderBoard()
    

Referee:

-   turnCount: int
    
-   pickTile(): Tile
    
-   sendTiles(Tile, Player): void
    
-   receiveTile(Player): Tile
    
-   receiveFirstMove(Player): (Tile, (int x, int y))
    
-   checkMove(Tile, Player): bool
    

Game (Server):

-   Board
    
-   Deck of unique 35 tiles (from which the referee will randomly draw and give to players)
    
-   Referee
    
-   List of players
    
-   Dictionary mapping player to a socket connection
    
-   Main(): void
    
-   StartGame(): void
    

The server's main function will create the deck of unique tiles and wait for players to connect on a certain port for a certain period of time. At the end of that waiting session, if there are 3 to 5 players, start the game. Else, remove all players. The server starts the game by creating an empty Board, and a Referee. The Referee manages turns, communicates with Players, checks if a Player is knocked out, and checks if the game is over. To run a turn, the Referee will give the Players tiles in order and receive the tile that the Player wants to place. For the first turn, the Referee will give each Player 3 Tiles and receive the chosen Tile and the place the Player wants to place it. The Referee will first check to see if the chosen move is valid. If so, the Referee will then interact with the Board on behalf of the Player to place the Tile and move the Player's Avatar. The Referee will then move any Avatars on the Board that were affected by the current Player's move. Then the Referee will remove any Avatars that have lost as a result of the move and determine if a Player has won the game. Once the game has been completed, the server will query each Player to see if they want to play another game. If the number of Players that respond yes is enough for a second game, the server will reset the Board and begin a new game, otherwise, the server will disconnect from all players and start listening for a new game.

Plan for implementation:

-   Implement Tile and Board
    
-   Implement Player and Referee
    
-   Implement Server
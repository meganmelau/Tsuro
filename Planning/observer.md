# Observer
The observer watches the game as it progresses. The board is 
visually represented at each game state.

Mock ups:
1. start
2. initial placement
3. intermediate placement
4. game win

#### Class variable
board: the current state of the board, in the format for rendering

#### Class methods
render(): renders the board of this observer

set_board_state(): sets the board of this observer to a new state

##### Notes
If this is implemented, the referee running the game should add some wait time so that the observer can display
changes to the board in a meaningful way, rather than making changes as soon as they come in. Since players are
automated, changes will be made extremely quickly and so waiting will allow the observer to preserve the state of
the board for observation longer.


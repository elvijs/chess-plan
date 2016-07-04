## Finish the `describe_moves` module 
The next step is to add unit tests for the following functions:
* get_piece_letter(move_string)
* get_to_square(move_string)
* get_from_square(piece_letter, to_square, board)
* is_check(move_string)
* is_capture(move_string)
* is_checkmate(move_string)

This will allow us to write reliable functions and 
get the `describe_moves` module working well (needs better naming).
That in turn unlocks weighted heatmaps including:
* weighing by how long pieces stay on a square,
* weighing by piece positions, when checkmates or wins are delivered,
* weighing by evaluation swings - once computer analysis is done.

## Improve the opening navigation
A drop down with a mapping of openings to regexes should be implemented.
This will massively improve the opening browsing experience.

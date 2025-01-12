class Instructions:
     """
     Instructions is a helper class for the user_interface class.
     Because of voluminous explanations and options those are outsourced here.
     """
     
     def _show_input_options_pre_game(current_difficulty:str,current_size:int):
          # TODO implement input given game
          print("The following are all the input options before the game:\
               \n[n]: Start a new sudoku game \
               \n[d]: Set the difficulty (easy, medium, hard). The current difficulty is " + current_difficulty.name + "\
               \n[s]: Set size of sudoku. The current size is " + str(current_size) +"\
               \n[p]: Set player \
               \n[o]: Open game from file \
               \n[h]: Show all high scores \
               \n[r]: Show rules of sudoku \
               \n-------------------------------------------------------------------------------")

     def _show_input_options_during_game():
          print("The following are all the input options during the game:\
               \n[r]: Show rules of sudoku \
               \n[h]: Give me a hint \
               \n[c]: Type in new value at specified coordinates \
               \n[u]: Show/Hide all user inputs until now\
               \n[w]: Show wrong fields \
               \n[s]: Solve rest of sudoku \
               \n[q]: Save the game and quit \
               \n-------------------------------------------------------------------------------")

     def _show_input_options_during_coordinates_values_input():
          print("Please navigate to the desired field (by pressing arrow keys ↑,↓,→,←) and enter the number (1-9) you want to fill in. Your cursor is at the blinking cell.\
               \n[0]: Empty a cell with zero \
               \n[u]: Show/Hide all user inputs until now \
               \n[esc]: Leave this menu with escape key \
               \n-------------------------------------------------------------------------------")

     def _show_input_options_save_game(name: str, path: str):
          print("[s]: Save the game and quit \
               \n[f]: Change the current filename [" + str(name) + "] \
               \n[p]: Change the current filepath [" + str(path) + "] \
               \n-------------------------------------------------------------------------------")

     def show_rules():
          print("Sudoku is a number puzzle played normally on a 9x9 grid, which is divided into 9 smaller 3x3 subgrids. The objective is to fill the grid with numbers from 1 to 9, following three main rules: \
               \n- Row Rule: Each row must contain all the numbers from 1 to 9 without repetition. \
               \n- Column Rule: Each column must also contain all the numbers from 1 to 9 without repetition. \
               \n- Subgrid Rule: Each of the nine 3x3 subgrids must contain all the numbers from 1 to 9 without repetition. \
               \nThe puzzle starts with some numbers already filled in, and the goal is to complete the grid while adhering to these rules.")
          input("Press enter to proceed!\n")
# SnakeFight

A game where snakes fight to the death

# TO DO  

- lobby

  - Fix buggyness asociated with finding a server
  - Catch all errors
  - add quit button
  - Send people to servergame/clientgame
- main game
  - Share required drawing variables between server and client
    - Create sending protocol
    - Create socket
    - Send Data
  - Make it so that the game still runs while the display is resizing
    - Make main game code inside one thread, make sure that the clock.tick is in there
    - Make sending code inside another thread
    - Leave the resizing code/ displaying code outside of a thread.
- ...
- Tutorial
  - add a button on the main menu
  - make a tutorial file
  - ...
- ...
- Window
  - Make it so that the window stays open the entire time
  - make it so that if an error occurs in any branch off the main menu, it returns you to the main menu
    - Add a disconect screen
  - Make it so that the window can be resized
  - Adjust window settings so that the window represents other games
  - cosmetic changes
    - rename window
- Make program look nice
    - COMMENT
    - Reformat where necesary
- Finish
    - Play test
        - try to break the game
    - Cool app image
    - Make into executable
    - PROFIT

# Acknowledgements

Although Jacob and Wes did all the coding, they would like to formally thank Mclean Muir who used his great intellect to inspire them to make the game playable. Wes and Jacob would like to ensure that everyone seeing this game knows that Mclean has done 90% of all the work on this project.

# Disclaimer

We are not responsible for any injuries or death associated with this game. Please do not sue.

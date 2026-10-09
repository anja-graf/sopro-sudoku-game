# Software Assignment: Developing a Game

## Schedule

| Milestone | Start Date | Submission Date | Deliverable                                            | Points    |
|-----------|------------|-----------------|--------------------------------------------------------|-----------|
| 1         | 15.11.2024 | 08.12.2024      | [Planning Document](#planning-document-requirements)   | 4         |
| 2         | 22.11.2024 | 12.01.2025      | [Game Code](#game-code)                                | 13        |
| 3         | 06.01.2025 | 01.03.2025      | [AI Player Code](#ai-implementation)                   | 9         |
| 4         |            | 01.03.2025      | [Video Presentation](#video-presentation-requirements) | 4         |
|           |            |                 |                                                        | Total: 30 |


## How it works

- Assign clear roles for each person (e.g. game logic, player interface)
- __Each student needs to commit their own contributions to this repository,
  that's how we assign points__
- Use Git to share your code and track issues
- Document your code! This is also part of your final grade!

## Submission

All submissions are via Git and __must__ be confirmed in Vips. One submission
per group per milestone.

## Games to choose from:

### Simple

If this course is your first encounter with programming, choose one of these
options. These are single-player games with clear and simple rule sets and
clear win conditions. You can turn this first experience into a first success
if you plan and document everything carefully from the beginning and break down
each part of the game into small concrete subproblems.

- Sudoku
- Solitaire

### Medium

If you have some prior programming experience, these are a good choice. Good
planning and documentation is important because while they might seem simple at
first, these games can get quite complex.

- Black Jack
- Checkers

### Complex

If you are an experienced programmer, feel like you got a good grasp on Python
during this semester, and are looking for a challenge, this is for you. These
games are very complex, with many rules and interactions. Make sure you have a
precise design plan and document everything carefully, especially the things
that take a few attempts to work correctly. A modular implementation and tests
for each module are extremely important.

- Chess
- Space Invaders


## Planning Document Requirements

Due: 08.12.2024

- Format: 2 full pages, 11 point Arial or Times font
- State which game you are planning to implement
- State the role distribution within your team (who does what?)
- State which classes, methods and functions you will need (at least a Game
  class, a Player class, and a UserInterface class)
- Describe in 1-3 sentences each what each class, method and function will do.
  What are the inputs and outputs?


## Game Code

Due: 12.01.2025

### First Steps

- The three classes in the three files need to be implemented in your code.
  - How you implement them is up to you. 
  - You can use the method stubs for inspiration but you don't need to use
    these exact ones.
  - You can add additional classes/methods/functions as you see fit.
- Test every small part you implement frequently! This will help you find bugs
  early.
- Ask the tutor if you have any questions

### Requirements

- Make sure a player understands how to play the game. Give instructions
  regarding the rules and make clear that the menu is understandable.
- Your program has to provide a highscore list. 
  - After the program is quit, the highscore list has to be saved in a file.  
  - When you start your program, the highscore list has to be loaded.
  - No shelve or pickle allowed here – the highscore list must be saved to and
    read from a text file!
- There must be a user interface, but it does not need to be fancy
  - Console interface is enough
  - GUI (Tkinter, ...) optional, only partially supported by tutors
  - No physics engines
  - User controls must be implemented in UI class, NOT in Player class
- You must document your code using comments and docstrings.
  - This will help your collaborators understand what each method, function,
    and even a single line (if there is something complicated) does
  - It also helps you remember what you did
  - This is also part of your final grade!
- You must write doctests for your code.
  - Ideally there should be 1-2 doctests for each function/method
  - But depending on what the function/method does, it does not always make
    sense to have a test (e.g. for methods with side-effects that do not return
    anything)


### Object-Oriented Modeling

At a high-level:
- Use object-oriented programming (OOP)!
- Modular code design: 
  - Break down into subproblems, define separate classes, methods, functions
  - Use multiple .py files, import them as modules as appropriate
  - All the given classes and method stubs must be implemented!
  - In addition, you may add any classes / methods you need for your particular
    game (in separate files, as appropriate)

In more detail:
- Your code should model parts of the game as objects wherever appropriate. 
- Users should be modeled as objects. New players can register as users, and
  pick a password.
- Each round played should also be an object, which contains the current state
  of the game. This allows for pausing a game and starting another one. 
  - When quitting the program, the current game should be saved, and when
    starting again, each user should have the possibility to continue his or
    her current game. (It is sufficient if each user who logs in can either
    start a new game or continue a saved one, if there is any.) 
  - For the objects which are supposed to be saved to a (text) file, think of
    an appropriate file format and provide methods that write the state of an
    object to file or that read the state of an object from file.
  - If you are a beginner of programming, we recommend actually saving the
    state of games etc. as text files, as this is an excellent exercise to get
    some routine with writing and reading files. 
  - If you are already an advanced programmer, you may serialize user / game
    state objects using shelve (see
    https://docs.python.org/3.4/library/shelve.html)
- Think about what else could be modeled as an object (e.g., the board, deck of
  cards and each single card, ...)


## AI Implementation

Due: 01.03.2025

### Requirements

- The "AI" player should interact with the game "like a human", i.e. should
  have the same (not more or fewer) input/output options.
- It should be able to play through a (round of a) game __from start to
  finish__.
- It should __react differently to different game states__ (not just repeat the
  same action always).
- Make sure that it is __always possible to return to the main menu__ and the
  AI does not get caught in an infinite loop. Depending on your design, you may
  need to build in a __failsafe mechanism__ like a timeout counter or a button
  press that interrupts the AI playthrough.
- The AI should __pass all applicable doctests / unit tests__, and vice versa,
  you can refine your tests based on your observations from the AI. 


- As with the base game code, we use the commit history to track individual
  contributions, so make sure to __distribute the workload fairly among the
  group members__.


- As always: __planning and documentation are important!__


### Things that are allowed

- You already had a lot of freedom for implementing the base game, you now have
  even more freedom and flexibility.
- __The AI does not need to be very good at the game!__ 
  - Relatively simple, rule-based approaches are ok.
  - It's ok if it often (or always) loses.
  - Advanced optimization and/or data science and/or machine learning
    approaches are great if you want to try, but not required.
- You may change or add features to your original game code to make the AI
  work.
  - E.g. you should add an entry in the UI where the user can select to play
    against the AI or let the AI play on its own.
  - You can also take this as an opportunity to find and fix bugs.
  - Note however that these changes will NOT be taken into account
    retroactively when grading Milestone 2, for that we really only look at the
    last commit before the Milestone 2 deadline.


## Video Presentation Requirements

Due: 01.03.2025

- __Total length: 3 minutes max__
- Language: English strongly preferred, German also okay
- __Required:__ Screen recording video where you show and explain your code
  - MP4 file format
  - Each team member should name all parts of the game they worked on
  - Each team member should __briefly explain__ how 1-2 of their contributions
    work
  - Really, keep it short! We just want to see that you understand what you
    did.
  - Show how to start a new game
  - Optional: a short demo of your game (30 seconds max!)
- __Required:__ 3-5 slides with illustrations. 
  - PPT(X) or ODP format (no other formats)
  - Please use bullet points in the Speaker Notes function to make it clear
    what you would be saying about this slide if you were presenting if live.
    The slides will be submitted separately and should be readable and
    understandable independently of the video.
  - There should be one overview slide summarizing your project plan and result
    and the link to your Git repository.
  - Otherwise, the slides can either show pretty much what you are also showing
    in the screencast, or highlight a few specific design and/or implementation
    decisions. 
- **Upload** the video and the slides to DigiCampus to the folder "SoPro
  Presentations".
  - Files should be named "GroupXX_GAMENAME_LASTNAME1_LASTNAME2_LASTNAME3".
- If possible (i.e. if the files are not too large), also upload your slides
  and video to your project's **Git repository**.

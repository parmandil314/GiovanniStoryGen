# Giovanni's Room Story Generator
A program that generates Giovanni's Room-style story plots, given character specifications.

## Program Structure
At its core, the program operates on a list of characters. Each character represents an actor in the plot of the story, and is represented as a container of data. Each character representation contains the following:
- The character's name
- The character's current goal
- The character's current and previous locations
- The character's current self-hatred, as an integer
- Whether the character is alive
- Whether the character is available for participation in the plot
- The character's traits (i.e. "Gay", "Love is Transactional", "Love Is Not Transactional"). A trait can technically be anything, but in v1.0.0 only certain specific traits will influence the plot events.
- The character's relationships with other characters:
  - The name of the other character
  - Whether they have actually met 
  - Their current and past relationship statuses (i.e. "Sexual Abuse Victim", "Private Lover", "Official Lover").
    - These can be asymmetrical, meaning that two characters in a relationship can have different relationship statuses for each other. Only one "Official Lover" can be had at a time, but the number of "Private Lovers" a character can have at once should be unbounded within reasonable expectations. 
  - The current character's internal and external platonic love for the other character (internal = the love they truly feel; external = the love they outwardly present)
  - The current character's internal and external sexual interest in the other character (internal = the interest they truly feel; external = the interest they outwardly present) 
  - The current character's internal and external romantic love for the other character (internal = the love they truly feel; external = the love they outwardly present) 
    - Romantic love is differentiated from sexual interest in that it includes personal attraction as well as sexual attraction.
    
When the program starts up, an interface should be created that allows the user to run the simulation over the course of an arbitrary number of rounds.

During each round, a set of rules should be applied one by one to the list of characters, testing for certain conditions and triggering certain actions if the conditions are satisfied. 

If a rule is triggered, the round ends after the corresponding action resolves. If no rule triggers, the plot should end.

Each rule is a rule of the world of Giovanni's Room, and is meant to be true in any story set in this world. The rules for v1.0.0 are described below.

### Rules (apply in order):
1. If all the characters in each location who are alive and available have not met each other, but have initial relationship values listed, they meet each other somehow. This applies in all locations; for example, if there were two characters in Spain who hadn't met each other, and three characters in France who hadn't met each other, both groups would meet each other.
2. If some or all of the characters met each other during the last round, the ones who began romantic relationships when they met will sleep together.
   - If a lover has the "Love Is Transactional" trait, they will lose 1 point of internal platonic love, internal sexual interest, and internal romantic love for the other lover. 
   - However, if a lover has the "Love is Not Transactional" trait, the above statement will not trigger, and that lover will gain 2 points of external platonic love and 1 point each of internal platonic, internal sexual, and internal romantic love.
3. If two private lovers slept together during the last round, they will tell each other about any existing official lovers they have.
   - Each private lover that has an official lover causes both private lovers to lose 1 point each of internal platonic, internal sexual, and internal romantic love for each other.
4. If two private lovers are both alive and available, and they have been private lovers for 3 rounds since they met, they will reach some seemingly insignificant point at which they either dramatically strengthen or dramatically weaken their relationship.

   - If a lover thus involved feels 5 or more points of self-hatred, they lose 1 point of every kind of love for their partner, and gain 1 point of self-hatred.

   - If a lover thus involved feels less than 5 points of self-hatred, they gain 1 point of every kind of love for their partner.
5. If two private lovers have been together for 4 rounds since they last met, the lover with the most self-hatred, if alive and available, will receive letters from any official lover they may have that will give them the goal "Prove Conventionality", if they do not possess the "Straight" trait. If they do possess the "Straight" trait, they gain 1 point of self-hatred.
6. If a character has the goal "Prove Conventionality", and they are alive and available, they will spend time with and subsequently sleep with a person who they would find themselves attracted to if they were straight. They gain 1 point of self-hatred, and lose their current goal.
7. If a character has had the relationship "Employed; Sexual Abuse Victim" with another character for 6 rounds, and both characters are alive and available, that relationship is replaced with "Sexual Abuse Victim" as that character loses their job. That character also loses 1 point of every kind of love for their sexual abuser.
8. If a character has been in a separate location from their official lover (if any) for 7 rounds, and they have no private lovers, and they are alive and available, they return to their official lover's location.
9. If a character is alive and available, and their official lover has met any private lovers they have, that character gains 1 point of self-hatred.
10. If a character has 10 or more points of self-hatred, they break up with any existing private lovers. They and their private lovers lose 5 points of every kind of love for each other, to a minimum of 1. Their relationship changes to "Ex-Private Lover". The character who has more self-hatred loses 1 point of it.
11. If a character has broken up with a private lover, and they have no official lover, they do something drastic:
    - If they have a SAV (Sexual Abuse Victim) relationship with another character, they are sexually abused by and (in response) murder that character. Each of the murderer's private lovers, if any, gain 2 points of self-hatred.
  
        - If the murderer is not straight, they are sentenced to death for the murder, become unavailable, and change location to "Death Row".
  
        - Otherwise, they are not sentenced, but gain 3 points of self-hatred
12. If a character broke up with a private lover at any point in the past, they begin to separate from their official lover, if any. If they are in an "Official Lover" relationship, both official lovers lose 1 point of each kind of internal love.
13. If a character has 7 or less internal sexual interest in their official lover (if any), they have a minor affair and are caught by their official lover. Both official lovers lose 5 points of each kind of love, to a minimum of 1, and their relationship changes to "Ex-Official Lover".
14. If a character is in the "Death Row" location, and rule #11 did not trigger last turn, they are executed, stop being alive, and cause each other character they have ever had as a private lover to gain 2 points of self-hatred.
15. If a character's self-hatred is greater than 10, and they are alive and available, they commit suicide. Each of the characters they have had "Private Lover" relationships with gain 2 points of self-hatred.



## How to Install:
Those who want to run this program must first install Python on their computer. Python is a popular general-purpose programming language, known for being easy to learn and use.
### Python installation on Windows:
- Go to python.org/downloads/windows and click the link under "Python 3.12.7" that says "Windows Installer (64-bit)".
It should download a file called "python-3.12.7-amd64.exe" to your computer.

- Navigate to this file in File Explorer and run it. It will open an installation wizard.
Check the boxes titled "Use admin privileges when installing py.exe" and "Add python.exe to PATH."

- Click "Install Now".
You may need to input an administrator password.

- Python will be installed on your computer.

### Python installation on a Mac:
- Go to python.org/downloads/macos and click the link under "Python 3.12.7 - Oct. 1, 2024" that says "macOS 64-bit universal2 installer".
It should download a file called "python-3.12.7-macos11.pkg" to your computer.

- Navigate to this file in Finder and open (double-click) it. It will open an installation wizard.
Click "Continue" until you reach the license terms, then click "Agree".

- Click "Install".

- Python will be installed on your computer.
	
Once Python is installed, you will need to download the Python code for this program from this GitHub page.

## Program Execution Instructions
- On Windows, press the "Windows+R" key combination, and type "cmd" in the box that appears onscreen. On a Mac, open the Terminal application. 

- Type in "cd Downloads/GiovanniStoryGen-1.0.0".

- Type in "python3 src/main.py" on a Mac, or "python src/main.py" on Windows.

- The program should output this text onscreen:

```
Welcome to the Giovanni's Room Story Generator!
For a complete program specification, 
view README.md in the project root directory.
To learn how to navigate this interface, input 'help'
or look at the README.
>>>
```

## How to Use:
Before doing anything else, run the program following the steps detailed in the "How to Run" section.
- To load a set of characters from a folder:
  - Input `load-chars path/to/folder` where path/to/folder is replaced with the path to the folder you stored the character files in.

- To save a story to a file:
  
  - Input `save filename` to save the story to a file called `filename`.
  
- To load a story from a file:
  - Input `load filename` to load a story from a file called `filename`.
    
- To run a round of a story that has been loaded:
  - Input `round`.
- To run an arbitrary number of rounds:
  - Input `rounds #`, where `#` is the number of rounds you want to run
- To output a version of these instructions:
  - Input `help`
- To view a character's information:
  - Input `inspect character` where `character` is the name of the character
- To quit the program:
  - Input `quit` and then `Y` or `y`.

## How to Use:
- Run the program.

- Input `load-chars path/to/folder` where "folder" is the path to a folder containing your character JSON files (i.e. examples/g_room).

- Run a few rounds.

- The plot of a story should be outputted.

## How to Create a Character:
Make a copy of one of the character files in the examples/g_room folder.
Play around with it. You can change any of the numbers (self-hatred, love values, etc.), any of the names, the location, the goal, and any of the traits.

#### Make sure everything else stays exactly the same. Even a missing bracket will cause the program to exit with a weird error message.

A list of valid traits that will change the course of the plot:
- "LIT" ("Love is Transactional")
- "LINT" ("Love is Not Transactional")
- "Straight"

A list of valid relationship values:

- "EPL: Ex-Private Lover
- "EOL" : Ex-Official Lover
- "OL" : Official Lover
- "PL" : Private Lover
- "SAP" : Sexual Abuse Perpetrator
- "SAV" : Sexual Abuse Victim

You might see other traits or relationship values in the pre-supplied JSON files. They won't affect the program's output. They're left over from development, when I considered implementing other rules that these traits would affect. However, I didn't implement those rules, so the corresponding traits mean nothing.

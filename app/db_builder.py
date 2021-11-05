'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang, Owen Yaggy
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="StoryCharger.db"

def dbseteup():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("DROP TABLE IF EXISTS Users")
    command = "CREATE TABLE Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)"    
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("DROP TABLE IF EXISTS Stories")
    command = "CREATE TABLE Stories (ID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, FullStory TEXT, Latest_Update TEXT)"
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("DROP TABLE IF EXISTS Contributions")
    command = "CREATE TABLE Contributions (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID INTEGER, StoryID INTEGER, Contribution TEXT, FOREIGN KEY (UserID) REFERENCES Users (ID), FOREIGN KEY (StoryID) REFERENCES Stories (ID))"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database


def get_contributed_stories(username):
    pass

def get_editable_stories(username):
    pass


def signup(username, password):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create

    c = db.cursor()

    dbseteup()

    c.execute("""SELECT Username FROM Users WHERE Username=?""",[username])
    result = c.fetchone()

    if result:
        return(True, "Username already exists")
    else:
        c.execute('INSERT INTO Users VALUES (null, ?, ?)', (username, password))
        db.commit()
        db.close()
        return(False, "Welcome")


def login(username, password):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create

    c = db.cursor()

    c.execute("""SELECT Username FROM Users WHERE Username=? AND Password=?""",[username, password])
    result = c.fetchone()

    if result:
        ##access this specifc user data
        return(False)

    else:
        return(True)


def new_story(title, story, username):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute('INSERT INTO Stories VALUES (null, ?, ?, ?)', (title, story, story))

    c.execute("SELECT ID FROM Stories WHERE Title=? AND Latest_Update=? AND FullStory=?", [title, story, story])
    story_id = c.fetchone()[0]

    c.execute("SELECT ID FROM Users WHERE Username=?", [username])
    user_id = c.fetchone()[0]

    c.execute('INSERT INTO Contributions VALUES (null, ?, ?, ?)', (story_id, user_id, story))

    db.commit()
    db.close()


def add_story(story_id, story, new_update, username):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute('UPDATE Stories SET FullStory=? AND Latest_Update=? WHERE ID=?', (story, new_update, story_id))

    c.execute("SELECT ID FROM Users WHERE Username=?", [username])
    user_id = c.fetchone()[0]

    c.execute('INSERT INTO Contributions VALUES (null, ?, ?, ?)', (story_id, user_id, new_update))

    db.commit()
    db.close()

def view_story(story_id):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute("SELECT Title AND FullStory AND Latest_Update WHERE ID=?", [story_id])
    Title = c.fetchone()[0]
    Story = c.fetchone()[1]
    LatestUpdate = c.fetchone()[2]

    return (Title, Story, LatestUpdate)
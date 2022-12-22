# Pymodoro
## Video Demo:  https://youtu.be/EVZE1jc5Qm0
#### Description:
>Pomodoro application created with the Flask framework
#### Features:
0. Main Page
    - This is where the user completes the actual pomodoro sessions
    - Start/stop button that makes a click sound once pressed
    - Alarm sound is emmited each time the timer reaches zero
    - Also contains instructions on the bottom regarding use of the timer
1. Settings
    - Fully functioning settings menu implemented via a boostrap modal component
    - Currently 8 supported settings that can be manipulated via various HTML input tags
    - Interacts with the SQL database in order to save each user's settings
    - Uses Javascript as well in order to get responses from form
2. Log History
    - Shows the user their login, logout, and register history, including the type of log and date
    - Uses SQLite as well
3. Analysis
    - TBA
4. Registration
    - User must register with a password that meets basic requirements
    - werkzeug.security module from Flask is used in order to hash the password so that it cannot be compromised
#### File Explanations:
0. Static Folder
    - Contains the script.js file with all the js I wrote, it also has all of the css in styles.css
    - There is also the audio folder, which contains all of the .wav files that I used for various sound effects
1. Template Folder
    - analysis.html
        - html file for analyzing past user performance, not yet implemented
    - history.html
        - this file tracks all of the user's login and logout times, in addition to registration time
    - index.html
        - this is the homepage, which has the pomodoro timer as its main feauture
    - layout.html
        - this is the layout file which uses jinja to avoid redundancies
    - login.html
        - file which displays the login interface
    - register.html
        - file for registration, contains instructions for user
    - settings.html
        - this is the file where the user changes their settings, uses a modal component from bootstrap
2. app.py
    - file containing all of the flask code, including get and post requests
3. helpers.py
    - contains all of the helper functions used in app.py
4. newapp.py
    - my initial attempt to convert from cs50's sqlite implementation, to sqlite3, will continue to work on this in the future
#### TODO:
1. Switch database api from cs50 to Flask-PyMongo
2. Implement Analysis page using num-py?
3. Add support for permanent background colour change
4. Figure out how to make volume slider dynamic
5. Add dark mode
6. Link it with my to-do list app, afaire
# selfquiz
SelfQuiz is a website that you can write down questions to yourself and return remember them later. 

## CS50 Final Project - SelfQuiz

The project is a webpage where users can save questions and answers called mementos. Then, they can create their own quizes selecting multiple questions or test themself with questions they saved before to freshen up their knowledge. Also, they can share their quizes with users online so other users can use their quizes to test themself and vise versa. 

### Technologies used:
JS
sqlite3
flask
html
css

### How the webpage works?
The idea is simple. The user can register then start saving mementos for s/he to return and remember. Also, user can test herself with quizes other users created. 

### Register
During registration you need to enter these fields:
  -Email
  -Phone Number
  -User Name
  -Name Surname
  -Password: it is checked to match, must be at least 6 symbols long and is hashed after checks are done
  -Checkbox for accept dummy terms and conditions. 

### Login
User can login to account with username and password. 

### Homepage
Left Side:
  Form to create questions. User must enter at least a question, an answer and a choice. User also can enter up to three choices. User also needs to identify type of the question.(For example, Python, C#, Flask, General etc.)
Right Side:
  Quick remember section which consist of maximum 10 random questions that user created before. If user did not saved a memento before, this section will have a note. "Save Mementos and come back!"

### Mementos
User can review all the questions saved by and create quizes with specific names by selecting questions. Also user can delete and edit questions saved before. 

### Remember
User can review all the quizes saved by, select a quiz to start that quiz or start a random quiz that consist of 10 random questions that saved by user before.
Users also can share quizes they created with other users in this section.

### Test Yourself
User can see all the public quizes shared by other users. 

### About
A quick text with developer information.

### Logout
User can logout from the page.

### Sessions
The webpage uses sessions to confirm that user is registered. 

### Database
sqlite3 database stores all users, questions, quizes, question types, shared quizes etch. 

### Possible improvements
As all applications this one can also be improved. Actually, this project is stopped due to high workload on other projects. 
This was my very first website other than I have created for CS50 Web homeworks. I have learnt a lot and I can learn more with possible improvements.

Possible improvements:
  -Ability to change account details
  -Like/Dislike public quizes
  -Filter quizes by popularity, date created, type etc.
  -Filter questions by type, date created
  -Disable questions so they don't appear on random quizes. 
  -Statistics that shows user's quiz result histories. 

### How to launch application
Clone the code: git clone https://github.com/RokasDie/cs50-final-project.git
Paste to https://ide.cs50.io/
Change directory to selfquiz and run "flask run"
You are ready to go!

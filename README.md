# MakersBnB

### Overview
We, as a team of 6 developers, had the task to create a web app, using python, to make an AirBnb style application. Where users are able to list "spaces" available to rent and book from available spaces. We worked towards the Agile Methodology with a timeframe of 3 days.

### Tech Stack:
* Python
  * Flask
  * Pytest
* PostgreSQL
* HTML
* CSS


## Planning

When planning our project, we decided as a team to initially design the database schema together before seperating further tasks into tickets (Using a Trello board). This helped our team to all be on the same page when it came to data handling further down in the project. We then decided and agreed on a minimum viable product (MVP) as well as nice to have features. After finishing our tickets, we then sorted them by priority and estimated the time needed for each ticket - to allow for a better breakdown of the timeline of the project. Finally, we visualised what our ideal version of our website and it's routes would look like (using Excallidraw).

Following the completion of the planning stage, we seperated into pairs and began allocating the first set of tickets.


## Setup

```shell
# Set up the virtual environment
; python -m venv makersbnb-venv

# Activate the virtual environment
; source makersbnb-venv/bin/activate 

# Install dependencies
(makersbnb-venv); pip install -r requirements.txt

# Install the virtual browser we will use for testing
(makersbnb-venv); playwright install
# If you have problems with the above, contact your coach

# Create a test and development database
(makersbnb-venv); createdb YOUR_PROJECT_NAME
(makersbnb-venv); createdb YOUR_PROJECT_NAME_TEST

# Open lib/database_connection.py and change the database names
(makersbnb-venv); open lib/database_connection.py

# Run the tests (with extra logging)
(makersbnb-venv); pytest -sv

# Run the app
(makersbnb-venv); python app.py

# Now visit http://localhost:5001/index in your browser
```

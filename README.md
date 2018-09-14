## Item Catelog Web App for Item-Catelog in the Udacity Full-Stack Nano-degree

- This web app is for Creating and Maintaining a list of authors and their books.

# Setup
- Download and install Vagrant.
- Download and install VirtualBox.
- Clone or download the Vagrant VM configuration file from https://github.com/udacity/fullstack-nanodegree-vm .
- Navigate to the above directory and navigate to the vagrant/ sub-directory
- Clone or download this repo to the vagrant folder
- In a terminal type 
    ```vagrant up
        vagrant ssh
    ```
- Run the following to setup the db
    ```python init_db.py
       python load_db.py
    ```
- Run the following to start the project
    ```python project.py
    ```
- Open your web browser to http://locallhost:5000
- Click the login button to login via Google.

        
## Features
- Full CRUD support using SQLAlchemy and Flask.
- Implements JSON endpoints.
- Third party authentication and authorization through Google Accounts.
- Formatted with PEP8 style.
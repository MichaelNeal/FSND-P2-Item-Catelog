# Udacity Full-Stack Nanodegree

## Project 2 - Item Catalog

## Project Purpose
Develop an application that provides a list of items within a variety of categories as well as provided a user registration and authentication system.

# Setup
- Download and install Vagrant.
- Download and install VirtualBox.
- Clone or download the Vagrant VM configuration file from https://github.com/udacity/fullstack-nanodegree-vm .
- Navigate to the above directory and navigate to the vagrant/ sub-directory
- Clone or download this repo to the vagrant folder
- In a terminal type 
    ```
		vagrant up
        vagrant ssh
    ```
- Run the following to setup the db
    ```
		python init_db.py
        python load_db.py
    ```
- Run the following to start the project
    ```
		python project.py
    ```
- Open your web browser to http://locallhost:5000
- Click the login button to login via Google.

        
## Features
- Full CRUD support using SQLAlchemy and Flask.
- Implements JSON endpoints.
- Third party authentication and authorization through Google Accounts.
- Formatted with PEP8 style.

## JSON Endpoints
- The json endpoints are:
http://localhost:5000/author/JSON
http://localhost:5000/author/<author_id>/booklist/JSON
http://localhost:5000/author/<author_id>/booklist/<book_id>/JSON



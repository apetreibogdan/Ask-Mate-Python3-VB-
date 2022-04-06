# Codecool Educational Project - ASK MATE
Web and SQL with Python / 1st and 2nd TW week / Ask Mate project




## Description
Small web project with a question and answer format. It is essentially an
 extremely simple Stack Overflow clone.  
## Main features:
- post questions, with question, detailed description and picture upload
- post answers to existing questions, with detailed descriptions and picture upload
- edit and delete both questions and answers
- sort the questions on the main page, ascending and descending, by date posted,
number of views, number of votes, question alphabetically and details alphabetically
- upvote or downvote questions and answers
- add/edit comments to questions and answers  
Note: Not all features are available at this time.

# Login
![Login](https://user-images.githubusercontent.com/70704260/161933787-65835ead-5166-481c-85a0-4878dc5be260.png)


# List all questions
![List all questions](https://user-images.githubusercontent.com/70704260/161929990-9f640b7c-52ac-4802-bec5-09af5a75f3c9.png)

# Search
![UnSeartch](https://user-images.githubusercontent.com/70704260/161933125-e973e7c8-8a64-4dcd-a618-02b7c04d2808.png)

# Display Answers and Comments
![Display answers and comments ](https://user-images.githubusercontent.com/70704260/161934685-fa061603-8453-420d-9ee7-0a707d2a365f.png)



## Installation
This installation guide is made for the Ubuntu operating system. Other operating 
systems have similar steps but please check the details on the web first. Also Python
3 is required and some operating systems don't have it by default.
1. Clone the project on your computer

        sudo apt-get update
        sudo apt-get install git
        git --version
        *navigate to the destination folder on your machine
        git clone 
        
2. Make sure you have pip3 installed for python

        pip3 --version

3. Install PostgreSQL

        sudo apt install postgresql postgresql-contrib

4. Conect to PostgreSQL

        sudo -i -u postgres

    and open a postgress promot using the command 

        psql

    create a new database
    
        CREATE DATABASE askmate3; 
        
    conect to database
    
        \c askmate3

    run sample askmatepart2-sample-data.sql

        \i <relative path to askmatepart2-sample-data.sql>

        
5. Install and activate the virtual environment in the git project folder (not 
where you run git clone)

        pip3 install virtualenv
        virtualenv venv
        source venv/bin/activate
        
6. Install all dependencys from requirements.txt

          pip3 install -r requirements.txt
        
6. Create  an  .env file in the root of the folder 

         export PSQL_USER_NAME= <add your postgress user name>
         export PSQL_PASSWORD= <add your postgress password>
         export PSQL_HOST=localhost
         export PSQL_DB_NAME=askmate3
        
7. Run the project on the given 0.0.0.0:5000 address

        python3 server.py
        
Note: You might be able to access the site from other devices on the same network. 
If you aren't able to, check your local network or server computer firewall and 
other security settings and run the server accordingly. 
## How to use
Pretty intuitive UI, just like any other question/answer forum/board.

# EpicMail2

[![Build Status](https://travis-ci.com/HabibSentongo/epicmail2.svg?branch=api)](https://travis-ci.com/HabibSentongo/epicmail2)      [![Maintainability](https://api.codeclimate.com/v1/badges/c808281d4382afa9f7ba/maintainability)](https://codeclimate.com/github/HabibSentongo/epicmail2/maintainability)        [![Coverage Status](https://coveralls.io/repos/github/HabibSentongo/epicmail2/badge.svg?branch=api)](https://coveralls.io/github/HabibSentongo/epicmail2?branch=api)

## Project Overview
The internet is increasingly becoming an integral part of lives. Ever since the invention of electronic mail by Ray Tomlinson, emails have grown to become the primary medium of exchanging information over the internet between two or more people, until the advent of Instant Messaging (IM) Apps.

As EPIC Andelans who work towards advancing human potential and giving back to the society, we wish to empower others by building a web app that helps people exchange messages/information over the internet.

# EpicMail2 API Endpoints
This project is about a set of API endpoints for the EpicMail app that the user interface interacts with and store user data and emails in memory using Data Structures.
## The Features Include:
* Sign-up a user.
* Login a user.
* Send an email.
* Get all recieved emails.
* Get all sent emails.
* Get all saved email drafts.
* Get all read emails.
* Get all unread emails.
* Get a specific email by ID.
* Delete an email by ID.

## Table of Contents
- [Project Description](#EpicMail2)
- [Project Planning](#project-planning)
- [Language and Tools used](#language-and-tools-used)
- [Installing](#installing)
- [Running the application](#running-the-application)
- [Unit Testing the app](#unit-testing-the-application)
- [Available Version](#url-versioning)
- [Deployed Version](#deployed-version)
- [API Documentation](#deployed-version)

## Project Planning
PivotalTracker was used for project Planning and Management. You can find this project's PivotalTracker Board [here](https://www.pivotaltracker.com/n/projects/2319053 "EpicMail2 on PivotalTracker")

## Language and Tools Used
### Tools used include:
* [Python 3.7](https://www.python.org)
* [Flask](http://flask.pocoo.org/)
* [Pip - A python package installer](https://pypi.org/project/pip/)
* [Virtualenv](https://pypi.org/project/virtualenv/)
* [Git](https://git-scm.com/downloads)
* [VSCode (IDE)](https://code.visualstudio.com/)
* [Open API](https://www.openapis.org/)
* [Swagger](https://swagger.io/)
* [Postman](https://www.getpostman.com/)
* [PivotalTracker](https://www.pivotaltracker.com "PivotalTracker")

## Installing

##### Cloning and Configuring the Project to Your Local Machine

- Step 1: Open the Terminal (or git bash, for windows) on the Directory/Folder where you want to place the project.
- Step 2: Then run this command 

    `git clone https://github.com/HabibSentongo/epicmail2.git`

    This copies the entire project onto your local machine. Confirm that the project name is “epicmail2”
- Navigate to the root folder of the project using the command below.

    `cd epicmail`

- Step 4: Change to the "develop" branch using the command below.

    `git checkout develop`

##### Setting Up the Virtual Environment
Inorder to set up the virtual environment, you need to install the python package called virtualenv using pip. Run the command below to install it.
- `pip install virtualenv` to install virtualenv
- `virtualenv venv`  to create a virtual environment named venv
- `. venv/scripts/activate` to activate the virtual environment.
- `. venv/scripts/deactivate` to deactivate the virtual environment when you need to.

### Installing Requirements
You need to install all the packages required by the project in the activated virtual environment. All these requirements are listed and stored in the requirements.txt file in the root folder of the project.
While in this folder, run the command below to install these requirements.
- `pip install -r requirements.txt`

With success of all the above steps, you have successfully cloned and configured the project to run on your local machine.

## Running the Application
To run this application, while in the root folder of the project via the Terminal or command prompt, run the command below:
- `py main.py`

On running that command, the application server will be launched and the URL to that server will be shown to you in the command-line/terminal.

## Unit Testing the Application

* Pytest has been used to test these API endpoints. To run unit tests for this application, you must install pytest, pytest-cov and coverage on your pc or in your virtual environment.
* While in the root directory of the project, run the command below to run the unit tests and also generate a coverage report.
- `pytest --cov`

## URL Versioning

The endpoints of this application have been versioned. The current version is one (1); i.e.: `api/v1`

## Deployed Version
### Heroku
Find the deployed API [here](https://epicmail-sentongo.herokuapp.com/ "epicmail2 on Heroku")

## API Documentation

The endpoints of this application have been well documented using Swagger Flasgger.
Find the API Documentation [here](https://epicmail-sentongo.herokuapp.com/apidocs/ "EpicMail API Docs")
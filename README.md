# Udacity's fsnd Item Catalog project!
A web application that provides a list of items within a variety of categories and integrate third party user registration and authentication.

## Project structure

directory  | Description
 ---- | -----------
`app` | Contains all the application initialization logic.
`auth` | App that handles user authentication and authorization.
`catalog` | App that handles the catalog CRUD logic.
`static` | contains the app stylesheets and JS scripts.
`templates` | contains the jinja2 templates.

## Usage  
#### Download and setup the VM:  
```
git clone https://github.com/udacity/fullstack-nanodegree-vm  
cd fullstack-nanodegree-vm/vagrant/  
vagrant up
vagrant ssh
# Now clone this repo
git clone https://github.com/HassenPy/udacity-fsnd-project-3
# Create the databases:  
psql -f commands.sql
```  

#### Create the facebook app:
You need to create a facebook app for the facebook login/signup to work:
1- Go to https://developers.facebook.com  
2- Add a new app  
3- Click on facebook login and choose setup.  
4- Choose the web option.  
5- For the domain option put: `http://localhost:8000/`  
6- now go to facebook login settings and add `http://localhost:8000/login` and `http://localhost:8000/` to the Valid OAuth redirect URIs" option and save.  
7- Make a file named `fb_app.json` that has this structure:  
`{
  "id": "your_app_id",
  "secret": "your_app_secret"
}`  

#### Running the app:
First you need to install the dependencies:  
`pip3 install -r requirements.txt`

Create an environment variable for the SECRET_KEY and FLASK_APP:  
`export SECRET_KEY='secret_key';`  
`export FLASK_APP='run.py';`  

Run the app:
`flask run -h 0.0.0.0 -p 8000`

[![Django CI](https://github.com/Kariss83/verbose-broccoli/actions/workflows/django.yml/badge.svg?branch=develop)](https://github.com/Kariss83/verbose-broccoli/actions/workflows/django.yml)
[![shields](https://img.shields.io/badge/coverage-95%25-green)](https://img.shields.io)
[![shields](https://img.shields.io/badge/uses-css-blue)](https://img.shields.io)
[![shields](https://img.shields.io/badge/uses-bootstrap-blue)](https://img.shields.io)
[![shields](https://img.shields.io/badge/uses-python-blue)](https://img.shields.io)
[![shields](https://img.shields.io/badge/uses-django-blue)](https://img.shields.io)
[![shields](https://img.shields.io/badge/uses-javascript-blue)](https://img.shields.io)
# verbose-broccoli
---
## Repo that hosts the code for GameZScan app
---
You can see live app @ : gamezscan.gitgudat.com

### How to install locally your project
This app have been designed to be used on mobile mainly, so the best way to navigate in it is to use
your favorite web browser inspector and simulate use on mobile.

**Prerequisites :**
- you need to have installed git, pipenv and postgresql on your machine.
- You also need to create a rapid-API account and an eBay account in order to get API keys. 
See the following links :
  - [eBay Dev](https://developer.ebay.com/)
  - [Rapid API](https://rapidapi.com)
  - More precisely for rapid API you'll need to get access token for [Product Lookup by UPC or EAN](https://rapidapi.com/go-upc-go-upc-default/api/product-lookup-by-upc-or-ean/)


(If you are on windows we suggest you run all these commands using WSL).


**In order to start run the app :**
1. Install libzbar0 : `sudo apt-get install libzbar0`
2. Install opencv for python : `sudo apt install python3-opencv`
3. Get your repo locally by running : `git clone https://github.com/Kariss83/verbose-broccoli.git`.
4. Install all dependencies using pipenv (previously installed using pip) : `pipenv install`
   If you want to participate in development you also have to install dev dependencies using : `pipenv install --dev`
5. Create a postgresql DB named `GameZScan` on you computer (alternatively you could use env variable for the DB name)
6. Set up your environnement variables in a .env file at the root of your project.
    - EBAY_KEY='*your_ebay_api_key*'
    - RAPIDAPI_KEY='*your_rapid_api_key*'
    - DB_USER='*your_db_user*'
    - DB_PWD='*users_db_pwd*'
    - DJANGO_KEY='*your_secret_django_key*' -- If you are not deploying it in production you can leave that blank
7. Inside `/datafetcher/oauthclient/` create a file named `ebay-config-sample.json` with the following structure :
`
{
    "api.sandbox.ebay.com" : {
                "appid" : "yoursandboxappid",
                "devid" : "yoursandboxdevid",
                "certid" : "yoursandboxcertid",
                "redirecturi" : ""
                },
    "api.ebay.com" : {
                    "appid" : "yourappid",
                    "devid" : "yourdevid",
                    "certid" : "yourcertid",
                    "redirecturi" : ""
                   }
}
`. All these info are available on the ebay developper hub.
7. Set the virtual environment by running : `pipenv shell`
8. Start the server using `python manage.py runserver` ou `python3 manage.py runserver` on Unix machines and `py manage.py runserver` on Windows machines.
9.  You can now go to the page http://127.0.0.1:8000 and have fun on your GameZScan app.
    - This app have been designed for a mobile usage so if you want the best experience plz use your browser dev console and fake usage with a mobile. Design for computer will be reworked in the coming realese.


### How to launch tests
1. If you want to just run the tests after you've initiated your virtual environment, you can run : `python manage.py test` on Unix machines and `py manage.py test` on Windows machines.
2. If you want something with a bit more verbosity and to check coverage.
    - you can create a file called 'coverage.sh' at the root of the project that contains the following:
    ```
    #!/bin/sh
    set -e  # Configure shell so that if one command fails, it exits
    coverage erase
    coverage run manage.py test --verbosity 2
    coverage report
    coverage html
    ```
    - make it executable using : `chmod +x coverage.sh`
    - run the command : `./coverage.sh`


### Linting with flake8
1. If you want to check code linting on your project you can run `flake8`
    - (optionnal) You can set up flake8 by creating a setup.cfg file with the following content :
    ```
    [flake8]
    exclude = accounts/migrations,home/migrations,products/migrations
    max-complexity = 10
    max-line-length = 119
    ```
2. For a nicer visual representation of that info you can run `flake8 --format=html --outputdir=flake-report` and open the html file that's in the flake-report directory.


### Technologies
- Python --> Django
- CSS --> Bootstrap
- JS

### Authors

Romain VACHE

---

TO DO dev - Version 0.2.0:
- [ ] Working on handling API bad return in case something break on their side
- [ ] Make a complete check of datastructures used (are all barcode strings for instance)
- [ ] Rework Database Models and check if the datastructure are coherent there
- [ ] Add functionnality the allows user to see all previously scanned games and let them add it to their collection without having to scan it themselves
- [ ] Web app design on non mobile browser
- [ ] Backing up security for file upload with NginX
- [ ] Add contact info on About and Legal Pages
- [x] Add a nice favicon
- [ ] Add a Button to allow camera flip for mobile users
- [ ] Switch all to Class Based Views

---

# sqlalchemy-challenge

Completed SQLAlchemy (week 10) homework for Monash University Data Analytics Boot Camp.

Homework task is to use SQLAlchemy to (i) explore the provided climate database, and (ii) design a Flask API that queries select information from the provided climate database.

Folder structure include - 
* **Resources** folder - contains sqlite database and csv files explored in this homework
* **climate_starter.ipynb** file - jupyter notebook to connect to and interrogate the sqlite database, and visualise the queries through pandas and matplotlib
    * queries include - 
        1. ***Precipitation Analysis*** - past 12 months precipitation data
        2. ***Station analysis*** - data from the most active weather station
        3. **Bonus analyses *Temperature & Rainfall Analyses*** - explore weather data during a proposed trip date
* **app.py** file - Flask API to query climate data from the dataset

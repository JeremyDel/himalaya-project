# Welcome to the Himalayan Expeditions Project

# General Information
The Himalayan Database is a compilation of records for all expeditions that have climbed in the Nepal Himalaya.
The database is based on the expedition archives of Elizabeth Hawley, a longtime journalist based in Kathmandu, and it is supplemented by information gathered from books, alpine journals and correspondence with Himalayan climbers.
Each expedition record contains detailed information including dates, routes, camps, use of supplemental oxygen, successes, deaths and accidents.

The Himalayan Database contains data over:
  * Year: 2004 - to date
  * Peaks: 450+
  * Expeditions: 10.000+
  * Members: 80.000+


# "Le Wagon" Project
**Data**

The data collection contains five files:
  * Peaks
  * Expeditions
  * Members
  * Weather
  * Peaks Coordinates

**Data Visualization**

The goal is to understand and visualize pattern.

**Machine Learning**

* Predict the member's ascension success (binary classification).
* Predict the number of summiters on the Everest (time-series).

**Web App**

The final goal is to set up the dashboard and the mahcine learning algorythm in a web app such as Flask or Streamlit.

# Resources
**Project Management**

https://trello.com/invite/b/B6UFlhf7/be72b5e325d221862dd493463272353e/le-wagon-project

**Himalayan Database Guide**

https://www.himalayandatabase.com/


# Startup the project
Clone the project and install it:
```bash
  $ git clone gitlab.com/{user}/himalaya-project
  $ cd ~/code/{user}/himalaya-project
  $ pip install -r requirements.txt
  $ make clean install test                # install and test
```
Functionnal test with a script:
```bash
  $ cd /tmp
  $ himalaya-project-run
```

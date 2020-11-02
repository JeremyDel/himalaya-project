# Data analysis
- Document here the project: himalaya-project

- Description: Machine learning project and data visualization

- Data Source:
Elizabeth Hawley (1923 – 2018) was an American journalist, author, and chronicler of Himalayan mountaineering expeditions.

Hawley's The Himalayan Database became the unofficial record for climbs in the Nepalese Himalaya.

The Himalayan Database contains data over:

  2004 - to date
  Peaks 450+
  Expeditions 10.000+
  Members 80.000+


- Type of analysis:
This project will focus on predicting the expeditions’ success based on our machine learning algorithm and predicting the number of summiters using time-series


# Stratup the project

The initial setup.

Create virtualenv and install the project:
```bash
  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
  $ make clean install test
```

Check for himalaya-project in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/himalaya-project`
- Then populate it:

```bash
  $ ##   e.g. if group is "{group}" and project_name is "himalaya-project"
  $ git remote add origin git@gitlab.com:{group}/himalaya-project.git
  $ git push -u origin master
  $ git push -u origin --tags
```

Functionnal test with a script:
```bash
  $ cd /tmp
  $ himalaya-project-run
```
# Install
Go to `gitlab.com/{JeremyDel}/himalaya-project` to see the project, manage issues,


Create a python3 virtualenv and activate it:
```bash
  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:
```bash
  $ git clone gitlab.com/{group}/himalaya-project
  $ cd himalaya-project
  $ pip install -r requirements.txt
  $ make clean install test                # install and test
```
Functionnal test with a script:
```bash
  $ cd /tmp
  $ himalaya-project-run
``` 

# Continus integration
## Github 
Every push of `master` branch will execute `.github/workflows/pythonpackages.yml` docker jobs.

## Gitlab
Every push of `master` branch will execute `.gitlab-ci.yml` docker jobs.

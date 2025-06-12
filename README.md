# [Eurobébé](https://github.com/johnncp/25su-DoC-Project-Team-Cool25)
by [Sophie Farrel](https://github.com/sophiefarrell), [Mia Giargiari](https://github.com/miagiargiari), [Emma Kulla](https://github.com/emmakulla), [John Nguyen](https://github.com/johnncp)

## About

This project was created throughout the course of Northeastern University's Data and Software in International Government and Politics Summer 2025 Dialouge of Civilizations. Our project is aimed towards exploring an alarming trend, falling birth rates. In 2023, the European Union saw its largest decline in birth rate since 1961. Given this trend, we seek to understand how a nations average weekly working hours, as well as parental and family oriented benefits and expenditures. Our project seeks to analyze what policy frameworks support the success of EU politicians, parents, and business owners. 

## To build this project follow the steps below

- `git clone 'https://github.com/johnncp/Eurobébé`
- rename the `.env.template` file in api\ to `.env` and change the placeholder in the file
- Then run the following docker commands in the root directory for this project:
    - `docker build`
    - `docker compose up -d`
- Finally, open up `localhost:8501` in your browser!

## Uses
After opening the app, the user can enter as three different personas. The first being Cara Day, an owner of a daycare franchise in the EU. Once logged in, Cara can use the app to predict the best nation to expand her business too. Cara may also manage her branches by viewing different features of her daycares such as enrollment rates and budgeting fluctuations, all while making her daycares more visible to expecting parents.

Another persona in our app is Eura Pean, an expecting parent living in the European Union. Eura can use the app to predict the country she should move too based off of what benefits she values most, she can also research nearby daycares, and parental affinity groups in her area.

Lastly, one can enter as Paul E. Tishan, a politician residing in the EU. Paul can use the app to predict the birth rate for his country to get a better sense as to what the future of his nation looks like. Paul can also view predictions for all European Union countries, as well as past legislatin that may have played a role in the trends he views. 

## Structure
Below is the general structure of the project. The `api` directory contains the majority of the routes connecting each component of the various Docker containers. Within the  `api/backend/ml_models` directory, you can find the backend renferences for the main logic of the two machine learning models. 

From the `app` directory, one can find the main contents of the front end. The `app\src\pages` folder contains each of the pages a user can interact with. Inside of the `pages` folder, one can see each of the pages labeled with the first two digits of each page representing its location within the app. For example, all of the pages a user acting as Anton can view begin with `0X`. 

Finally, the other main component of the project structure is the `database` folder which contains all of the information allowing for users to interact with articles and training data for the two machine learning models, amongst other features.

```
└───Eurobébé
    ├───api
    │   └───backend
    │       ├───affinity_groups
    │       ├───api_calls
    │       ├───benefits_expenditure
    │       ├───customers
    │       ├───daycare
    │       ├───daycare_data
    │       ├───daycare_locations
    │       ├───db_connection
    │       ├───employment_hours
    │       ├───ml_models
    │       ├───model2
    │       ├───ngos
    
    ├───app
    │   └───src
    │       ├───assets
    │       ├───modules
    │       └───pages
    ├───database
    └───fake_data
```

## Improvements To Make & Current Limitations
For future iterations of this app, there can be improvements upon the validity and accuracy of the predictive model which can be improved through more extensive training/feature use. Other improvements may involve including data on safety indexes of nations, or average wages, which may play a significant role in the declining birth rates.

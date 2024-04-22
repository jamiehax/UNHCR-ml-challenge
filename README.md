# UNHCR-ml-challenge
Code repository for the UNHCR's Artificial Intelligence for Operation Support to the Forcible Displaced Challenge.

## Notes on Data
Population movement data is only available starting in 2015, so all other data scraped starts then too. Nutrition data is not avilable until 2016, so 2015 CSVs are empty. Flood Data stops at 2021, so no data scraped for after that.

## Abstract
Our problem addresses the humanitarian crisis in Somalia related to refugee movements and forcibly displaced people. The ability to accurately predict patterns in forcibly displaced peoples movements is crucial to the development of public policies that provide aid and resources to refugees. We plan to focus on building a model trained on GIS data covering Somalia’s environment, economy, and stability provided by UNHCR. By looking at a variety of conditions affecting human movement, we seek to predict where people might move, either forcibly or voluntarily.bA successful model will be able to accurately predict where people are moving from due to a variety of factors like instability, drought, or economics. 

## Motivation and Question
We are curious about how certain environmental factors like drought or vegetation affect human movement. UNHCR’s extensive dataset allows us to answer this question due to its NDVI (normalized difference vegetation index) allows us to effectively investigate these questions. Ultimately, the model could help inform UN operations where people might be displaced and where people might move to. This information allows humanitarian efforts to effectively reach refugees by helping organizations plan their relief efforts based on the predicted change in the number of displaced people in a particular area.

## Planned Deliverables
We will develop a trained model, in the form of a Python package, that will predict forcibly displaced persons movement using GIS data. This package will contain the model class itself and all of the methods related to training the model and running inferences with the model. We will additionally create a Jupyter notebook to illustrate patterns in the data and demonstrate model predictions. If everything works out, we will deliver the trained model and a notebook demonstrating its accuracy and effectiveness. A partial success would be still delivering a trained model, but just one that is not as effective or accurate as we may have hoped. 

### Written Deliverables
You’ll also write a blog post on your project; you don’t have to discuss this post in your proposal though.

## Resources Required
The most important resource we will need for this project is good data. We plan to use GIS datasets from the [UNHCR’s operation data portal](https://data.unhcr.org/en/geoservices/). There are many different datasets available that we may incorporate, but we will probably use the Population Reference Points and Populations Reference Areas datasets, among others. While we are not set on the model we will use, it is unlikely to be a deep-learning model, therefore access to compute resources will likely not be needed. If they are, however, I (Jamie) already have access to ada, so we can run some training on there if needed.

## What You Will Learn
**Mihir:** I decided to focus on the implementation of machine learning algorithms as well as machine learning’s social impact. This project allows me to work on implementing machine learning algorithms designed to take in GIS data as well as also focus on developing a data pipeline that effectively cleans the data since much of what is collected cannot just be fit neatly into a machine learning model. Meanwhile, I also said I was interested in how machine learning can be used for a positive social impact. This project will allow me to consider how that may be true as well as consider important ethical questions related to the application of machine learning for humanitarian causes.

**Jamie:** A lot of the goals I set for myself at the beginning of the semester were focused on improving my theoretical understanding of machine learning models, which this project does not focus much on. That said, I think I have developed that understanding a lot in other aspects of the course, and for this project I am interested in developing better practical skills related to model implementation. By doing so, I hope learn about the practical aspects of implementing a model on real world data, especially as it relates to cleaning data and evaluating the model.

**Jake:** I set out to challenge myself to learn more of the theory of machine learning—the frameworks and math behind a lot of our models. I hope this project is a way for me to lean into that challenge as applied to an interesting topic. Given the scope of the topic as well, I want to think about the social responsibility of making these models. I think our topic in dealing with displaced peoples is extremely interesting, but it brings up interesting ethical questions about making models and drawing conclusions that can potentially be harmful or affirm biases.

## Risk Statement
While we have done some preliminary research into the datasets and are confident that we will be able to find useful and relevant features for predicting refugee movement, there is a risk that the data will not be predictively useful. Another issue is given that there is a lot of data and it may not be as useful as we first imagined, we might not achieve conclusive predictions by the end of the project.

## Ethics Statement
Our project has the potential to benefit refugees and forcibly displaced persons in Somalia by highlighting areas that need more resources. Unfortunately, resources are not infinite, and giving more resources to one area may mean less resources to another, potentially harming some people. Under the assumptions that our project is accurate, unbiased, and that better direction of resources will ease the humanitarian crisis in Somalia, our project would make the world a better place. Depending on the data we use to train the model, algorithmic bias could definitely be an issue we need to address. Specifically, our model might bias towards predicting the movements of refugees to common areas, discriminating against less common migration patterns.

## Tentative Timeline:
At the end of week 9, we plan on having our data pipeline setup such that we can fill data into the model and do some basic analysis looking at how one feature (maybe flooding) affects human movement. Finally after working on the project for six weeks, we hope to have set up a model that can accurately predict displacement given a set of information about the land of a region. For example, given the vegetation index, flood risk, drought risk, HDI, and so on, how many people might leave some specific region or go to a specific region. 

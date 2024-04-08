# UNHCR-ml-challenge
Code repository for the UNHCR's Artificial Intelligence for Operation Support to the Forcible Displaced Challenge.

## Abstract
Our problem addresses the humanitarian crisis in Somalia related to refugee movements and forcibly displaced people. The ability to accurately predict patterns in forcibly displaced peoples movements is crucial to the development of public policies that provide aid and resources to refugees. We plan to focus on building a model trained on GIS data covering Somalia’s environment, economy, and stability provided by UNHCR. By looking at a variety of conditions affecting human movement, we seek to predict where people might move, either forcibly or voluntarily.bA successful model will be able to accurately predict where people are moving from due to a variety of factors like instability, drought, or economics. 

## Motivation and Question
We are curious about how certain environmental factors like drought or vegetation affect human movement. UNHCR’s extensive dataset allows us to answer this question due to its NDVI (normalized difference vegetation index) allows us to effectively investigate these questions. Ultimately, the model could help inform UN operations where people might be displaced and where people might move to. This information allows humanitarian efforts to effectively reach refugees by helping organizations plan their relief efforts based on the predicted change in the number of displaced people in a particular area.

## Planned Deliverables
Concisely state what you are aiming to create and what capabilities it will have. For most projects, I would expect the deliverable to include:

- A Python package containing all code used for algorithms and analysis, including documentation.
- At least one Jupyter notebook illustrating the use of the package to analyze data.
However, your specific idea might imply different deliverables (e.g. an essay). Consult with me if you’re not sure.

You should describe what your deliverable will be able to do and how you will evaluate its effectiveness. **Please consider two scenarios:**

- “Full success.” What will your deliverable be if everything works out for you exactly as you plan?
- “Partial success.” What useful deliverable will you be able to offer even if things don’t 100% work out? For example, maybe you aren’t able to get that webapp together, but you can still create a code repository that showcases the machine learning pipeline needed to use to support the app. Have a contingency plan!

### Written Deliverables
You’ll also write a blog post on your project; you don’t have to discuss this post in your proposal though.

## Resources Required
What resources do you need in order to complete your project? Data? Computing power? An account with a specific service?

Please pay special attention to the question of **data**. If your project idea involves data, include at **least one link** to a data set you can use. If you can’t find data for your original idea, that’s ok! Think of something related to your group’s interests for which you can find data.

Most projects should involve data in some way, but certain projects may not require data. Ask me if you’re not sure.

## What You Will Learn
Each group member should return to their stated goals from the [reflective goal-setting assignment](https://middlebury-csci-0451.github.io/CSCI-0451-s24/assignments/process/goal-setting.html) at the beginning of the course. Then, in this section, please state what each group member intends to learn through working on the project, **relating your intentions to your stated goals**. You might be thinking of certain algorithms, software packages, version control, project management, effective teamwork, etc.

## Risk Statement
What are two things that could potentially stop you from achieving the full deliverable above? Maybe it turns out that the pattern you thought would be present in the data just doesn’t exist? Or maybe your idea requires more computational power than is available to you? What particular risks might be applicable for your project?

## Ethics Statement
All projects we undertake involve decisions about whose interests matter; which problems are important; and which tradeoffs are considered acceptable. Take some time to reflect on the potential impacts of your project on its prospective users and the broader world. Address the following questions:

1. What groups of people have the potential to **benefit** from our project?
2. What groups of people have the potential to be **excluded from benefit** or even **harmed** from our project?
3. Will the world become an **overall better place** because we made our project? Describe at least 2 **assumptions** behind your answer. For example, if your project aims to make it easier to predict crime, your assumptions might include:
  - Criminal activity is predictable based on other features of a person or location.
  - The world is a better place when police are able to perform their roles more efficiently.

If your project involves making decisions or recommendations, then you will also need to consider possible forms of algorithmic bias in your work. Here are some relevant examples:

A recipe recommendation app can privilege the cuisines of some locales over others. Will your user search recipes by ingredients? Peanut butter and tomato might seem an odd combination in the context of European cuisine, but is common in many traditional dishes of the African diaspora. A similar set of questions applies to recommendation systems related to style or beauty.
A sentiment analyzer must be trained on specific languages. What languages will be included? Will diverse dialects be included, or only the “standard” version of the target language? Who would be excluded by such a choice, and how will you communicate about your limitations?

## Tentative Timeline
We will have a checkpoint for the project in Week 9 or 10, and then final presentations in Week 12. With this in mind, please describe what you expect to achieve after **three** and **six**. Your goal by the three-week check-in should be to have “something that works.” For example, maybe in three weeks you’ll ready to demonstrate the data acquisition pipeline and show some exploratory analysis, and in the last couple weeks you’ll actually implement your machine learning models.

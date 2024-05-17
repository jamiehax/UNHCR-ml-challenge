# UNHCR-ml-challenge
### Jamie Hackney, Mihir Singh, Jake Gilbert
Code repository for our work on the UNHCR's Artificial Intelligence for Operation Support to the Forcible Displaced Challenge.

## Abstract
This project seeks to develop, implement, and evaluate various machine learning models to accurately predict refugee population movements in Somalia as part of the United Nations Commissioner for Refugees (UNHCR) Machine Learning Challenge. The data used by our models' was collected by the UNHCR between 2015 and 2024 in Somalia. It contains information on population movements, markets, health, conflicts, and climate. We developed a web scraper to collect this data and combine it all into a single dataframe. To deal with missing data values, we created two datasets, one by dropping the missing values and the other by imputing them. Then, we built a Logistic Regression, Decision Tree, and Random Forest model on different subsets of these two datasets. We tested these models to see how accurately they could predict the number of refugee arrivals into a specific district in Somalia by computing the root mean squared error (RMSE), framing it as a regression problem. We found that the models had, on average, very high root mean squared errors (indicating a poor fit on the data), yet also had high R2 values (indicating a good fit on the data). We believe this discrepancy is explained by the fact that there are several very large outliers present in the data. To validate this, we binned the predictions into the three severity levels proposed by the UN, and treated it as a classification problem. When doing so, our best model, a Decision Tree Regressor trained on a subset of the dataset where missing features were dropped, achieved an accuracy of 99.5%. This model was also able to perfectly predict the exact number of arrivals 98% of the time, further supporting our hypothesis that these models fit the data very well and the high RMSE is explained by the existence of several large outliers.

## Values Statement
The intended users of our project are the Somalian government and other NGOs that support refugees in the area. However, our project deals directly with people, as we are predicting where we expect refugees to move in Somalia. Because of this, the entire population of refugees in Somalia could potentially be affected by our project, if it were to be used by any of these agencies or governments to inform resource allocations. Both refugees in Somalia and the groups that support these refugees stand to benefit from our project, assuming the models are an effective tool. If this is the case, then these agencies can better allocate resources, which will benefit the refugees themselves as they will have access to more resources. Additionally, the government and agencies supporting them will benefit from more efficient resource movement. Conversely, if our models prove to be inaccurate enough that they cause resources to be misallocated, both refugees and the groups supporting them could be seriously harmed. Additionally, we note the possibility that bad actors could co-opt these models to predict refugee movements for malicious purposes.

We chose to work on this project because we were interested in the intersection between machine learning and public policy. When we found the UN challenge related to this project, we became very interested in the cause of this project, and found the ability to help refugees and their support groups compelling. Assuming that our models are an effective tool for helping agencies allocate resources for refugees, we believe that the benefits to refugee populations and their support groups will bring some relief to that region.
Introduction
Our program addresses the humanitarian crisis in Somalia related to refugee movements and forcibly displaced people. The ability to accurately predict patterns in forcibly displaced peoples movements is crucial to the development of public policies that provide aid and resources to refugees. This is not a novel problem, and in fact has been approached several times before. Suleimenova et al., Gulden et al., and Lin et al. all developed agent based models to predict population movements. Gleick investigated the relationship between water and conflict in Syria, drawing a connection between water scarcity and conflicts, which in turn can drive population movements. Finally, Finnley noted an increase in migration of women and children during the severe drought of 1983-1985. 

We focused on building models trained on a variety of data, including climate, conflicts, and market prices. By looking at a variety of conditions affecting human movement, we predict the movement patterns of displaced people in Somalia. The goal of this project is to effectively predict these population movements so that agencies supporting refugee populations in this area can better allocate resources to regions that are expected to receive a high number of migrants.

## Materials and Methods
### Our data
All of our data came from the Food Security and Nutrition Analysis Unit Dashboard for Somalia (FSNAU). This organization collects data related to food and security in Somalia. FSNAU provides access to this data through a public facing dashboard. Users can select what data they would like to look at and which time frames (in six month increments).

For our data, focused on creating two datasets, one where we drop missing values and one where we impute them. Within these datasets, we further split them into all available features, and just the top nine features as recommended by the UNHCR in their previous work with this data (project Jetson). Due to data availability, we focused on data from 2015 - 2024. Additionally, flood data is missing on the dashboard after 2021, so we did not use that in our analysis.

### Our Approach
The goal of our models was to predict the number of refugees arriving in a certain district in Somalia. We used the “Arrivals” column of our data as the target feature for our models to predict. For training features, we either trained our models on all features available on the FSNAU dashboard, or the nine features recommended by the UNHCR (region, district, month, year, rainfall, number of conflict fatalities, number of conflict incidents, water price, and goat price). We chose to run models trained on these nine features because the UN found these particularly helpful when building their own machine learning models (Jetson Data). For all models, we dropped the feature describing the number of departures because such data can only be collected after the fact. That is, at the time this model would be run in a “real” scenario, there would be no way of knowing the number of departures in a district for the entire month; a month must first pass for this data to become known. Finally, we split the data into train and test groups, with 80% of the data in the train split and 20% of the data in the test split. Depending on the dataset used, the exact number of rows varied, but for the dataset we found to be best (dropping missing values and only using the nine best features), we had 51,812 train rows and 12,953 test rows.

We trained a Linear Regression model, Decision Tree Regressor, and Random Forest Regressor model from Sci-Kit Learn to make our predictions. These models were chosen because predicting the number of refugees arriving is a regression problem, where we want our model to give us an estimate of the number of arrivals in a district. We trained each model on the four datasets we created: drop missing values and use all features, drop missing values and use only the best nine features, impute missing values and use all features, and impute missing values and use only the nine best features. The reason for choosing to both impute and drop missing values is to determine the best approach to deal with these missing values, of which there were many. In fact, out of the 328,856 available rows, only 230 had no missing values. A single missing value in any one feature can render the entire row obsolete in training or testing. The benefit of imputing the data is that we end up with much more data to train and test with, potentially increasing accuracy and decreasing the possibility of overfitting. The drawback is that the data is generally lower quality, as many values are estimates not actual observations. Dropping missing values, on the other hand, leads to a smaller dataset, potentially decreasing accuracy and increasing the possibility of overfitting. The data we are left with, however, is much higher quality since it is composed entirely of actual observations.

The four datasets that result from this process, as well as their sizes are below:

- `df_dropna` includes all rows without a single Na or NaN in any feature.
  - train size: 230 x 23
  - test size: 55 x 23

- `df_dropna_t9` includes all rows without a single Na or NaN in any of the top nine features. 
  - train size: 51,812 x 10
  - test size: 12,953 x 10

- `df_impute` includes all rows and features and fills in missing values by estimating their value using SciKitLearn’s SimpleImputer. 
  - train size: 263084 x 23
  - test size: 65,772 x 23

- `df_impute_t9`  includes all rows and only the best nine features, and fills in missing values by estimating their value using SciKitLearn’s SimpleImputer. 
  - train size: 263084 x 10
  - test size: 65,772 x 10

The disadvantage of imputing the data can be seen in the fact that it produces negative values in the “Arrivals” column, which is impossible.

We then evaluated each of the models on each data set using R<sup>2</sup>, RMSE, and the classification accuracy for the three alarm levels. This classification accuracy came from binning the predictions into one of the three population movement alarm levels set by FSNAU (alarm levels) and calculating the percent of times the model predicted the correct alarm level. The reason we included this metric is because the dataset contained several large outliers that heavily skewed the RMSE, which we will go into more at the end of this section. Additionally, we figured that in a real world scenario, it is more likely the aid groups would care more about whether the incoming number of migrants is low, medium, or high, rather than an exact number. 

## Results
We evaluate the models using three different metrics, R<sup>2</sup>, RMSE, and the alarm level classification accuracy. The R<sup>2</sup> value measures how well the model explains the observed data values. RMSE measures the average error for a prediction, with the interpretation being that the RMSE value is the average number of people the predictions are off by. Finally, the classification accuracy measures how often the models correctly predict the alarm level. In other words, the classification accuracy is how often the models can correctly predict whether the arrivals will be less than 1000 people, between 1000 and 5000 people, or greater than 5000 people. The tables below show the model performances when evaluated with each of these metrics on the testing data.

### Linear Regression Model

<table>
<thead>
<tr>
<th align="center"></th>
<th align="center">df_dropna</th>
<th align="center">df_dropna_t9</th>
<th align="center">df_impute</th>
<th align="center">df_impute_t9</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">R<sup>2</sup></td>
<td align="left">0.0</td>
<td align="left">0.020</td>
<td align="left">0.333</td>
<td align="left">0.100</td>
</tr>
<tr>
<td align="left">RMSE</td>
<td align="left">1.099 x 10<sup>-7</sup></td>
<td align="left">6309.552</td>
<td align="left">3423.200</td>
<td align="left">3899.569</td>
</tr>
<tr>
<td align="left">Classification</td>
<td align="left">1.0</td>
<td align="left">0.476</td>
<td align="left">0.678</td>
<td align="left">0.680</td>
</tr>
</tbody>
</table>

### Decision Tree

<table>
<thead>
<tr>
<th align="center"></th>
<th align="center">df_dropna</th>
<th align="center">df_dropna_t9</th>
<th align="center">df_impute</th>
<th align="center">df_impute_t9</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">R<sup>2</sup></td>
<td align="left">0.0999</td>
<td align="left">0.946</td>
<td align="left">0.937</td>
<td align="left">0.824</td>
</tr>
<tr>
<td align="left">RMSE</td>
<td align="left">9024.153</td>
<td align="left">1360.971</td>
<td align="left">1090.005</td>
<td align="left">1780.976</td>
</tr>
<tr>
<td align="left">Classification</td>
<td align="left">0.927</td>
<td align="left">0.994</td>
<td align="left">0.863</td>
<td align="left">0.865</td>
</tr>
</tbody>
</table>


### Random Forest

<table>
<thead>
<tr>
<th align="center"></th>
<th align="center">df_dropna</th>
<th align="center">df_dropna_t9</th>
<th align="center">df_impute</th>
<th align="center">df_impute_t9</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">R<sup>2</sup></td>
<td align="left">-2.534</td>
<td align="left">0.936</td>
<td align="left">0.965</td>
<td align="left">0.916/td>
</tr>
<tr>
<td align="left">RMSE</td>
<td align="left">3217.263</td>
<td align="left">1506.199</td>
<td align="left">784.980</td>
<td align="left">1308.188</td>
</tr>
<tr>
<td align="left">Classification</td>
<td align="left">1.0</td>
<td align="left">0.991</td>
<td align="left">0.864</td>
<td align="left">0.863</td>
</tr>
</tbody>
</table>


### Dataset Outliers
The dataset contained several large outliers for our target column (“Arrivals”) that were throwing off the RMSE calculations. The 90th percentile of arrivals was 1,677; in other words 90% of arrivales were 1,677 or fewer people. However, the maximum number of arrivals for a single observation was 259,678. This implies the existence of some large outliers in the dataset that skew the RMSE calculation, making the models seem to perform worse than they actually do.

## Conclusion
After testing each model on each dataset, we found the following models scored the highest for each metric:

<table>
<thead>
<tr>
<th align="center">Metric</th>
<th align="center">Best Model</th>
<th align="center">Value</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">R<sup>2</sup></td>
<td align="left">Decision Tree on df_dropna_t9</td>
<td align="left">0.946</td>
</tr>
<tr>
<td align="left">RMSE</td>
<td align="left">Decision Tree on df_dropna_t9</td>
<td align="left">1360.970</td>
</tr>
<tr>
<td align="left">Classification</td>
<td align="left">Decision Tree on df_dropna_t9</td>
<td align="left">0.994</td>
</tr>
</tbody>
</table>

Given that df_impute contains negative values, which are impossible in the real scenario, and df_dropna has only 230 training rows, making the possibility of overfitting high, we believe that neither of these models would give helpful predictions. Instead, we think that a Decision Tree trained on df_dropna_t9 would be the most useful in a real world scenario, as it would not predict negative values, is sufficiently large that overfitting is less of a worry, and still scores high. This model's scores are given below:

<table>
<thead>
<tr>
<th align="center">Metric</th>
<th align="center">Best Model</th>
<th align="center">Value</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">R<sup>2</sup></td>
<td align="left">Decision Tree on `df_dropna_t9`</td>
<td align="left"></td>
</tr>
<tr>
<td align="left">RMSE</td>
<td align="left">Decision Tree on `df_dropna_t9`</td>
<td align="left"></td>
</tr>
<tr>
<td align="left">Classification</td>
<td align="left">Decision Tree on `df_dropna_t9`</td>
<td align="left"></td>
</tr>
</tbody>
</table>


Our best model performs exceptionally well on the vast majority of predictions, perfectly predicting the exact number of arrivals 98% of the time. That said, it performs very poorly when trying to predict these large outliers, which is reflected in the high RMSE. If these observations are anomalies in the dataset that we would not reasonably expect to correctly predict given the data available, in other words, caused by some external factor not present in the data (such as a government ordering the evacuation of an area), then this error is not a huge issue. If, on the other hand, these observations are largely explained by the data we have available, then we would want to do better at predicting them. One way we could do this is to try to incentivize our model to be less conservative and make larger predictions. Without knowing more about these specific observations, it is hard to say which is the best course of action.

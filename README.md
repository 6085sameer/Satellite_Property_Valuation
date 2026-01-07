##Satellite Imagery-Based Property Valuation



This project predicts residential property prices by combining structured housing data with satellite imagery. 

The objective is to study whether visual context from satellite images can add useful information to traditional 

tabular price prediction models.



The project implements a multimodal regression pipeline that integrates numerical housing attributes with 

image-based features extracted using a convolutional neural network.





##Overview



The goal of this project is to estimate property market value using both tabular housing attributes and 

satellite imagery. Traditional features such as property size, location, and construction quality are used 

alongside image-based features to capture neighborhood context.



Satellite images are programmatically fetched using latitude and longitude coordinates from the dataset. 

Due to cloud cover and API limitations, only a subset of properties have usable satellite images. 

The project therefore focuses on building and evaluating a complete multimodal pipeline rather than 

maximizing image-based performance.





##Dataset



###Tabular Data



train(1).xlsx  

Training dataset containing property features and target price.



test2.xlsx  

Test dataset without price labels.



###Key features include:

\- Bedrooms and bathrooms

\- Living area and lot size

\- Latitude and longitude

\- Construction grade and condition

\- View rating and waterfront indicator





##Generated Files



X\_clean.csv  

Cleaned tabular training features.



X\_test\_clean.csv  

Cleaned tabular test features.



y.csv  

Target price values.



images/  

Satellite images downloaded programmatically using the Sentinel Hub API.



Due to file size constraints, the full satellite image dataset is not uploaded to the repository.





##Methodology



1\. Data Preprocessing  

The raw housing dataset is cleaned and relevant numerical features are selected. Missing values are handled 

and features are prepared for model training.



2\. Satellite Image Acquisition  

Satellite images are fetched using latitude and longitude coordinates. A cloud cover threshold is applied, 

resulting in a reduced set of valid images.



3\. Feature Extraction  

A pretrained ResNet18 model is used to extract image embeddings from satellite images. The final classification 

layer is removed, and the resulting feature vectors represent visual context.



4\. Model Training  

Two models are trained:

\- A baseline Random Forest regressor using only tabular features.

\- A multimodal Random Forest regressor using concatenated tabular and image features.



5\. Evaluation  

Model performance is evaluated using RMSE and R² score on a validation split.





##Results Summary



###Tabular-only Model:

\- RMSE: 130,112

\- R² score: 0.865



###Multimodal Model (Tabular + Satellite Images):

\- RMSE: 194,147

\- R² score: 0.793



Although satellite imagery provides additional contextual information, the reduced number of valid images 

and visual noise limit performance improvement in this implementation.





##Project Structure



data/

\- train(1).xlsx

\- test2.xlsx

\- X\_clean.csv

\- X\_test\_clean.csv

\- y.csv



images/

\- Downloaded satellite image tiles (subset after cloud filtering)



notebooks/

\- preprocessing.ipynb		Data cleaning and feature preparation

\- model\_training.ipynb		Model training and evaluation

\- image\_index.csv		Mapping of properties with valid satellite images



data\_fetcher.py  

Script used to download satellite images.



README.md  

Project documentation.





##Notes



This project focuses on demonstrating a complete multimodal learning pipeline rather than achieving 

maximum prediction accuracy. All code and analysis were implemented as part of this project.





##Submission Details



Enrollment Number: 24548005

Prediction File: 24548005\_final.csv

Report File: 24548005\_report.pdf

Repository: Public GitHub repository







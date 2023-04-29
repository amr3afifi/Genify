
# GENIFY RESTAPI

## Files Structure
*Directories:
 -datasets : contians training,testing,model_results CSVs

*Files:
 -app.py : Main Flask file
 -docker-compose.yml : docker files to prepare env and build image and run container
 -requirements.txt : txt file with libraries needed to prepare env
 -api-tests.rest : API testing examples
 -Dockerfile : docker files to prepare env and build image and run container
 -generate_model.py : python file to train and export the model into a pickle file
 -model.pkl : the exported model
 -playground.ipynb : jupyter notebook to train data and test my own machine learing model

## Overview
Build a REST API around a machine learning model that recommends banking products. It is based on a solution to a Kaggle competition [1]: the model is already engineered for you (notebook [3]), you just need to run the training script to obtain the trained model, and then your work focuses on building from scratch an API that serves this model. Some bonus tasks to further test your API design and devops skills are also included.

## Context on the problem
What this model solves relates to a sub-product of Genify. It helps banks recommend the right banking product (loan, deposit, credit card, etc.) to the right client at the right time. How these recommendations are delivered is equally important. Here, to do so, we opt for a REST API, and your task is to build it!

## HOW TO RUN?
docker compose up
(Now you are container is built and running local on port 5000 by default as initiated in docker)

## HOW TO TEST THE APIs?
You can find a file called api-rest.rest filled with some requests' examples that you can click on send request to try

## References
[1] overview of problem (Kaggle competition): [https://www.kaggle.com/c/santander-product-recommendation/overview](https://www.kaggle.com/c/santander-product-recommendation/overview)

[2] data (Kaggle competition): [https://www.kaggle.com/c/santander-product-recommendation/data](https://www.kaggle.com/c/santander-product-recommendation/data)

[3] reference Kaggle notebook: [https://www.kaggle.com/sudalairajkumar/when-less-is-more](https://www.kaggle.com/sudalairajkumar/when-less-is-more)

[4] details on ref. code: [https://www.kaggle.com/c/santander-product-recommendation/discussion/25579](https://www.kaggle.com/c/santander-product-recommendation/discussion/25579)

[5] Genify recommender system demo: [https://web.archive.org/web/20220524164933/https://jpweng.pythonanywhere.com/en/recosysdemo](https://web.archive.org/web/20220524164933/https://jpweng.pythonanywhere.com/en/recosysdemo)

[6] Genify PFM API: [https://docs.pfm.genify.ai/pfm-suite/v1/transaction-data-api](https://docs.pfm.genify.ai/pfm-suite/v1/transaction-data-api)


## Demo Video Link uploaded on google drive
[Demo](https://drive.google.com/drive/folders/1-wMP3WnJlio7iuRSaKDvEN9UnR3HwV-S?usp=sharing)

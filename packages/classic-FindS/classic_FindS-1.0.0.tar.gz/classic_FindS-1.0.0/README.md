Find-S Algorithm
===================


Find-S algorithm is a Machine Learning Algorithm that finds the most specific hypothesis that fits all the positive examples.

----------

Installation
-------------
Install directly from my [PyPi](https://pypi.org/project/classic-FindS/)

> pip install classic-FindS

Or Clone the [Repository](https://github.com/safir72347/ML-FindS-PyPi) and install

> python3 setup.py install

Parameters
-------------

## * X_train 
-------------
The Training Set array consisting of Features.

## * y_train
-------------
The Training Set array consisting of Outcome.


Attributes
-------------

## * fit(X_train, y_train)
-------------
Fit the Training Set to the model.

## * predict(y_test)
-------------
Predict the Test Set Results.



<i class="icon-file"></i> Documentation
-------------

### 1.  Install the package
>  pip install classic_FindS

### 2. Import the library
>  from classic_FindS import FindS

### 3. Create an object for FindS class
> fs = FindS()

### 4. Fit your Training Set to the model
> fs.fit(X_train, y_train)

### 5. Predict your Test Set results
> y_pred = fs.predict(y_test)

----------



Example Code
-------------

### 1. Import the dataset and Preprocess
> * import numpy as np
> * import pandas as pd
> * dataset = pd.read_csv('Covid-19_Data.csv')
> * result = {'Yes':1, 'No':0}
> * dataset['Covid_19'] = dataset['Covid_19'].map(result)
> * X = dataset.iloc[:, 0:5].values
> * y = dataset.iloc[:, -1].values

> * from sklearn.model_selection import KFold
> * kf = KFold(n_splits=10)
> * for train_index, test_index in kf.split(X,y):
>	 * X_train, X_test = X[train_index], X[test_index]
>	 * y_train, y_test = y[train_index], y[test_index]

### 2. Use the Find-S Library
> * from classic_FindS import FindS
> * fs = FindS()            
> * S_hypothesis = fs.fit(X_train, y_train)
> * print("Specific Hypothesis : ", S_hypothesis)
> * y_pred = fs.predict(X_test) 


----------



Footnotes
-------------

You can find the code at my [Github](https://github.com/safir72347/ML-FindS-PyPi).



Connect with me on Social Media
-------------

* [https://www.github.com/safir72347](www.github.com/safir72347)
* [https://www.linkedin.com/in/safir72347/](https://www.linkedin.com/in/safir72347/)
* [https://www.instagram.com/safir_12_10/](https://www.instagram.com/safir_12_10/)
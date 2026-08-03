📉 **Customer Churn Analysis**

Some customers leave without a word. This project figures out who — before they do.

Customer churn analysis is the difference between reacting to lost revenue and preventing it. This project explores customer behavior data to uncover why customers leave, builds a predictive model to flag who's likely to leave next, and turns those insights into something a business team can actually act on.

🎯 Objective
Identify the key drivers behind customer churn
Build a model that predicts churn risk before a customer leaves
Translate findings into actionable retention strategies
🗂️ Dataset
	
**Source:** Telco Customer Churn dataset (Kaggle)
Rows	e.g. 7,000+ customer records
Features	Demographics, subscription/contract details, usage patterns, billing history
Target	Churn (Yes/No)
🔍 **Project Workflow**
Data Cleaning — handle missing values, fix data types, remove duplicates
Exploratory Data Analysis (EDA) — uncover patterns in tenure, contract type, billing, and support interactions that correlate with churn
Feature Engineering — encode categorical variables, create derived features (e.g. tenure buckets, spend-per-month)
Modeling — train and compare classification models to predict churn
Evaluation — assess models using metrics suited to imbalanced classification
Insights & Recommendations — translate model output into retention actions
🧠 **Models Used**
Model	Purpose
Logistic Regression	Baseline, interpretable churn probability
Random Forest	Captures non-linear patterns, feature importance
XGBoost / Gradient Boosting	Higher-performance benchmark

📊 **Evaluation Metrics**
Since churn datasets are typically imbalanced (far fewer churners than non-churners), accuracy alone is misleading. This project evaluates models using:

Precision & Recall — how many flagged churners were actually going to churn, and how many real churners did we catch
F1 Score — balance between precision and recall
ROC-AUC — overall ability to distinguish churners from non-churners
Confusion Matrix — a clear view of false positives vs. false negatives
📈 **Key Insights**
Customers on month-to-month contracts churn at a significantly higher rate than those on annual contracts
Tenure is one of the strongest predictors — customers in their first few months are highest risk
High monthly charges combined with low service usage is a strong churn signal
Lack of tech support / add-on services correlates with higher churn
<img width="720" height="333" alt="Fist" src="https://github.com/user-attachments/assets/aa6ecef1-09a0-41aa-a043-9418b9265780" />
<img width="679" height="362" alt="third" src="https://github.com/user-attachments/assets/75b38a8b-7463-4a88-b827-8cf9616978c1" />
<img width="720" height="348" alt="fourth" src="https://github.com/user-attachments/assets/5492ee44-69eb-435c-9796-85f95561deb1" />






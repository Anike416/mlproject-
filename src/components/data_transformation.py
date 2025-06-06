import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
class DataTransConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTrans:
    def __init__(self):
        self.data_trans_config=DataTransConfig()
        
    def get_data(self):
        "This function is responsible for data transformation"
        try:
            num_col=["writing score","reading score"]
            cat_col=["race/ethnicity","gender","lunch","test preparation course","parental level of education"]
         
            num_pipeline=Pipeline(
             steps=[("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())]
             )   
         
            cat_pipeline=Pipeline(
                steps=[("imputer",SimpleImputer(strategy="most_frequent")),
                       ("onehot",OneHotEncoder(handle_unknown="ignore")),
                       ("scaler",StandardScaler(with_mean=False))]
            )
            
            logging.info('Numerical columns got standardized')
            logging.info('Categorical columns got onehot encoded')
            
            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_col),
                    ("cat_pipeline",cat_pipeline,cat_col)
                ]
            )
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_trans(self,train_path,test_path):
        try:
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            
            logging.info("Obtaining preprocessor object")
            
            preprocessing_obj=self.get_data()
            
            target_col='math score'
            num_col=["writing score","reading score"]
            
            input_feature_train_df=train_data.drop(columns=[target_col],axis=1)
            target_feature_train_df=train_data[target_col]
            
            input_feature_test_df=test_data.drop(columns=[target_col],axis=1)
            target_feature_test_df=test_data[target_col]
            
            logging.info("Applying preprocessing on train data and test data")
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr=np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]  
            test_arr=np.c_[input_feature_test_arr , np.array(target_feature_test_df)
                          ]
            
            logging.info("Saved the preprocessed data")
            
            save_object(
                file_path=self.data_trans_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            return(train_arr,test_arr,self.data_trans_config.preprocessor_obj_file_path)
        
        
        except Exception as e:
            raise CustomException(e,sys)
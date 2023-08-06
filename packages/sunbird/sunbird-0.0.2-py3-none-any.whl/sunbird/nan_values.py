import pandas as pd
import numpy as np
from scipy.stats import mode
import seaborn as sns


#1
def median_imputation(df,variable,plot=False,drop=False):
	median=df[variable].median()
	df[variable+"_median"]=df[variable].fillna(median).inplace=True
	if plot==True:
		sns.kdeplot(df[variable+"_median"])
		sns.kdeplot(df[variable])
	if drop==True:
		df=df.drop([variable],axis=1)




#2
def random_sampler(df,variable,plot=False,drop=False):
	df[variable+'_random']=df[variable]
	rs=df[variable].dropna().sample(df[variable].isnull().sum(),random_state=0)
	rs.index=df[df[variable].isnull()].index
	df.loc[df[variable].isnull(),variable+'_random']=rs
	if plot==True:
		sns.kdeplot(df[variable+"_random"])
		sns.kdeplot(df[variable])
	if drop==True:
		df=df.drop([variable],axis=1)




#3
def mean_imputation(df,variable,plot=False,drop=False):
	mean=df[variable].mean()
	df[variable+"_mean"]=df[variable].fillna(mean).inplace=True
	if plot==True:
		sns.kdeplot(df[variable+"_mean"])
		sns.kdeplot(df[variable])
	if drop==True:
		df=df.drop([variable],axis=1)




#4
def mode_imputation(df,variable,plot=False,drop=False):
	mode=df[variable].mode()
	df[variable+"_mode"]=df[variable].fillna(mode).inplace=True
	if plot==True:
		sns.kdeplot(df[variable+"_mode"])
		sns.kdeplot(df[variable])
	if drop==True:
		df=df.drop([variable],axis=1)



#5
def capture_nan(df,variable):
	df[variable+'_nan']=np.where(df[variable].isnull(),1,0)
	df[variable].median()
	df[variable].fillna(df.variable.median(),inplace=True)




#6
def endof_distribution(df,variable,plot=False,drop=False):
	extr=df[variable].mean()+3*df[variable].std()
	df[variable+'_enddist']=df[variable].fillna(extr)
	if plot==True:
		sns.kdeplot(df[variable+"_enddist"])
		sns.kdeplot(df[variable])
	if drop==True:
		df=df.drop([variable],axis=1)




#7
def arbitrary_imputation(df,variable,arbit,plot=False,drop=False):
	df[variable+'_arbitrary']=df[variable].fillna(arbit)
	if plot==True:
		sns.kdeplot(df[variable+"_arbitrary"])
		sns.kdeplot(df[variable])
	if drop==True:
		df=df.drop([variable],axis=1)




#8
def frequent(df,variable):
    most_frequent_category=df[variable].mode()[0]
    df[variable].fillna(most_frequent_category,inplace=True)




#9
def add_variable(df,variable):
	df[variable]=np.where(df[variable].isnull(),1,df[variable])
	frequent=df[variable].mode()[0]
	df[variable].fillna(frequent,inplace=True)




#10
def fill_missing(df,variable):
	df[variable]=np.where(df[variable].isnull(),'Missing',df[variable])
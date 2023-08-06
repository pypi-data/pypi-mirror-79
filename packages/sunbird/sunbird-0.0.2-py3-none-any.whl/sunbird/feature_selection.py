from sklearn.feature_selection import SelectKBest,chi2,f_regression,f_classif
import pandas as pd


class SelectBest:
	def __init__(self,score_func,k):
		self.score_func=score_func
		self.k=k
		self.score=None
		self.X=None

	def fit(self,X,y):
		model=SelectKBest(score_func=self.score_func,k=self.k)
		model.fit(X,y)
		self.score=model.scores_
		self.X=X


	def best_feature(self):
		dfscore=pd.DataFrame(self.score)
		dfcolumn=pd.DataFrame(self.X.columns)
		best_rank_feature=pd.concat([dfcolumn,dfscore],axis=1)
		best_rank_feature.columns=["Features","Score"]
		print(best_rank_feature)




def RemoveCollinearity(dataset, threshold): 
    col_corr = set() # Set of all the names of correlated columns 
    corr_matrix = dataset.corr() 
    for i in range(len(corr_matrix.columns)):
        for j in range(i): 
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value 
                colname = corr_matrix.columns[i]
                col_corr.add(colname) 
    return col_corr
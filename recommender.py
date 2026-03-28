import os
import pandas as pd
from data_loader import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBaseRecommender:
    
    def __init__(self, movies_database):
        # Make a copy of the movies database
        self.movies_df = getattr(movies_database, 'movies').copy()
        # Make sure genres are strings
        self.movies_df['genres'] = self.movies_df['genres'].fillna('').astype(str)

        # TF-IDF vectorizer on genres
        self.tfidf = TfidfVectorizer(tokenizer=lambda x: x.split('|'))
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['genres'])

        # Precompute calculate the cosine sim matrix
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)


    def recommend(self, movie, year, top = 10):
        target_idx = movie.index[0]
        similar_idxes = []
        # Search through the cosine matrix for movies that have score between 0.7 and 1
        for i, value in enumerate(self.cosine_sim[target_idx]) :
            if i != target_idx and (value >= 0.6 ) :
                similar_idxes.append(i) 
        
        similar_idxes = sorted(similar_idxes, key = lambda x : self.cosine_sim[target_idx][x], reverse= True)

        # Create a df contain movie with the same genres 
        df = pd.DataFrame(columns=['title'])
        for i in range(len(similar_idxes)) :
            # Comparing the year of release
            if float(self.movies_df.iloc[similar_idxes[i]]['year']) == year :
                df.loc[len(df)] = {'title': self.movies_df.iloc[similar_idxes[i]]['title']}
        
        return df.iloc[0:top]

 

class CollaborativeRecommender:
    def __init__(self, movies_database):
        # Make a copy of the movies database
        self.movies_df = getattr(movies_database, 'movies').copy()
        self.ratings_df = getattr(movies_database, 'ratings')[['userId','movieId','rating']].copy()
        self.ratings_df = self.ratings_df.pivot(index='movieId', columns='userId', values='rating')
        self.cosine_sim = cosine_similarity(self.ratings_df.fillna(0), self.ratings_df.fillna(0))
        self.ratings_df['avg'] = self.ratings_df.mean(axis=1)
    
    
    def recommend(self, movie, top = 10):
        target_idx = movie.index[0]
        similar_idxes = []
        # Search through the cosine matrix for movies that have rating score between 0.7 and 1
        for i, value in enumerate(self.cosine_sim[target_idx]) :
            if i != target_idx and (value >= 0.7 ) :
                similar_idxes.append(i)
        
        #  Filter through to make sure all movie are generally good
        similar_idxes = [
        idx for idx in similar_idxes
        if self.ratings_df.iloc[idx]['avg'] >= 3]
        
        similar_idxes = sorted(similar_idxes, key = lambda x : self.cosine_sim[target_idx][x], reverse= True)

        df = pd.DataFrame(columns=['title'])
        for i in range(len(similar_idxes)) :
            df.loc[len(df)] = {'title': self.movies_df.iloc[similar_idxes[i]]['title']}
        
        return df.iloc[0:top]

        
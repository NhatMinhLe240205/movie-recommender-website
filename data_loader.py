import pandas as pd
import os

def normalize_title(title):
    title = title.lower().strip()
    title = title[:-7] # Every movie end with a " (year)" which is 7 char
    for article in [', the', ', a', ', an'] :
        if title.endswith(article):
            title = article[2:] + ' ' + title[:-len(article)]
            break
    
    return title

class MovieDatabase:

    # Initialize the path for each file
    def __init__(self, file_path):
        self.movies_file = os.path.join(file_path, 'movies.csv')    # Movies database path
        self.ratings_file = os.path.join(file_path, 'ratings.csv')  # Ratings database path
        self.links_file = os.path.join(file_path, 'links.csv')      # Links database path
        self.tags_file = os.path.join(file_path, 'tags.csv')        # Tags databae path

    # Loading dataframe with files
    def load_database(self):
        self.movies = pd.read_csv(self.movies_file)
        self.ratings = pd.read_csv(self.ratings_file)
        self.links = pd.read_csv(self.links_file)
        self.tags = pd.read_csv(self.tags_file)
        self.movies['year'] =  self.movies['title'].str.extract(r"\((\d{4})\)", expand=False) # Copy the years to its proper column 
        self.movies['title_norm'] = self.movies['title'].apply(normalize_title)

    # Printing dataframe from name
    def print_dataframe(self, df_name):
        df = getattr(self, df_name, None)
        if df_name != None:
            print(df)
        else:
            print('Dataframe' + df_name + 'is not found ')

    # Get movie as a one row dataframe function
    def find_movie(self, movie_name):
        if not hasattr(self, 'movies') :
            raise ValueError("Movies DataFrame not loaded. Call load_database() first.")
        movie_name = movie_name.lower().strip()
        # Create df that have the movie's name
        df = self.movies[self.movies['title_norm'].str.contains(movie_name, case = False, na= False)]

        
        if (len(df) <= 0) :
            print("Movie is not in the database sorry")
        elif (len(df) > 1) :
            print("Can you specify which movie ? (in number) : ")
            for i in range(len(df)):
                print(str(i + 1) + ". " + str(df.iloc[i, 1]))
            
            # Input movie chosen among movies
            movie_index = int(input())
            movie_name_choosen = df.iloc[movie_index - 1, 1]
            print("You choose : " + movie_name_choosen)
            # Set dataframe to return a dataframe with one row
            df = df.iloc[[movie_index - 1]]
        
        return df

    def search_movies(self, query, limit=10):
        if not hasattr(self, 'movies'):
            raise RuntimeError("Call load_database() first.")
        query = query.lower().strip()
        mask = self.movies['title_norm'].str.contains(query, case=False, na=False)
        results = self.movies[mask].head(limit)
        return results[['movieId', 'title', 'genres', 'year']].to_dict(orient='records')

    # ← NEW
    def get_movie_by_id(self, movie_id):
        if not hasattr(self, 'movies'):
            raise RuntimeError("Call load_database() first.")
        df = self.movies[self.movies['movieId'] == movie_id]
        return df


    

    

    


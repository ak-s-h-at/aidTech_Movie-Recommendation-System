import csv
import numpy as np
from sklearn.metrics import pairwise_distances
from tkinter import Tk, Label, Entry, Button, Listbox, END


movies_dataset_path = r'D:\Task 2- Movie Recommendation system\movies.csv'
ratings_dataset_path = r'D:\Task 2- Movie Recommendation system\rating.csv'

def load_movie_ratings(filename):
    movie_ratings = {}
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            user_id, movie_id, rating = int(row[0]), int(row[1]), float(row[2])
            if user_id not in movie_ratings:
                movie_ratings[user_id] = {}
            movie_ratings[user_id][movie_id] = rating
    return movie_ratings

def load_movie_names(filename):
    movie_names = {}
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            movie_id, movie_name = int(row[0]), row[1]
            movie_names[movie_id] = movie_name
    return movie_names


movie_ratings = load_movie_ratings(ratings_dataset_path)
movie_names = load_movie_names(movies_dataset_path)


num_users = max(movie_ratings.keys()) + 1
num_movies = max(max(user_ratings.keys()) for user_ratings in movie_ratings.values()) + 1

ratings_matrix = np.zeros((num_users, num_movies))
for user_id, user_ratings in movie_ratings.items():
    for movie_id, rating in user_ratings.items():
        ratings_matrix[user_id, movie_id] = rating

def calculate_similarity_matrix():
    global similarity_matrix
    similarity_matrix = 1 - pairwise_distances(ratings_matrix, metric="cosine")

calculate_similarity_matrix()

def make_recommendations(user_ratings, ratings_matrix):
    user_id = num_users - 1
    user_ratings = movie_ratings[user_id]

    similarity_scores = similarity_matrix[user_id]
    weighted_scores = np.dot(similarity_scores, ratings_matrix)
    sorted_indices = np.argsort(weighted_scores)[::-1]
    recommendations = []
    for index in sorted_indices:
        if index not in user_ratings:
            movie_id = index
            movie_name = movie_names[movie_id]
            recommendations.append(movie_name)
        if len(recommendations) == 5:
            break
    return recommendations

def rate_movie():
    movie_name = movie_entry.get()
    rating = float(rating_entry.get())
    if movie_name in movie_names.values():
        movie_id = list(movie_names.keys())[list(movie_names.values()).index(movie_name)]
        user_ratings[movie_id] = rating
        movie_entry.delete(0, END)
        rating_entry.delete(0, END)
        ratings_matrix[num_users - 1, movie_id] = rating
        calculate_similarity_matrix()
        recommended_movies = make_recommendations(user_ratings, ratings_matrix)
        display_recommended_movies(recommended_movies)

def display_recommended_movies(recommended_movies):
    window = Tk()
    window.title("Recommended Movies")
    window.geometry("400x400")
    movie_listbox = Listbox(window)
    movie_listbox.pack()
    for movie in recommended_movies:
        movie_listbox.insert(END, movie)
    window.mainloop()

window = Tk()
window.title("Movie Recommendation System")
window.geometry("400x400")


movie_label = Label(window, text="Enter Movie Name:")
movie_label.pack()
movie_entry = Entry(window)
movie_entry.pack()


rating_label = Label(window, text="Enter Rating (1-5):")
rating_label.pack()
rating_entry = Entry(window)
rating_entry.pack()


rate_button = Button(window, text="Rate Movie", command=rate_movie)
rate_button.pack()

window.mainloop()

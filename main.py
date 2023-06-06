import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


dataset_path = r'D:\Task 2- Movie Recommendation system\movies.csv'
with open(dataset_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    movie_data = list(reader)

movies = []
genres = []
for movie in movie_data:
    movie_id, title, genre = movie
    genres.append(genre.split('|'))
    movies.append(title)

genres_list = [' '.join(g) for g in genres]
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(genres_list)

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

window = tk.Tk()
window.title("Movie Recommendation System")
window.geometry("400x300")

label = tk.Label(window, text="Enter a movie title:")
label.pack()
entry = tk.Entry(window)
entry.pack()


recommendation_text = scrolledtext.ScrolledText(window, height=10)
recommendation_text.pack()

def recommend_movies():
    movie_title = entry.get().strip()
    if movie_title:
        movie_index = -1
        for index, movie in enumerate(movies):
            if movie_title.lower() in movie.lower():
                movie_index = index
                break
        
        if movie_index != -1:
            similarity_scores = list(enumerate(cosine_similarities[movie_index]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            similar_movies_indices = [i[0] for i in similarity_scores]
            recommended_movies = [movies[i] for i in similar_movies_indices if i != movie_index]
            recommendation_text.delete("1.0", tk.END)
            for movie in recommended_movies[:10]:
                recommendation_text.insert(tk.END, f"- {movie}\n")
        else:
            messagebox.showwarning("Warning", "Movie not found in the dataset.")
    else:
        messagebox.showwarning("Warning", "Please enter a movie title.")


button = tk.Button(window, text="Get Recommendations", command=recommend_movies)
button.pack()

window.mainloop()

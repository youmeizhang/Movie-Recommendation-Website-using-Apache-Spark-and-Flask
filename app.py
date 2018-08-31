#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 21:18:55 2018

@author: yumi.zhang
"""

import cherrypy, os 
from flask import Blueprint, render_template
import json
from movie_engine import RecommendationEngine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from sqlalchemy import create_engine
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
 
from flask import Flask, request, session

@main.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        user_id = session['username']
        logger.debug("User %s TOP ratings requested", user_id)
        #select top 10 movies to show
        top_ratings = recommendation_engine.get_top_ratings(user_id, 10)
        
        #count how many movies did the user rate
        #select the top 10 movies that user gave high / low ratings
        rated_number, user_rated_movies_high, user_rated_movies_low, my_ratings_RDD = recommendation_engine.get_rated_movies(user_id)
        
        movie_file = pd.read_csv('file:///Users/yumi.zhang/Desktop/recommendation/datasets/ml-latest-small/movies.csv')
        tag_file = pd.read_csv('file:///Users/yumi.zhang/Desktop/recommendation/datasets/ml-latest-small/tags.csv')
          
        def get_poster_online(movidId):
            links = pd.read_csv('file:///Users/yumi.zhang/Desktop/recommendation/datasets/ml-latest-small/links.csv')
            
            number = "tt00"
            imdbId = list(links.loc[links['movieId'] == movidId, 'imdbId'])
            number += str(imdbId[0])        
            url = 'https://www.imdb.com/title/%s' % number
                
            response = get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            movie_containers = html_soup.find('div', class_ = 'poster')
            poster_url = movie_containers.a.img['src']
        
            return poster_url
    
        
        movie_year_name = []
            
        for i in top_ratings:
            movie_year_name.append(i[1])
           
        high_movie_year_name = []
        low_movie_year_name = []
        
        def get_movie_name(movieId):
            name = list(movie_file.loc[movie_file['movieId'] == movieId, 'title'])
            return name
            
        for i in user_rated_movies_high:
            tmp_name_high = get_movie_name(i[1])
            high_movie_year_name.append(tmp_name_high[0])
            
        for i in user_rated_movies_low:
            tmp_name_low = get_movie_name(i[1])
            low_movie_year_name.append(tmp_name_low[0])
            
        url_list = []
        genres_list = []
        tag_list = []
        
        for i in range(len(top_ratings)):
            movieId = top_ratings[i][0]
            poster_url = get_poster_online(movieId)
            url_list.append(poster_url)
            
            genres = list(movie_file.loc[movie_file['movieId'] == movieId, 'genres'])
            genres_list.append(genres)
            
            tag = list(tag_file.loc[tag_file['movieId'] == movieId, 'tag'])
            tag_list.append(tag)

        tmp_genre = []
        movie_genres = []
        for genre in genres_list:
            for i in genre:
                tmp_genre.append(i)
            movie_genres.append(tmp_genre)
            tmp_genre = []
        
        new_movie_genres = []
        
        for i in movie_genres:
             tmp = i[0].split('|')
             new_movie_genres.append(tmp)
             
            
        high_rated_movie_list = []
        for i in range(len(user_rated_movies_high)):
            movieId = user_rated_movies_high[i][1]
            high_rated_movie_url = get_poster_online(movieId)
            high_rated_movie_list.append(high_rated_movie_url)
            
        low_rated_movie_list = []
        for i in range(len(user_rated_movies_low)):
            movieId = user_rated_movies_low[i][1]
            low_rated_movie_url = get_poster_online(movieId)
            low_rated_movie_list.append(low_rated_movie_url)
            
        
        #get the newest movie information
        newmovie_src, newmovie_title, cinemas_name = get_newest_movies_info()
                
        return render_template('home.html', user_id = user_id, url_list = url_list, 
                               movie_year_name = movie_year_name,
                               new_movie_genres = new_movie_genres, tag_list = tag_list, 
                               rated_number = rated_number, high_rated_movie_list = high_rated_movie_list,
                               low_rated_movie_list = low_rated_movie_list, 
                               low_movie_year_name = low_movie_year_name,
                               high_movie_year_name = high_movie_year_name,
                               newmovie_src = newmovie_src, newmovie_title = newmovie_title,
                               cinemas_name = cinemas_name)
 
def get_newest_movies_info():
    url = "https://www.imdb.com/movies-in-theaters/"         
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    movie_containers = html_soup.find_all('div', class_ = 'image')
    newmovie_src = []
    title = []
    number = []
    for i in range(len(movie_containers)):
        newmovie_src.append(movie_containers[i].a.div.img['src'])
        title.append(movie_containers[i].a.div.img['title'])
        number.append(movie_containers[i].a['href'].split('/')[2])
      
    url = []
    for i in number:
        url.append('https://www.imdb.com/showtimes/title/%s/?ref_=inth_ov_sh' % i)
        
    #showtime_url = "https://www.imdb.com/showtimes/title/tt4779682/?ref_=inth_ov_sh"
    cinemas_name = []
    for i in url:
        span_name = []
        showtime_response = get(i)
        showtime_html_soup = BeautifulSoup(showtime_response.text, 'html.parser')
        new_movie_containers = showtime_html_soup.find_all('div', class_="fav_box")
        
        for i in range(len(new_movie_containers)):
            span_name.append(new_movie_containers[i].h3.a.span.text)
            
        cinemas_name.append(span_name)
        
    return newmovie_src, title, cinemas_name

@main.route('/login', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    session['username'] = request.form['username']
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@main.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@main.route("/shutdown")
@cherrypy.expose
def shutdown(self):  
    cherrypy.engine.exit()
    
@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
        
    return json.dumps(top_ratings)
    
 
@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])
    return json.dumps(ratings)

@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the negine (user_id, movie_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)
 
    return json.dumps(ratings)
 
def create_app(spark_context, dataset_path):
    global recommendation_engine 
    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    app.secret_key = os.urandom(12)
    
    return app
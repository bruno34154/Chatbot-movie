from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests 
import json
import os
from dotenv import load_dotenv
load_dotenv() 

def fetchPopularMovies(link):
    requisicao = requests.get(link)
    obj = json.loads(requisicao.content)
    arrayMovies = obj['results']
    strmovies = ""
    for movie in arrayMovies:
        strmovies = strmovies + str(movie['title']) + ", "
    return strmovies
def fetchOneSingleMovie(movie):
    requisicao = requests.get('https://api.themoviedb.org/3/search/movie?api_key='+os.getenv('API_KEY')+'&language=pt-BR'+'&query='+ movie)
    obj = json.loads(requisicao.content)
    arrayMovie = obj['results']
    strmovies = ""
    
    strmovies = arrayMovie[0]['overview']
    return strmovies

def fetchMostPopularMovie():
    requisicao = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+os.getenv('API_KEY')+'&language=pt-BR')
    obj = json.loads(requisicao.content)
    arrayMovie = obj['results']
    popularMovie = ''
    MostVoted = 0.0
    for movie in arrayMovie:
        if(movie['vote_average'] > MostVoted):
            MostVoted = movie['vote_average']
            popularMovie = movie['title']
            
    return popularMovie    

chatbot = ChatBot('botzin')
trainer = ListTrainer(chatbot)
trainer.train('conversaTreino.yml') #Aqui dentor é onde eu treino a ia passando dialogos

while True:
    pergunta = input("Usuario: ")
    resposta = chatbot.get_response(pergunta)
    moviesres = ""
    if(str(resposta).startswith('1')):
        moviesres = fetchPopularMovies('https://api.themoviedb.org/3/movie/popular?api_key='+os.getenv('API_KEY')+'&language=pt-BR')
    if(str(resposta).startswith('2')):
        frase = pergunta.split(' ')
        moviesres = fetchOneSingleMovie(frase[-1])
    if(str(resposta).startswith('3')):
        moviesres = fetchMostPopularMovie()
    if(float(resposta.confidence)>0.5):
        print(str(resposta) + " " + moviesres)
    else:
        print('ainda nao sei responder essa pergunta')


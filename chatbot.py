from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests 
import json
import os
from dotenv import load_dotenv
load_dotenv() 

def fetchResponse():
    requisicao = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+os.getenv('API_KEY')+'&language=pt-BR')
    obj = json.loads(requisicao.content)
    arrayMovies = obj['results']
    strmovies = ""
    for movie in arrayMovies:
        strmovies = strmovies + str(movie['title']) + ", "
    return strmovies


chatbot = ChatBot('botzin')
trainer = ListTrainer(chatbot)
trainer.train(['' ]) #Aqui dentor é onde eu treino a ia passando dialogos

while True:
    pergunta = input("Usuario: ")
    resposta = chatbot.get_response(pergunta)
    moviesres = ""
    if(str(resposta).startswith('1')):
        moviesres = fetchResponse()
    if(float(resposta.confidence)>0.5):
        print(str(resposta) + " " + moviesres)
    else:
        print('ainda nao sei responder essa pergunta')


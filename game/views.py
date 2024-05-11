from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json
import datetime
import random
import string

from .models import IndividualGame
# Create your views here.

def gameCodeGen():
    now = datetime.datetime.now()
    random_part = random.choice(string.ascii_uppercase)
    second = str(now.second) 
    gameCode = random_part  + second
    return gameCode

def makeGame():
    gameCode = gameCodeGen()
    gameState = False
    return gameCode, gameState

def homePage(request):
    gameCode, gameState = makeGame()
    context = {'gameCode' : gameCode, 'gameState' : gameState}
    IndividualGameItem = IndividualGame(gameCode = gameCode, gameState = gameState)
    IndividualGameItem.save()
    context = {'gameCode': gameCode, 'gameState': gameState}
    return render(request, "game/X.html", context)

def joinAsO(request):
    if request.method == 'POST':
        gameCode = request.POST.get('gameCodeInput', '').strip()
        print (gameCode)
    else:
        # Handle the case for a GET request or other methods if needed
        gameCode = request.GET.get('gameCodeInput', '').strip()
    try:
        specificGame = IndividualGame.objects.get(gameCode = gameCode)
        specificGame.gameState = True
        specificGame.save() 
    except:
        print("Could Not find game")
        homePage(request)
    gameCode = specificGame.gameCode
    gameState = specificGame.gameState
    context = {'gameCode': gameCode, 'gameState': gameState}
    return render(request, "game/O.html", context)

def xPlayer(request):
    print("About to make a new page")
    return render (request, "game/xPlayer.html")


def checkGameState(request):
    gameCode = request.GET.get('gameCode', '').strip()
    try:
        specificGame = IndividualGame.objects.get(gameCode=gameCode)
        gameState = specificGame.gameState
        if gameState:
            return JsonResponse({'redirect': True, 'url': '/xPlayer'})
        else:
            return JsonResponse({'gameState': gameState})
    except IndividualGame.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

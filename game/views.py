from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
    board = specificGame.board
    context = {'gameCode': gameCode, 'gameState': gameState, "board":board}
    return render(request, "game/O.html", context)

def xPlayer(request, gameCode):
    print("Loading xPlayer page for game code:", gameCode)
    specificGame = IndividualGame.objects.get(gameCode=gameCode)
    board = specificGame.board
    return render(request, "game/xPlayer.html", {'gameCode': gameCode,"board":board})


def checkGameState(request):
    gameCode = request.GET.get('gameCode', '').strip()
    try:
        specificGame = IndividualGame.objects.get(gameCode=gameCode)
        gameState = specificGame.gameState
        if gameState:
            redirect_url = reverse('xPlayer', args=[gameCode])  # Correctly constructs the URL with the actual gameCode
            return JsonResponse({'redirect': True, 'url': redirect_url})
        else:
            return JsonResponse({'gameState': gameState})
    except IndividualGame.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
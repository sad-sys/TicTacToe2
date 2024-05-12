from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
    gameTurn = specificGame.gameTurn
    context = {'gameCode': gameCode, 'gameState': gameState, "board":board, "gameTurn":gameTurn}
    return render(request, "game/O.html", context)

def xPlayer(request, gameCode):
    print("Loading xPlayer page for game code:", gameCode)
    specificGame = IndividualGame.objects.get(gameCode=gameCode)
    board = specificGame.board
    gameTurn = specificGame.gameTurn
    return render(request, "game/xPlayer.html", {'gameCode': gameCode,"board":board,"gameTurn":gameTurn})

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
    
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
@csrf_exempt  # This is generally not recommended without proper CSRF handling, especially in production.
def updateGameBoard(request, gameCode):
    gameID = request.POST.get('gameID')
    try:
        specificGame = IndividualGame.objects.get(gameCode=gameCode)

    except IndividualGame.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)
    print ("POST GAME ID is ", gameID)
    print ("specificGame.gameTurn ", specificGame.gameTurn)
    if gameID == specificGame.gameTurn:
        new_board = request.POST.get('board')
        if new_board:
            specificGame.board = new_board.split(',')
            if specificGame.gameTurn == "X" and gameID == "X":
                specificGame.gameTurn = "O"
            elif specificGame.gameTurn == "O" and gameID == "O":
                specificGame.gameTurn = "X"
            specificGame.save()

             # Assuming the board is sent as a comma-separated string
            return JsonResponse({"status": "success", "new_board": specificGame.board})
        else:
            return JsonResponse({"error": "No board data provided"}, status=400)
    else: 
        print ("Not your turn")
        pass
@require_http_methods(["GET", "POST"])  # Allow both GET and POST requests
@csrf_exempt  # Note: Using csrf_exempt is not recommended in production without proper CSRF protection
def getGameBoard(request, gameCode):
    if request.method == 'GET':
        game = get_object_or_404(IndividualGame, gameCode=gameCode)
        return JsonResponse({'board': game.board})
    # Handle POST request if necessary, here

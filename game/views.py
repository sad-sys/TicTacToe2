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

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
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

@csrf_exempt
@require_http_methods(["GET", "POST"])
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

@csrf_exempt
@require_POST
def updateGameBoard(request, gameCode):
    gameID = request.POST.get('gameID')

    def checkIfWon(game_board):
        # Check rows for a winner
        for row in game_board.values():
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[0]
        
        # Check columns for a winner
        for col in range(3):
            if game_board['0'][col] == game_board['1'][col] == game_board['2'][col] and game_board['0'][col] != 0:
                return game_board['0'][col]
        
        # Check diagonals for a winner
        if game_board['0'][0] == game_board['1'][1] == game_board['2'][2] and game_board['0'][0] != 0:
            return game_board['0'][0]
        if game_board['0'][2] == game_board['1'][1] == game_board['2'][0] and game_board['0'][2] != 0:
            return  game_board['0'][2]
    
        # If no winner, return 'Noone'
        return 'Noone'

    def boardConverter(game, gameBoard, board, player):
        # Extract column and row from the board list
        col = board[0]
        row = board[1]
        # Update the gameBoard at the specified column and row
        # Here, row_key accesses the correct row, and col accesses the correct column
        row_key = str(row)
        if row_key in gameBoard and col < len(gameBoard[row_key]):
            if gameBoard[row_key][col] == 0:
                gameBoard[row_key][col] = player 
                current_turn = game.gameTurn
                toggle_turn(game, current_turn)
            else:
                print ("Empty")
        print(checkIfWon(gameBoard))
        return gameBoard
    
    def convertBoardDataIntoList(board_data):
        board_dataList = []
        for i in range(0,len(board_data)):
            if i == 0 or i == 2:
                board_dataList.append(int(board_data[i]))
        return board_dataList
        
    def get_game_by_code(game_code):
        try:
            return IndividualGame.objects.get(gameCode=game_code)
        except IndividualGame.DoesNotExist:
            return None

    def update_game_board(specificGame, board_data, game_id):
        specificGame.board = board_data.split(',')
        oldBoard = specificGame.gameBoard.copy()
        print("OldBoard is ", oldBoard)
        print ("Data to be passed into boardconverter", list(board_data))
        board_data = convertBoardDataIntoList(board_data)
        print (board_data)
        specificGame.gameBoard = boardConverter(specificGame, specificGame.gameBoard, board_data, specificGame.gameTurn)
        specificGame.save()
        print (specificGame.gameBoard)
        newBoard = specificGame.gameBoard
        print("New Board is", newBoard)
        specificGame.save()
        return specificGame.board

    def toggle_turn(game, current_turn):
        if game.gameTurn == "X" and current_turn == "X":
            game.gameTurn = "O"
        elif game.gameTurn == "O" and current_turn == "O":
            game.gameTurn = "X"


    specificGame = get_game_by_code(gameCode)
    if not specificGame:
        return JsonResponse({"error": "Game not found"}, status=404)
    
    print("POST GAME ID is ", gameID)
    print("specificGame.gameTurn ", specificGame.gameTurn)

    if gameID == specificGame.gameTurn:
        new_board = request.POST.get('board')
        if new_board:
            updated_board = update_game_board(specificGame, new_board, gameID)
            return JsonResponse({"status": "success", "new_board": updated_board})
        else:
            return JsonResponse({"error": "No board data provided"}, status=400)
    else:
        print("Not your turn")
        return JsonResponse({"error": "Not your turn"}, status=403)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def getGameBoard(request, gameCode):
    def get_game(game_code):
        return get_object_or_404(IndividualGame, gameCode=game_code)

    if request.method == 'GET':
        game = get_game(gameCode)
        return JsonResponse({'board': game.board, "wholeBoard":game.gameBoard, "gameTurn":game.gameTurn})
    # Additional handling for POST can be added here if necessary
from django.db import models

# Create your models here.
class IndividualGame(models.Model):
    gameCode = models.CharField(max_length = 3)
    gameState = models.IntegerField(null=True, blank=True, default = 0)
    board = models.JSONField(null=True, default=list)  # Stores the Tic-Tac-Toe board state
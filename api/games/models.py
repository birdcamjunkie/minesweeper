from django.db import models

"""
A minesweeper game
"""


class Game(models.Model):
    is_complete = models.BooleanField(default=False)
    game_map = models.JSONField()

    def __str__(self):
        return str(self.id)

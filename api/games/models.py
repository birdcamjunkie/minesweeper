from django.db import models

"""
A minesweeper game
"""
class Game(models.Model):
    is_complete = models.BooleanField(default=False)
    values = models.JSONField()

    def __str__(self):
        return str(self.id)

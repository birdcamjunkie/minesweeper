from django.db import models

## Example:
## id - ak2_32
## is_complete: False
## values: { {is_revealed: false, is_bomb: true}, {is_revealed: true, is_bomb: false}, ...}
class Game(models.Model):
    is_complete = models.BooleanField(default=False)
    values = models.JSONField()

    def __str__(self):
        return str(self.id)

from django.db import models
# from django.contrib.auth.models import User


class Platforms(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    platform = models.ForeignKey(Platforms, on_delete=models.CASCADE)
    elo = models.IntegerField()
    master = models.BooleanField(default=False)
    numberOfduels = models.IntegerField()
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.title + ' - Platform: ' + self.platform.title

class Duels(models.Model):
    dueltoken = models.CharField(max_length=100)
    game1 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game1')
    eloGame1 = models.IntegerField()
    newEloGame1 = models.IntegerField(default=0)
    eloToUpdateGame1 = models.IntegerField(default=0)
    game2 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game2')
    eloGame2 = models.IntegerField()
    newEloGame2 = models.IntegerField(default=0)
    eloToUpdateGame2 = models.IntegerField(default=0)

    def __str__(self):
        return self.dueltoken + ' - Platform: '
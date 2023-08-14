from django.shortcuts import render
from elogame.models import Game, Duels


# Create your views here.

def home(request):
    return render(request, 'index.html')

def rankings(request):
    bestGameEver = Game.objects.all().order_by("-elo").first()
    bestGameEverImage = '/media/' + str(bestGameEver.image)
    return render(request, 'rankings.html',{
        'bestgame': bestGameEver,
        'bestgameimage': bestGameEverImage 
    })

def about(request):
    return render(request, 'about.html')
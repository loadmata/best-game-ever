from django.shortcuts import render, redirect
from .models import Game, Duels
import random
import secrets

# Funcion que se ejecuta al entrar en PLAY/
def gameHome(request):

    if request.method == 'GET':
        games = Game.objects.all()
        selectedGame1 = random.choice(games)
        selectedGame2 = random.choice(games)

        while selectedGame1.pk == selectedGame2.pk:
            selectedGame2 = random.choice(games)

        image1 = '/media/' + str(selectedGame1.image)
        image2 = '/media/' + str(selectedGame2.image)
        token = secrets.token_hex(32)

        return render(request, 'gameHome.html', {
            'game1': selectedGame1,
            'game2': selectedGame2,
            'image1': image1,
            'image2': image2,
            'token': token
        })
    else:
        return redirect('play')

# Funcion que actualiza los valores de ELO y muestra los resultados.
def calculateElO(request):
    if request.method == 'GET':
       return redirect('play')
    else:
        try:
            duelstoken = random.choice(Duels.objects.filter(dueltoken=request.POST['duel']))
            return redirect('play')
        except:
            # recupero los juegos de la base de datos
            # TODO: hacerlo de otra forma
            game1 = random.choice(Game.objects.filter(id=request.POST['game1']))
            game2 = random.choice(Game.objects.filter(id=request.POST['game2']))

            # Preparo las URL de las imagenes para mostrarlas.
            image1 = '/media/' + str(game1.image)
            image2 = '/media/' + str(game2.image)
        
            # miro cual a sido el ganador y los añado a las variables correspondientes.
            # TODO: Hacerlo de otra forma.
            try:
                buttonPressed = request.POST['button_1.x']
                resultGame1 = 1
                resultGame2 = 0

            except:
                buttonPressed = request.POST['button_2.x']
                resultGame1 = 0
                resultGame2 = 1

            expectedResultGame1 = expectedResult(game1.elo, game2.elo)
            expectedResultGame2 = expectedResult(game2.elo, game1.elo)

            eloResultGame1 = int(eloInThisDuel(
                game1.numberOfduels, game1.master, expectedResultGame1, resultGame1))
            eloRresultGame2 = int(eloInThisDuel(
                game2.numberOfduels, game2.master, expectedResultGame2, resultGame2))

            oldElo1 = game1.elo
            oldElo2 = game2.elo

            # Actualizar el valor de elo.
            game1.elo += int(eloResultGame1)
            game2.elo += int(eloRresultGame2)

            # Se le suma un duelo a cada juego
            game1.numberOfduels += 1
            game2.numberOfduels += 1

            # comprobacion para saber si es master, si es master se graba el valor maestro en la bsae de datos.
            # este valor es para siempre una vez llega a 2400 punto elo ya se le considera un maestro para siempre.
            game1.master = isMaster(game1.elo, game1.master)
            game2.master = isMaster(game2.elo, game2.master)

            # Guardar en la bsae de datos los nuevos valores de elo.
            game1.save()
            game2.save()

            saveDuel(request.POST['duel'], game1, game2, oldElo1, oldElo2, game1.elo, game2.elo)

            # se renderiza la pagina pasando todos los valores que necesita.
            return render(request, 'result.html', {
                'game1': game1,
                'game2': game2,
                'image1': image1,
                'image2': image2,
                'elogame1': eloResultGame1,
                'elogame2': eloRresultGame2,
            })

# Funcion que calcula el resultado esperado del duelo para los dos juegos.
def expectedResult(elo1, elo2):
    result = 1 / (1+10**((elo2-elo1)/400))
    return result

# Funcion que mira el nivel de Master que tiene el juego y calcula el elo que se gana o se pierde en el duelo.
def eloInThisDuel(duels, master, expectedResult, result):
    k = 0

    if duels <= 30:
        k = 40
    elif master == False:
        k = 20
    else:
        k = 10

    result = k * (result - expectedResult)
    return result

# Funcion que mira si se superan los 2400 puntos y marca el check de master
def isMaster(elo, master):
    if master == False:
        if elo > 2400:
            master = True
            return master
    return master

# Funcion que guarda el duelo en el registro de duelos.
def saveDuel(token, game1, game2, oldElo1, oldElo2, newElo1, newElo2):
    duel = Duels()
    duel.dueltoken = token
    duel.game1 = game1
    duel.game2 = game2
    duel.eloGame1 = oldElo1
    duel.eloGame2 = oldElo2
    duel.newEloGame1 = newElo1
    duel.newEloGame2 = newElo2

    duelEloGame1 = newElo1 - oldElo1 
    duelEloGame2 = newElo2 - oldElo2 

    duel.eloToUpdateGame1 = duelEloGame1
    duel.eloToUpdateGame2 = duelEloGame2

    duel.save()

def top500(request):
    top500 = list()
    items = 0
    gameList = Game.objects.all().order_by('-elo')
    for game in gameList:
        top500.append(game)
        items +=1
        if items == 3:
            return render(request, 'top500.html',{
        'gamelist': top500
    })

    
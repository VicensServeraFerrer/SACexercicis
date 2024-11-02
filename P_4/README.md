EXPLICACIO
La solusió per aquest exercici consta de 3 fitxers:

player.py
sala.py
server.py

Les funcions de cada un son:

player.py: Es conecta al servidor, rep el topic d'una sala i un nom y llança missatges que contenen les seves jugades
    - Topics: game/connect - Serveix per demanar un nom i que li assignin una sala (només publica)
              game/getGame - Es el topic on rebra el seu nom i el topic de la sala (es subscriu i no publica)
              topic de la sala - Es el topic on enviarà els seus moviments i sabrà si guanya perd o empata (es subscriu i publica)


sala.py: Rep el topic d'una sala i s'encarrega de gestionar la seva llògica, la qual consisteix inicialitzar els valors del tauler
        assignar quins jugadors son els que enviaran el missatge al topic de la sala, actualitzar el tauler amb els valors corresponents i 
        declarar si hi ha hagut un guanyador.
    - Topics: create/sala - en aquest topic rep el nom del jugador que s'ha conectat i el topic de la sala al que s'ha conectat (es subscriu i no publica)
              Tots els topics de sala - la entitat sala es subscriu a tots els topics de les salas que li arriben

server.py: Aquesta entitat s'encarrega de donar el nom als jugadors que es connecten, així com el topic de la sala a la qual jugaran. Per altre
            banda dona a l'entitat sala tots els noms i topics de sala que necessita per fer el matchmakeing.
    - Topics: game/connect - Rep els noms dels jugadors que volen jugar (es subscriu i no publica)
              game/getGame - Retorna el nou nom i el topic de la sala a la qual el jugador s'ha de conectar (només publica)
              create/sala - Envia el nom del jugador i el topic de la sala al qual s'ha de conectar a l'entitat sala (només publica)

EXECUCIÓ
S'ha d'executar per ordre, server, sala i posteriorment tots els players que es vulgui.


REFLEXIONS:
Amb aquest tipus de tecnologia es poden fer virgueries, es molt potent i fàcil de manejar. El problema es el de sempre, la centralizació de procesos, sense l'entitat sala els jugadors no podrien jugar i tampoc ho podrien fer sense l'entitat server. Es podria fer una versió mes independent on cada jugador tengués el seu taulell i la conexió fos mes estil peer-to-peer, encara que també es necessitaria una entitat centralitzadora, que en aquest cas podria ser un sol topic, i asumint que no hi ha problemes de xarxa sería factible. 
Aplicant la solusió alterna augmentaria la quantitat de missatges ja que crec que hi hauria d'haver moltes més comprovacions de seguretat i consistència.
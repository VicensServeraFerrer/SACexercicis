La solució aportada esta enfocada amb conexió TCP i per un nombre indefinit de players

Cada vegada que un fil es connecta queda registrat dins un array de players, en el qual només hiha un master i els altres no ho son.

Funcions master: 
Quan un fil es el master s'encarrega de demanar ajuda, si ja l'ha demanada decrementa el timeout del missatge. Si l'ajuden (que per
ferho es necessita que 2 players slave l'ajudin) es torna a triar qui es el master entre tots els players de l'array.

Funcions slave:
Un slave si ha de donar suport a un missatge de ajuda te un 30% de probabilitats de ferho, independentment de si dona suport o no,
posa a True una variable que indica que ja ho ha fet, fent que nomes pugui ajudar 1 pic cada missatge de help. Despres d'això es dorm entre
1 i 3 segons.

Reflexions:
Aquesta implementació tot i que funciona i es per qualsevol nombre de players no la trob eficient a novell de consum de recursos. 
Ja que tots els fils estan constantment executant operacions. A més en el cas de que el master sortís de la sessió tots els altres 
quedarien amb bucle, essent un punt comú de falla per a tots els fils d'execució.

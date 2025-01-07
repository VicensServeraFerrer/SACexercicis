FORMACIÓ I DETALLS DEL CODI:

En el codi es poden veure 3 funcions, sequential_histogram (processa les dades de l'histograma de manera seqüencial), parallel_histogram (processa les dades de l'histograma de manera paralela) i el main.

Les dies funcions que tracten les dades segueixen el mateix esquema:

1. Comptatge de freqüències
2. Càlcul d'acumulació

A la funció paralela hi ha una inicialització del vector atomic (que s'utilitza per evitar problemes de concurrència) i posteriorment, després del comptatge de les freqüències, un traspàs de valors a un vector no atòmic (per temes de returns i tractament de dades).

La passa 1 a la funció sequencial es fa amb un for y a la funció paralela amb un parallel_for. 

La passa 2 a la funció seqüencial també es fa amb un for i a la funció paralela es fa amb un scan.

La funció main es dedia a llançar les dues funcions, a recollir els seus resultats, imprimir-los per pantalla i calcular i imprimir el temps que tarda cada una d'elles

PROVES, RESULTATS I CONCLUSIONS:

Fent proves amb distints mides de vector he pogut veure que si el vector es molt petit, l'algoristme executat de manera seqüencial. Per mides de vector de menys de 100.000 unitats, el sequencial es més ràpid, de manera que quan més aprop de 0 més diferència hi ha, i quan mes aprop de 100.000 menys diferència hi ha.

A partir d'aquest punt, a mesura que el nombre de unitats dins el vector continua creixent la diferència entre paralel i seqüencial es més grossa a favor del paralel. 







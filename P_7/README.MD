En aquesta pràctica es presenta una solusió al radix sort usant la llibreria tbb de intel.

El codi consta de 4 funcions:

main()
radixSort()
sortByDigit()
getDigit()

main()
Es tracta de la funció que llança el radix sort i es comunica amb l'usuari mitjançant sortides de text esmentant el resultat. 

radixSort()
En aquesta funció es crida les vegades que sigui necessari a la funcio sortByDigit segons el nombre de digits del nombre més gran de l'array.

sortByDigit()
La funció principal que du a terme tota l'operativa es la de sortByDigit(). La qual es pot dividir en 4 parts.

1. Contar el nombre d'aparicions de cada digit dins l'array
2. Calcular les posicions de cada digit amb un parallel scan
3. Construir l'array output generat
4. Copiarlo a l'array per a la seguent iteració

Per realitzar aquestes funcions s'usen les funcions de tbb parallel for i parallel scan,

1. El primer parallel for es per contar el nombre d'aparicions de cada digit
2. El parallel scan es per trobar les posicions de cada un dels digits de l'array,sumant el nombre d'aparicions de cada un dels digits.
3. Després, mitjançant un parallel for es transpassen els resultats a un array  local output
4. I finalment un darrer parallel for per transpassar els valors a l'array passat per parametre.

getDigit()
Donat un nombre retorna el figit de la posició que s'indica



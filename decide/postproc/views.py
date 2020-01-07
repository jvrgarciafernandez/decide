from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        return Response({})

class dhondt():
 
   #Requiere un diccionario con atributos nombre y valor respectivamnete, el nº de escaños y el valor minimo que se pone en 3% por defecto
   #Ejemplo de llamada
   #lista = {'nombre' : ['PP', 'PSOE', 'TMT', 'EGC', 'PGPI', 'DP'] , 'valor' : [547,2715,6443,21,14,7331]}
   #nescanos = 8
   #valorMin = 3
   #
   #print(dhondt.calc(nescanos, lista, valorMin))
   #
   #output del ejemplo: dp tmt dp tmt psoe dp tmt dp (array[])
 
 
   def calc(nescanos, lista, valorMin):
 
       sol = [0 for i in range(nescanos)]
       solNombres = [0 for i in range(nescanos)]
       length = len(lista['nombre'])
       listaAux = copy.deepcopy(lista)
       totalVotos = 0
      
       #Total votos
       for i in range(length):
           totalVotos += listaAux['valor'][i]
 
       #Excluir los que no superan el minimo
       i = 0
       while i < length:
           if listaAux['valor'][i] / totalVotos <= (valorMin/100):
               del(listaAux['nombre'][i])
               del(listaAux['valor'][i])
               length = length-1
           else: i += 1
 
       #Matriz para el calculo
       matrix = [[0 for x in range(length)] for y in range(nescanos)]
       for i in range(length):
           for j in range(nescanos):
 
               #La matriz se puede omitir ya que solo hace falta el calculo del valor
               matrix[j][i] = listaAux['valor'][i] / (j+1)
               if sol[nescanos-1] < matrix[j][i]:
                   sol[nescanos-1] = matrix[j][i]
                   solNombres[nescanos-1] = listaAux['nombre'][i]
 
               #Ordenamos la solucion
               pos = copy.deepcopy(nescanos) -1
               aux = 0
               auxN = ""
               while sol[pos] > sol[pos-1] and pos > 0:
 
                   aux = sol[pos]
                   sol[pos] = sol[pos-1]
                   sol[pos-1] = aux
 
                   auxN = solNombres[pos]
                   solNombres[pos] = solNombres[pos-1]
                   solNombres[pos-1] = auxN
 
                   pos -= 1
 
       #return sol para valores numericos, matrix para matriz
       return solNombres
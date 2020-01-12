from rest_framework.views import APIView
from rest_framework.response import Response
import copy

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def calc(self, opts, nescanos):
        
        out = []

        sol = [0 for i in range(nescanos)]
        solNombres = [0 for i in range(nescanos)]
        length = (len(opts))
        listaAux = copy.deepcopy(opts)
        totalVotos = 0     

        for i in range(length):
            totalVotos += opts[i]['votes']

        for i in range(length):
           if opts[i]['votes'] / totalVotos <= (3/100):
               opts[i]['votes'] = 0

        matrix = [[0 for x in range(length)] for y in range(nescanos)]
        for i in range(length):
            for j in range(nescanos):
 
                #La matriz se puede omitir ya que solo hace falta el calculo del valor
                matrix[j][i] = listaAux[i]['votes'] / (j+1)
                if sol[nescanos-1] < matrix[j][i]:
                    sol[nescanos-1] = matrix[j][i]
                    solNombres[nescanos-1] = listaAux[i]['option']
 
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

        #Cambiamos el postproc con los escaños
        for i in range(length):
            opts[i]['postproc'] = 0

        for i in range(nescanos):
            for j in range(length):
                if solNombres[i] == opts[j]['option']:
                    opts[j]['postproc'] += 1

        for opt in opts:
            out.append({**opt})

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
        d = request.data.get('dhont')
        n = request.data.get('numero_dhont')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            if d == True:
                return self.calc(opts,n)
            else:
                return self.identity(opts)

        return Response({})
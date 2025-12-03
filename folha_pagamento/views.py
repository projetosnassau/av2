from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import CalculadoraFolhaPagamento

class FolhaPagamentoView(APIView):
    def post(self, request):
        dados = request.data ## recebe os dados enviados pelo usuário
        
        try:
            # pega os valores, se não existir assume que é 0
            salario_base = float(dados.get('salario_base', 0))
            horas_extras = float(dados.get('horas_extras', 0))
            faltas = float(dados.get('faltas', 0))

            if salario_base <= 0:
                return Response(
                    {"erro": "O salário base é obrigatório e deve ser positivo!"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # instanciando o service
            calculadora = CalculadoraFolhaPagamento(salario_base)

            # processamento da folha
            resultado = calculadora.processar_folha(horas_extras, faltas)

            # retornando o resultado
            return Response(resultado, status=status.HTTP_200_OK)

        except ValueError:
            # caso enviem texto ao invés de numero
            return Response(
                {"erro": "Por favor, envie apenas números!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
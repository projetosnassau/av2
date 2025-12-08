from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FolhaPagamentoSerializer
from .services import CalculadoraFolhaPagamento, AnaliseSalarialService

class FolhaPagamentoView(APIView):
    """
    Calcula um único salário (Individual)
    """
    def post(self, request):
       # O serializer valida os dados antes de qualquer coisa
        serializer = FolhaPagamentoSerializer(data=request.data)
        
        if serializer.is_valid():
            # Se chegou aqui os dados são seguros e limpos
            dados = serializer.validated_data
            
            calc = CalculadoraFolhaPagamento(dados['salario_base'])
            resultado = calc.processar_folha(dados['horas_extras'], dados['faltas'])
            
            return Response(resultado, status=status.HTTP_200_OK)
        
        # Se deu erro (ex: salario negativo), tem q devolver o erro formatado
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnaliseSalarialView(APIView):
    """
    recebe uma lista de funcionários e devolve estatisticas
    """
    def post(self, request):
        # many=True avisa que vamos receber uma lista de objetos, não só um
        serializer = FolhaPagamentoSerializer(data=request.data, many=True)

        if serializer.is_valid():
            analise_service = AnaliseSalarialService()
            relatorio = analise_service.analisar_lista(serializer.validated_data)
            
            return Response(relatorio, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
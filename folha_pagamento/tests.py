from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import FolhaPagamentoView

class FolhaPagamentoViewTest(TestCase):
    def setUp(self):
        # o factory simula um navegador acessando o site
        self.factory = APIRequestFactory()
        # preparando a view para ser testada
        self.view = FolhaPagamentoView.as_view()

    def test_calculo_folha_sucesso_2025(self):
        """
        esta função testa um cenário padrão com salario de R$ 2.500,00
        tbm verifica se a view devolve status 200 (OK) e se a matematica bate
        com as regras de 2025 (INSS faixa 2 e IRRF isento)
        """
        # dados simulados ( que o usuário enviaria)
        dados = {
            "salario_base": 2500.00,
            "horas_extras": 0,
            "faltas": 0
        }

        # requisição post falsa
        request = self.factory.post('/api/calcular/', dados, format='json')

        # passando a requisição para a view
        response = self.view(request)

        # VERIFICAÇÕES:

        # o status deve ser 200 (=sucesso)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # o salário liquido deve ser exatamente 2297.77 (conforme calculei manualmente)
        # o 'places=2' diz para verificar até 2 casas decimais
        self.assertAlmostEqual(response.data['salario_liquido'], 2297.77, places=2)
        
        # verificando se o inss foi calculado certo (202.23)
        self.assertAlmostEqual(response.data['desconto_inss'], 202.23, places=2)

    def test_validacao_erro_sem_salario(self):
        """
        testa se a view bloqueia requisições sem o salario base
        """
        # enviando dados vazios
        request = self.factory.post('/api/calcular/', {}, format='json')
        response = self.view(request)
        
        # o status deve ser 400 (=erro do cliente)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validacao_erro_valor_negativo(self):
        """
        testa se a view bloqueia salarios negativos
        """
        dados = {"salario_base": -500}
        request = self.factory.post('/api/calcular/', dados, format='json')
        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
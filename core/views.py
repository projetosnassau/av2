from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Funcionario, FolhaPagamento
from .serializers import FuncionarioSerializer, FolhaPagamentoSerializer, CalculoInputSerializer, UserSerializer, RegisterSerializer
from .services import CalculadoraFolha

class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            dados = serializer.validated_data
            
            user = User.objects.create_user(
                username=dados['email'],
                email=dados['email'],
                password=dados['password'],
                first_name=dados['name']
            )

            if dados['role'] == 'manager':
                user.is_staff = True
                user.save()
            
            elif dados['role'] == 'employee':
                salary = dados.get('salary', 0)
                Funcionario.objects.create(
                    user=user,
                    nome=dados['name'],
                    email=dados['email'],
                    salario_base=salary,
                    cargo="Empregado (Auto-cadastro)"
                )

            return Response({
                "message": "Usuário criado com sucesso",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(views.APIView):
    """Retorna dados do usuário logado para o Frontend montar o perfil"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "name": user.get_full_name() or user.username,
            "email": user.email,
            "role": "manager" if user.is_staff else "employee"
        }
        
        if not user.is_staff:
            try:
                func = user.funcionario_profile
                data['name'] = func.nome
                data['salary'] = float(func.salario_base)
            except:
                data['salary'] = 0.0

        return Response(data)

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]

class FolhaViewSet(viewsets.ModelViewSet): 
    serializer_class = FolhaPagamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FolhaPagamento.objects.all().order_by('-data_emissao')
        
        if hasattr(user, 'funcionario_profile'):
            return FolhaPagamento.objects.filter(funcionario=user.funcionario_profile).order_by('-data_emissao')
        
        return FolhaPagamento.objects.none()

class ProcessarFolhaView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CalculoInputSerializer(data=request.data)
        if serializer.is_valid():
            dados = serializer.validated_data
            
            func = get_object_or_404(Funcionario, id=dados['employeeId'])
            
            calc = CalculadoraFolha(func.salario_base)
            resultado = calc.calcular(
                horas_extras=dados['overtimeHours'],
                bonus=dados['bonuses'],
                deducoes_manuais=dados['deductions']
            )
            
            folha = FolhaPagamento.objects.create(
                funcionario=func,
                mes_referencia=dados['month'],
                qtd_horas_extras=dados['overtimeHours'],
                bonus=dados['bonuses'],
                deducoes_manuais=dados['deductions'],
                
                valor_horas_extras=resultado['valor_horas_extras'],
                valor_faltas=resultado['valor_faltas'],
                salario_bruto=resultado['salario_bruto'],
                inss=resultado['inss'],
                irrf=resultado['irrf'],
                salario_liquido=resultado['salario_liquido']
            )
            
            return Response(FolhaPagamentoSerializer(folha).data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
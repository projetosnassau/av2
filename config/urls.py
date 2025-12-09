from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import FuncionarioViewSet, FolhaViewSet, ProcessarFolhaView, MeView
from core.views import RegisterView 

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'folhas', FolhaViewSet, basename='folha')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', MeView.as_view(), name='user_profile'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', include(router.urls)),
    path('api/calcular-folha/', ProcessarFolhaView.as_view(), name='calcular_folha'),
]
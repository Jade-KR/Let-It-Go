from django.urls import path, include
from rest_framework import routers
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

schema_view = get_schema_view(
    openapi.Info(
        title="LET IT GO API",
        default_version="v1",
        description="레고 커뮤니티 API 서비스입니다.",
        # terms_of_service='https://www.google.com/policies/terms/', # 약관 예시
        contact=openapi.Contact(email="pyeonggangkim@gmail.com"),
        license=openapi.License(name="SSAFY License"), 
    )
)

router = routers.DefaultRouter()
router.register(r"Themes", views.ThemeViewSet, basename="Themes")

urlpatterns = [
    *router.urls,
    path('swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/', include('allauth.urls')),
]

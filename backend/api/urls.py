from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="LET IT GO API",
        default_version="v1",
        description="레고 커뮤니티 API 서비스입니다.",
        # terms_of_service='https://www.google.com/policies/terms/', # 약관 예시
        contact=openapi.Contact(email="pyeonggangkim@gmail.com"),
        license=openapi.License(name="SSAFY License"), 
    ),
    "https://k02d1081.p.ssafy.io:8009/api/"
)

router = DefaultRouter(trailing_slash=False)
router.register(r"Themes", views.ThemeViewSet, basename="Themes")
router.register(r"LegoSet", views.LegoSetViewSet, basename="LegoSet")
router.register(r"LegoPart", views.LegoPartViewSet, basename="LegoPart")
router.register(r"UserPart", views.UserPartViewSet, basename="UserPart")
router.register(r"SetPart", views.SetPartViewSet, basename="SetPart")
router.register(r"Review", views.ReviewViewSet, basename="Review")
router.register(r"Follower", views.FollowUserViewSet, basename="Follower")
router.register(r"Following", views.FollowingUserViewSet, basename="Following")
router.register(r"User", views.UserViewSet, basename="User")
router.register(r"UserLegoSet", views.UserLegoSetViewSet, basename="UserLegoSet")
router.register(r"UserLikeLegoSet", views.UserLikeLegoSetViewSet, basename="UserLikeLegoSet")
router.register(r"LegoSetRanking", views.LegoSetRankingViewSet, basename="LegoSetRanking")
router.register(r"ItemBasedRecommend", views.ItemBasedRecommendViewSet, basename="ItemBasedRecommend")
router.register(r"UserBasedRecommend", views.UserBasedRecommendViewSet, basename="UserBasedRecommend")
router.register(r"UserSet", views.UserSetViewSet, basename="UserSet")

urlpatterns = [
    *router.urls,
    path('set_user_category', views.set_user_category, name="set_user_category"),
    path('UpdateUserPart', views.UpdateUserPart, name='UpdateUserPart'),
    path('UpdateUserPart2', views.UpdateUserPart2, name='UpdateUserPart2'),
    path('CreateLegoSet', views.CreateLegoSet, name='CreateLegoSet'),
    path('UpdateUserProfile', views.UpdateUserProfile, name='UpdateUserProfile'),
    path('swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('go_to_myhome/', views.go_to_myhome, name="go_to_myhome"),
    path('like_set', views.like_set, name='like_set'),
    path('follow', views.follow, name='follow'),
    path('crawll/<int:idx>', views.crawll, name='crawll'),
    path('user_parts_registered_by_IoT', views.user_parts_registered_by_IoT, name="user_parts_registered_by_IoT"),
    path('reset_user_based_knn', views.reset_user_based_knn, name="reset_user_based_knn"),
    path('reset_item_based_knn', views.reset_item_based_knn, name="reset_item_based_knn"),
    path('reset_user_based_k_means', views.reset_user_based_k_means, name="reset_user_based_k_means"),
    path('reset_item_based_k_means', views.reset_item_based_k_means, name="reset_item_based_k_means"),
    path('update_user_set_inventory', views.update_user_set_inventory, name="update_user_set_inventory"),
    path('update_user_set_inventory2', views.update_user_set_inventory2, name="update_user_set_inventory2"),

    # path('create_review', views.create_review, name='create_review')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

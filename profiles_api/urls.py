from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("hello-viewset", views.HelloViewSet, basename = "hello-viewset")
router.register("profiles", views.UserProfilesViewset)
router.register("feeds", views.ProfileFeedItemsView)

urlpatterns = [
    path("api/hello/", views.HelloAPIView.as_view()),
    path("api/login/", views.UserLoginApiView.as_view()),
    path("api/", include(router.urls)),

]

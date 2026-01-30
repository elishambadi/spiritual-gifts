from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpiritualGiftViewSet, QuestionViewSet, SurveyResponseViewSet

router = DefaultRouter()
router.register(r'spiritual-gifts', SpiritualGiftViewSet, basename='spiritual-gift')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'survey-responses', SurveyResponseViewSet, basename='survey-response')

urlpatterns = [
    path('', include(router.urls)),
]

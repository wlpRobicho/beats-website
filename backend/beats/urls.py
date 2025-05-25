from django.urls import path
from beats.views.upload import BeatUploadView
from beats.views.detail import BeatDetailView

urlpatterns = [
    path('upload/', BeatUploadView.as_view(), name='beat-upload'),
    path('<slug:slug>/', BeatDetailView.as_view(), name='beat-detail'),
]

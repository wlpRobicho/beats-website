from django.urls import path
from beats.views.upload import BeatUploadView
from beats.views.detail import BeatDetailView
from beats.views.list import BeatListView
from beats.views.featured import FeaturedBeatsView
from beats.views.top import TopBeatsView
from beats.views.latest import LatestBeatsView
from beats.views.tags import TagListView
from beats.views.random import RandomBeatView
from beats.views.trending import TrendingBeatsView

urlpatterns = [
    
    path('trending/', TrendingBeatsView.as_view(), name='trending-beats'),
    path('random/', RandomBeatView.as_view(), name='random-beat'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('latest/', LatestBeatsView.as_view(), name='latest-beats'),
    path('top/', TopBeatsView.as_view(), name='top-beats'),
    path('featured/', FeaturedBeatsView.as_view(), name='featured-beats'),
    path('', BeatListView.as_view(), name='beat-list'), 
    path('upload/', BeatUploadView.as_view(), name='beat-upload'),
    path('<slug:slug>/', BeatDetailView.as_view(), name='beat-detail'),
]

"""
Django urls.
"""

from django.urls import path
from api.views.leaderboard_country import LeaderboardCountryListView, \
    LeaderboardCountryRangeView, LeaderboardCountryStreamView
from api.views.leaderboard_global import LeaderboardListView, \
    LeaderboardRangeView, LeaderboardStreamView
from api.views.user import UserGetView, UserCreateView
from api.views.user_score import UserScoreView

app_name = 'api'

urlpatterns = [
    path(r'user/profile/<str:user_id>', UserGetView.as_view(), name='user_get'),
    path(r'user/create', UserCreateView.as_view(), name='user_create'),
    path(r'score/submit', UserScoreView.as_view(), name='score_submit'),
    path(r'leaderboard', LeaderboardListView.as_view(), name='leaderboard_list'),
    path(r'leaderboard/stream', LeaderboardStreamView.as_view(), name='leaderboard_stream'),
    path(r'leaderboard/range', LeaderboardRangeView.as_view(), name='leaderboard_range'),
    path(r'leaderboard/<str:iso_code>',
         LeaderboardCountryListView.as_view(), name='leaderboard_country'),
    path(r'leaderboard/country/<str:iso_code>/range',
         LeaderboardCountryRangeView.as_view(), name='country_range'),
    path(r'leaderboard/country/<str:iso_code>/stream',
         LeaderboardCountryStreamView.as_view(), name='country_stream')
]

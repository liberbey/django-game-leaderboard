"""
Model for UserScore.
"""

from django.db import models
from django.utils import timezone


class UserScore(models.Model):
    """
    Model for user-score, all score submits are hold in this model.
    """
    score_worth = models.FloatField(blank=False)
    user_id = models.ForeignKey('User', related_name='scores',
                                on_delete=models.CASCADE, blank=False,
                                db_column='user_id')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_score'

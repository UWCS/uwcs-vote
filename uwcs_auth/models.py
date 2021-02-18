from django.contrib.auth.models import User

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from votes.models import Ticket

class WarwickVoteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")

    uni_id = models.CharField(max_length=11)
    nickname = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return '{uni_id} - {nick} for user {id}'.format(uni_id=self.uni_id,
                                                        nick=self.nickname if self.nickname else "no nickname",
                                                        id=self.user.id)

    @property
    def is_exec(self):
        """
        Check if the user is part of the exec group
        """
        return 'exec' in self.user.groups.values_list(Lower('name'), flat=True)

    @property
    def long_name(self):
        if self.nickname.strip():
            return self.nickname.strip()
        else:
            return self.user.get_full_name()

    @property
    def ticket_set(self):
        return Ticket.objects.filter(member=self.uni_id)

    @property
    def member(self):
        return self

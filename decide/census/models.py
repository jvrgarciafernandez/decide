from django.db import models
from voting.models import Voting

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    def check_save(self,id):

        votings = Voting.objects.all()

        if votings:

            for v in votings:
                if v.id == id:
                    break
                    return True
                else:

                    return False



    class Meta:
        unique_together = (('voting_id', 'voter_id'),)



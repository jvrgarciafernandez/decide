import pandas as pd

from django import forms
from django.conf import settings
from django.db import transaction

from base.models import Auth
from voting.models import Question, QuestionOption, Voting


def get_local_auth():
    base_url = settings.BASEURL
    auths = Auth.objects.filter(url=base_url, name='System')

    if len(auths) == 0:
        result = Auth(url=base_url, name='System')
        result.save()
    else:
        result = auths[0]

    return result


class ImportSenateCandidates(forms.Form):

    candidate_file = forms.FileField()

    @transaction.atomic
    def save(self):
        candidate_file = self.cleaned_data.get('candidate_file', None)
        df = pd.ExcelFile(candidate_file, engine='xlrd').parse(index_col=0)

        Voting.checkInputFile(candidate_file)
        # TODO: se podría refactorizar el check para que solo haya que leer el
        #       fichero una vez

        for name, group in df.groupby(['Provincia']):
            count = 2

            quest = Question(desc='Elige un máximo de 2 personas para las '
                                  'listas al senado por ' + name)
            quest.save()

            voting_name = 'Votación Senado ' + name
            voting_desc = 'Listas al Senado por ' + name
            voting = Voting(name=voting_name, desc=voting_desc, question=quest)
            voting.save()
            voting.auths.add(get_local_auth())

            for row in group.iterrows():
                # TODO posible refactorización: eliminar count
                count += 1
                desc_option = row[1][4] + ': ' + \
                              row[0] + ' ' + row[1][0] + ' ' + row[1][1]

                quest_option = QuestionOption(number=count, option=desc_option)
                quest_option.question = quest
                quest_option.save()

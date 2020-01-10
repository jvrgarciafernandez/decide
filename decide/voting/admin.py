from django.contrib import admin, messages
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import TO_FIELD_VAR
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .forms import ImportSenateCandidates

from .models import QuestionOption
from .models import Question
from .models import Voting

from .filters import StartedFilter


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    fields = ['question', 'option']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [start, stop, tally]

    def get_add_context(self, form, to_field, extra_context):
        context = dict(
            title='Import votings',
            opts=self.model._meta,
            change=False,
            is_popup=False,
            to_field=to_field,
            save_as=False,
            has_delete_permission=False,
            has_add_permission=False,
            has_change_permission=False,
            form=form,
        )

        context.update(extra_context or {})

        return context

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('candidate_file',)

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(
                "The field %s cannot be referenced." % to_field)

        if request.method == 'POST':
            form = ImportSenateCandidates(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'All votings created correctly')
                return HttpResponseRedirect('/admin/voting/voting')
            else:
                messages.error(request, 'Please correct the error below')
        else:
            form = ImportSenateCandidates()

        context = self.get_add_context(form, to_field, extra_context)

        return render(request, 'import_form.html', context)

    def change_view(self, request, object_id, extra_context=None):
        self.form = ModelForm
        self.fields = None
        return super(VotingAdmin, self).change_view(request, object_id)


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)

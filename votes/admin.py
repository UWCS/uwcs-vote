from django.contrib import admin

from .models import Election, Candidate, Ticket, FPTPVote, APRVVote, STVVote, STVPreference, STVResult


class PreferenceInline(admin.StackedInline):
    model = STVPreference
    readonly_fields = ['order', 'candidate']
    can_delete = False
    extra = 0


class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 1


class STVVoteAdmin(admin.ModelAdmin):
    inlines = [PreferenceInline]
    readonly_fields = ['election', 'uuid', 'time', 'selection']


class ElectionAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]


# Register your models here.
admin.site.register(Election, ElectionAdmin)
admin.site.register(FPTPVote)
admin.site.register(APRVVote)
admin.site.register(Ticket)
admin.site.register(STVVote, STVVoteAdmin)
admin.site.register(STVResult)
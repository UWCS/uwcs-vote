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


class FPTPVoteAdmin(admin.ModelAdmin):
    readonly_fields = ['election', 'uuid', 'time', 'selection']


class STVVoteAdmin(admin.ModelAdmin):
    inlines = [PreferenceInline]
    readonly_fields = ['election', 'uuid', 'time', 'selection']


class STVResultAdmin(admin.ModelAdmin):
    readonly_fields = ['election', 'full_log', 'winners', 'generated']


class ElectionAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]


# Register your models here.
admin.site.register(Election, ElectionAdmin)
admin.site.register(FPTPVote, FPTPVoteAdmin)
admin.site.register(APRVVote, FPTPVoteAdmin)
admin.site.register(Ticket)
admin.site.register(STVVote, STVVoteAdmin)
admin.site.register(STVResult, STVResultAdmin)

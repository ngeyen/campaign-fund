from django.contrib import admin
from django.views.decorators.csrf import csrf_protect
from .models import Campaign


def has_approval_permission(request, obj=None):
    if request.user.has_perm('campaign.can_approve_campaign'):
        return True
    return False


class CampaignAdmin(admin.ModelAdmin):
    @csrf_protect
    def changelist_view(self, request, extra_context=None):
        if not has_approval_permission(request):
            self.list_display = ['title', 'slug', 'content', 'tag', 'image',
                                 'date_created', 'updated', 'is_approved']
            # list of fields to show if user can't approve the post

            self.editable = ['title', 'slug', 'content', 'tag', 'image',
                             'date_created', 'updated']
        else:
            self.list_display = ['title', 'slug', 'content', 'tag', 'image',
                                 'date_created', 'updated', 'approved_by', 'is_approved']
            # list of fields to show if user can approve the post
        return super(CampaignAdmin, self).changelist_view(request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        if not has_approval_permission(request, obj):
            self.fields = ['title', 'slug', 'content', 'tag', 'image',
                           'date_created', 'updated', ]  # same thing
        else:
            self.fields = ['title', 'slug', 'content', 'tag', 'image',
                           'date_created', 'updated', 'approved_by', 'is_approved']
        return super(CampaignAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Campaign)
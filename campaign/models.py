from django.db import models
from django.conf import settings
from django.db.models import Q
from accounts.models import User,Coordinator

Organizer = settings.AUTH_USER_MODEL


class CampaignQuerySet(models.QuerySet):  # custom query set
    def approved(self):
        return self.filter(is_approved__lte=True)

    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(User__first_name__icontains=query) |
                Q(User__last_name__icontains=query) |
                Q(User__username__icontains=query)
        )
        return self.filter(lookup)


class CampaignManager(models.Manager):  # uses this to only display what is published
    def get_queryset(self):
        return CampaignQuerySet(self.model, using=self._db)

    def is_approved(self):
        return self.get_queryset().approved()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().approved().search(query)


class Campaign(models.Model):
    organizer = models.ForeignKey(Organizer, blank=False, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # hello world -> hello-world
    content = models.TextField(null=False, blank=False)
    tag = models.CharField(verbose_name='Tag', max_length=50)
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)  # when added to the database, the field changes to that time
    updated = models.DateTimeField(auto_now=True)  # when save is hit, the time changes
    approved_by = models.ForeignKey(Coordinator,on_delete=models.SET_NULL, null=True, blank=True)


    objects = CampaignManager()

    class Meta:
        ordering = ['-updated', '-is_approved', '-date_created']
        permissions = (
            ('can_approve_campaign', 'Can Approve campaign'),
        )
    
    def  __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"

class Item(models.Model):
    campaign    = models.ForeignKey(Campaign, blank=False, null=True, on_delete=models.CASCADE)
    item_name   = models.CharField( verbose_name="Item Name", max_length=50)
    item_slug   = models.SlugField(verbose_name='slug', unique=True)
    short_desc  = models.CharField( verbose_name="Item desc", max_length=300)
    item_cost   = models.IntegerField( verbose_name="Item Cost", null=False, blank=False)
    is_funded   = models.BooleanField(verbose_name = "Fully Funded?", default = False)

    def __str__(self):
        return self.item_name
    
    
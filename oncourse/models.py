import datetime
from audioop import reverse

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(upload_to='media', blank=True)

    def __str__(self):
        return self.course_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Details(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, default='')
    date = models.DateField(blank=True, null=True)
    image = Course.image

    def __str__(self):
        return self.lecturer


class Participants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


'''   
    class Groups(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    g = Group(name=Course.objects.get(Course.course_name))
    g.save()

    def __str__(self):
        return self.g

  
    somemodel = ContentType.objects.get_for_model(Details)
    can_view = Permission(name='Can View', codename='can_view_something', content_type=somemodel)
    can_view.save()
    '''
'''
    content_type = ContentType.objects.get_for_model(Details)
    can_view = Permission.objects.create(
        codename='can_view',
        name='Can View',
        content_type=content_type,
    )
    g.permissions.add(can_view)
    
    
class Permissions(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)

    content_type = ContentType.objects.get(Details)
    can_view = Permission.objects.create(
        codename='can_view',
        name='Can View',
        content_type=content_type,
    )
    group.permissions.add(can_view)




'''



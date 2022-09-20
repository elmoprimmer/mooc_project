from django.db import models

from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class Nickname(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.TextField()

class File(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	data = models.FileField(upload_to=user_directory_path)


# This is only needed for unittest to check if the cookie has been stolen
class Mail(models.Model):
	content = models.TextField()

class Message(models.Model):
	source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source')
	target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
	content = models.TextField()
	time = models.DateTimeField(auto_now_add=True)

class No(models.Model):
    content = models.TextField()

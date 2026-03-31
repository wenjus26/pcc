from django.db import models
from django.conf import settings
from apps.citizens.models import Category
from django.utils.translation import gettext_lazy as _

class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Discussion')
        verbose_name_plural = _('Discussions')

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Commentaire')
        verbose_name_plural = _('Commentaires')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.thread.title}"

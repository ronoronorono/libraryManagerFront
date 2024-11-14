from django.db import models
from django.utils import timezone

class Book(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=50, unique=False)
    subtitle = models.CharField(max_length=50, unique=False, default='subtitulo vazio')
    theme = models.CharField(max_length=50, unique=False)
    author = models.CharField(max_length=50, unique=False)

    #book_copies = models.ForeignKey('BookCopies', on_delete=models.RESTRICT, related_name='book_copies',default=None)

    def __str__(self):
        return f'{self.title} - {self.subtitle} - {self.author}'
    '''
    def delete(self, *args, **kwargs):

        if not self.is_active and self.deleted_at is not None:
            models.Model.delete(self, *args, **kwargs)
        else:
            self.is_active = False
            self.deleted_at = timezone.now()
            self.save()
    '''
    def save(self, *args, **kwargs):
        #super().save(*args, **kwargs)
        '''
        if self.is_active:
            self.is_active = True
            self.deleted_at = None
        else:
            self.is_active = False
            self.deleted_at = timezone.now()
        '''
        super().save(*args, **kwargs)
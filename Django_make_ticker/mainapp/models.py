from django.db import models


class Request(models.Model):
    text = models.TextField(max_length=256, verbose_name='Text')
    background_color = models.CharField(max_length=256, verbose_name='Color')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created', editable=False)

    def __str__(self):
        return f'{self.pk}\t{self.text}'


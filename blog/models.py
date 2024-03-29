from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    views = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

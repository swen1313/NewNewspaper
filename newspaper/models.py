from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    userRating = models.IntegerField(default=0)

    def update_rating(self):
       postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
       pRat = 0
       pRat += postRat.get('postRating')
       commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
       cRat = 0
       cRat += commentRat.get('commentRating')

       self.userRating + pRat * 3 * cRat
       self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


article = 'A'
new = 'N'
choices = [(article, 'статья'), (new, 'новость')]


def __str__(self):
    return f'{self.name.title()}'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postType = models.CharField(max_length=1, choices=choices, default='article')
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.TextField(max_length=100)
    text = models.TextField()
    postRating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.header.title()}: {self.text[:20]}'


    def like(self):
        return self.postRating + 1
        self.save()


    def dislike(self):
        return self.postRating - 1
        self.save()


    def preview(self):
        return self.text[:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=64)
    commentRating = models.IntegerField(default=0)

    def like(self):
        return self.commentRating + 1
        self.save()


    def dislike(self):
        return self.commentRating - 1
        self.save()


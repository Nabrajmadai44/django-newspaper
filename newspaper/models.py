from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Don't create table in DB
        

class Category(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

        
class Tag(TimeStampModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in_active", "Inactive"),
    ]
    title = models.CharField(max_length=200)
    content= models.TextField()
    featured_image= models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    
    def __str__(self):
        return self.title
    
    
class UserProfile(TimeStampModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_images/%Y/%m/%d", blank=False)
    address = models.CharField(max_length=200)
    biography = models.TextField()
    
    def __str__(self):
        return self.user.username
    
    
class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField
    
    def __str__(self):
        return f"{self.email} | {self.comment[:70]}"
    
    
class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["created_at"]
    
    
# 1 user can create M posts => M
# 1 post can be created by 1 user => 1
# ForeginKey => Many side

# 1 post can be associated to only 1 category => 1
# 1 category can have multiple posts => M
# ForeignKey => Many Side

# 1 post can have multiple tags => M
# 1 tag can have multiple posts => M
# ManyTOManyField => Any side
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'telephone']


class Paint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')
    image4 = models.ImageField(upload_to='images/')
    image5 = models.ImageField(upload_to='images/')
    pdf_file = models.FileField(upload_to='pdf_files/', blank=True, null=True)
    artist = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.id}'


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - Profile'


class FavouritePaint(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    paints = models.ManyToManyField(Paint, related_name='liked_by')

    def __str__(self):
        return f'{self.user.username} - Favourite Paints'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paint = models.ForeignKey(Paint, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'paint']
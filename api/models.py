from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import JSONField, HStoreField
# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with username field."""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """Create and save a User with a given username and password."""
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """
        Create and save a regular User with the given username and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class GidaUser(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    image = models.TextField(null=True,
            default='https://res.cloudinary.com/systemshiftio/image/upload/v1565557753/cloudinary_qyi649.jpg')
    
    verified = models.BooleanField(default=False)
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    star_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
 
     
APARTMENT = (
     ('Serviced', 'Serviced'),
     ('Shared', 'Shared'),
     ('Private', 'Private')
     )
 
STATE = (
    ('', ''),
    ('Lagos', 'Lagos')
 )
 
COUNTRY = (
    ('', ''),
    ('Nigeria', 'Nigeria')
 )
 
LOCATION = (
     ('Yaba', 'Yaba'),
     ('Lekki', 'Lekki'),
     ('Victoria-Island', 'Victoria-Island'),
     ('Surulere', 'Surulere'),
     ('Ikoyi', 'Ikoyi')
 )
    
class Apartment(models.Model):
    room_type = models.CharField(max_length=50, choices=APARTMENT)
    address = models.CharField(max_length=100)
    images = JSONField(default=list)
    ammenities = HStoreField()
    price = models.DecimalField(max_digits=6, null=True, decimal_places=2)
    star_rating = models.IntegerField(default=0)
    number_of_checkins = models.IntegerField(default=0)
    state = models.CharField(max_length=50, choices=STATE)
    country = models.CharField(max_length=50, choices=COUNTRY)
    location = models.CharField(max_length=50, choices=LOCATION)
    info = models.TextField(null=True)
    owner = models.ForeignKey(GidaUser, null=True, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=10, default="Monthly")
    is_active = models.BooleanField(default=True)
    
    def _str__(self):
        return self.address
    

class BookedApartment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(GidaUser, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)
    occupied = models.BooleanField(default=False)
    # if a user decides to deactivate an apartment, it should send a message
    # to all users currently not checked in that they can book new apartment
    
    
class ApartmentReview(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    owner = models.ForeignKey(GidaUser, on_delete=models.CASCADE)
    content = models.TextField()
    star = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    

class UserReview(models.Model):
    user = models.ForeignKey(GidaUser, on_delete=models.CASCADE, related_name='home_owner')
    owner = models.ForeignKey(GidaUser, on_delete=models.CASCADE, related_name='owner')
    star = models.IntegerField(default=0)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    

    
    
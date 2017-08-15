from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import  datetime
from django.contrib.auth.models import  User
from django.core import validators
# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=50);
    lastname = models.CharField(max_length=50);
    city = models.CharField(max_length=50,null=True,blank=True)
    birthdate = models.DateField();
    #age = models.IntegerField()
    def __str__(self):
        return self.firstname;

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    numpages = models.IntegerField(null=False, default=0,validators=[MaxValueValidator(1000), MinValueValidator(50)])
    in_stock = models.BooleanField(default=True)
    def __str__(self):
        return self.title;


class Student(User):
    PROViNCE_CHOICES= (('AB','Alberta'),('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
                       )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROViNCE_CHOICES, default='ON')
    age = models.IntegerField()
    picture = models.ImageField(upload_to='myapp/images',null=True, blank=True)
    def __str__(self):
        return self.first_name;


class Course(models.Model):
    course_no = models.IntegerField( primary_key=True)
    title = models.CharField(max_length=50)
    textbook = models.ForeignKey(Book)
    students = models.ManyToManyField(Student)
    def __str__(self):
        return self.title;

class Topics(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    intro_course = models.BooleanField(default=True)
    NO_PREFERENCE = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    TIME_CHOICES = (
        (0, 'No preference'),
        (1, 'Morning'),
        (2, 'Afternoon'),
        (3, 'Evening')
    )
    time = models.IntegerField(default=0, choices=TIME_CHOICES)
    num_responses = models.IntegerField(default=0)
    avg_age = models.IntegerField(default=20)
    def __str__(self):
        return self.subject;

class ImagesTable(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='myapp/images')
    student = models.OneToOneField(Student);

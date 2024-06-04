from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Hall(models.Model):
    name = models.CharField("Name", max_length=50)
    nomer = models.IntegerField("Nomer")
    flor = models.IntegerField("Flor")
    square = models.IntegerField("Square")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hall'
        verbose_name_plural = 'Halls'


class EmployeePosition(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()

    def get_absolute_url_for_delete(self):
        return reverse('delete_employee_position', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('update_employee_position', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Employee_positions(models.Model): #1111111111111111111111111111
     name = models.CharField("Name", max_length=50)

     def __str__(self):
         return self.name

     class Meta:
         verbose_name = 'Employee_position'
         verbose_name_plural = 'Employee_positions'


class CustomUser(AbstractUser):
    age = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(18), MaxValueValidator(100)])
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13, null=True, default='+375290000000')

    def get_absolute_url_for_delete(self):
        return reverse('delete_user', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('edit_user', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True)
    legal_entity = models.BooleanField()

    def get_absolute_url(self):
        return reverse('clients', kwargs={'client_id': self.id})

    def __str__(self):
        return self.user.username


class Art_form(models.Model): #1111111111111111111111111111
    name = models.CharField("Name", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Art_form'
        verbose_name_plural = 'Art_forms'


class Exhibit(models.Model):
    name = models.CharField("Name", max_length=50)
    art = models.ForeignKey(Art_form, related_name="Art", on_delete=models.CASCADE)
    date = models.DateTimeField('Date')
    hall = models.ForeignKey(Hall, related_name="Hal", on_delete=models.CASCADE)
    image_source = models.ImageField(upload_to='images/', null=True, blank=True)
    keeper = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Exhibit'
        verbose_name_plural = 'Exhibits'


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    image_source = models.ImageField(upload_to='images/', null=True, blank=True)
    job = models.ForeignKey(EmployeePosition, on_delete=models.SET_NULL, null=True)
    hall = models.ForeignKey(Hall, related_name="Haall", on_delete=models.CASCADE)
    exhibits = models.ManyToManyField(Exhibit)
    exhibitions = models.ManyToManyField('Exhibitions')

    def __str__(self):
        return self.user.username


class Exhibitions(models.Model): #1111111111111111111111111111
    name = models.CharField("Name", max_length=50)
    date = models.DateTimeField('Date')
    people = models.IntegerField("People")
    code = models.IntegerField("Code")
    cost = models.IntegerField("Cost")
    hall = models.ForeignKey(Hall, related_name="Hall", on_delete=models.CASCADE)
    employe = models.ForeignKey(Employee, related_name="Employ", on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url_for_delete(self):
        return reverse('delete_service_type')

    def get_absolute_url_for_update(self):
        return reverse('update_service_type')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Exhibition'
        verbose_name_plural = 'Exhibitions'

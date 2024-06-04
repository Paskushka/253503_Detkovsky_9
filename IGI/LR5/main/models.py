from django.db import models
from django.urls import reverse
from myzei.models import CustomUser, Client, Employee, EmployeePosition, Exhibitions

class Question(models.Model):
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content

    def get_absolute_url_to_add(self):
        return reverse('add_answer', kwargs={'pk': self.pk})


class Answer(models.Model):
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content


class Vacancy(models.Model):
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.CASCADE)
    number_of_this_position = models.IntegerField()
    vacancy_description = models.TextField()

    def get_absolute_url_for_delete(self):
        return reverse('delete_vacancy', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('update_vacancy', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.employee_position.__str__()} {self.number_of_this_position}'


class Review(models.Model):
    author = models.ForeignKey(Client, on_delete=models.CASCADE)
    rate = models.IntegerField()
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.author.__str__()}'


class PromoCode(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()

    def __str__(self):
        return self.code


class Bonus(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()

    def __str__(self):
        return self.code


class Company(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to='images/', null=True, blank=True)
    logo = models.ImageField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyStory(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_source = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    exhibitions = models.ForeignKey(Exhibitions, on_delete=models.CASCADE)
    promocode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    bonus = models.ForeignKey(Bonus, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_to_add(self):
        return reverse('add_service_to_order', kwargs={'pk': self.pk})

    def get_absolute_url_to_more_info(self):
        return reverse('order_details', kwargs={'pk': self.pk})

    def get_total_price(self):
        total_price = self.exhibitions.cost
        if self.bonus != None and self.promocode != None:
            total_price *= (100 - (self.bonus.discount_percentage + self.promocode.discount_percentage)) / 100

        return total_price

    def __str__(self):
        return str(self.pk)


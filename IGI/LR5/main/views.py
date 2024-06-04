from datetime import timezone, datetime, timedelta
import pytz
import main.apis as api
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.contrib.auth.hashers import make_password
from tzlocal import get_localzone
from .forms import LoginForm, ClientRegistrationForm, EmployeeRegistrationForm, ReviewForm, QuestionForm, AnswerForm, \
    VacancyForm, EmployeePositionForm, OrderForm, ExhibitionsForm, ExhibitionsTypeForm
from django.conf import settings
import main.models as mod
from main import functions

import tzlocal
import calendar
import logging
from django.utils import timezone
from datetime import timezone as dt_timezone
from myzei import models

logger = logging.getLogger('django')


class LoginView(View):
    template_name = 'main/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def get(self, request):

        print("users", models.CustomUser.objects.all())
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user:
                login(request, user)

                logger.info(f'User logged in')

                return redirect(self.success_url)

        logger.info(f'User didn\'t log in')

        return render(request, self.template_name, {'form': form})


class ClientRegistrationView(View):
    template_name = 'main/register.html'
    form_class = ClientRegistrationForm
    success_url = reverse_lazy('login')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        client = self.form_class(request.POST)
        if client.is_valid():
            data = client.cleaned_data

            user = models.CustomUser(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=make_password(data['password1']),
                telephone=data['telephone'],
                username=data['email'],
                age=data['age'],
            )
            print("result: ", user, user.save())

            client_object = client.save(commit=False)
            client_object.user = user
            client_object.save()

            logger.info(f'Client was added')

            return redirect('login')

        logger.info(f'Client was NOT added')

        return render(request, self.template_name, {'form': client})


class EmployeeRegistrationView(View):
    template_name = 'main/register.html'
    form_class = EmployeeRegistrationForm
    success_url = reverse_lazy('employee_positions')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        employee = self.form_class(request.POST, request.FILES)
        if employee.is_valid():
            data = employee.cleaned_data

            user = models.CustomUser(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=make_password(data['password1']),
                telephone=data['telephone'],
                username=data['email'],
                age=data['age'],
                is_staff=True,
            )
            user.save()
            employee_object = employee.save(commit=False)
            employee_object.user = user
            employee_object.image_source = data['image_source']
            employee_object.date_of_beginning = datetime.now().strftime("%m-%d-%Y %H:%M:%S %Z")
            employee_object.save()
            employee_object.exhibits.set(data['exhibits'])
            employee_object.save()

            logger.info(f'Employee was added')

            return redirect('employees')

        logger.info(f'Employee was NOT added')

        return render(request, self.template_name, {'form': employee})


def delete_user(request, pk):
    user = models.CustomUser.objects.get(pk=pk)

    user.delete()

    logger.info(f'User was deleted')

    return redirect('home')


def edit_employee(request, pk):
    custom_user = models.CustomUser.objects.get(pk=pk)
    employee = models.Employee.objects.get(user=custom_user)
    form = EmployeeRegistrationForm({
        'first_name': custom_user.first_name,
        'last_name': custom_user.last_name,
        'email': custom_user.email,
        'telephone': custom_user.telephone,
        'age': custom_user.age,
        'image_source': employee.image_source,
        'exhibits': employee.exhibits.all(),
        'exhibitions': employee.exhibitions.all(),
        'job': employee.job,
    })

    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            custom_user.first_name = data['first_name']
            custom_user.last_name = data['last_name']
            custom_user.email = data['email']
            custom_user.password = make_password(data['password1'])
            custom_user.telephone = data['telephone']
            custom_user.username = data['email']
            custom_user.age = data['age']

            custom_user.save()

            employee.image_source = data['image_source']
            employee.position = data['position']
            employee.clients.set(data['clients'])
            employee.save()

            logger.info(f'Employee was edited')

            return redirect('employees')

    return render(request, 'main/register.html', {'form': form})


class EmployeesView(View):
    template_name = "main/employees.html"
    def get(self, request):
        employee = models.Employee.objects.all()
        all_halls = models.Hall.objects.all()
        hall_filter = request.GET.get('hall_filter')
        if hall_filter:
            employee = employee.filter(hall_id=hall_filter)
        context = {'employees': employee, 'all_halls': all_halls, }
        return render(request, self.template_name, context)


class ClientsView(View):
    template_name = "main/clients.html"

    def get(self, request):
        context = {'clients': models.Client.objects.all()}
        return render(request, self.template_name, context)


class LogoutView(View):
    success_url = reverse_lazy('login')

    def get(self, request):
        logout(request)

        logger.info(f'User logged out')

        return redirect(self.success_url)





def main_info(request): #добавить апишки
    logger.info('Main view was accessed')

    latest_news = mod.News.objects.order_by('-date').first()

    context = {
        "latest_news": latest_news,
        "joke": api.get_joke(),
        "quote": api.get_quote()
    }

    return render(request, 'main/main_info.html', context)


def about_company(request):# вот сюда добавить графики
    logger.info('About company view was accessed')

    context = {
               'client_age_median': functions.client_age_median(),
               'client_age_mean': functions.client_age_mean(),
               'client_age_mode': functions.client_age_mode(),
               #'average_service_price': functions.average_service_price(),
               #'get_difference_between_highest_price_and_average': functions.get_difference_between_highest_price_and_average(),
               'get_order_with_highest_price': functions.get_order_with_highest_price(),
               'get_most_popular_exhibition': functions.get_most_popular_exhibition(),
               'histogram_url': functions.plot_halls(),
               #'clients_with_order_count': functions.get_orders_sorted_by_clients_and_dates()
               }

    return render(request, 'main/about_company.html', context)

def news_page(request):
    logger.info('News view was accessed')

    news = mod.News.objects.order_by('-date')

    context = {"news": news}

    return render(request, "main/news.html", context)

def dictionary_page(request):
    logger.info('Dictionary view was accessed')

    questions = mod.Question.objects.all().order_by('-date')

    context = {"questions": questions}

    return render(request, "main/dictionary.html", context)

def contacts_page(request):
    logger.info('Contacts view was accessed')

    employees = models.Employee.objects.all()

    context = {"employees": employees}

    return render(request, "main/contacts.html", context)

def privacy_policy_page(request):
    logger.info('Privacy policy view was accessed')

    return render(request, "main/policy.html")

def vacancies_page(request):
    logger.info('Vacancies view was accessed')

    vacancies = mod.Vacancy.objects.all()

    context = {"vacancies": vacancies}

    return render(request, "main/vacancies.html", context)

def discounts_page(request):
    logger.info('Discounts view was accessed')

    promo_codes = mod.PromoCode.objects.all()
    bonuses = mod.Bonus.objects.all()
    context = {"promo_codes": promo_codes, "bonuses": bonuses}

    return render(request, "main/discounts.html", context)

class ReviewsView(View):
    template_name = "main/rewies.html"
    form_class = ReviewForm

    def get(self, request):
        context = {'reviews': mod.Review.objects.all().order_by('-date')}

        if request.user.is_authenticated:
            context['form'] = self.form_class

        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = self.form_class(request.POST)
        print(form.data, form.is_valid())
        if form.is_valid():
            review = form.save(commit=False)
            review.author = models.Client.objects.get(user=request.user)
            review.date = datetime.now()
            review.save()

            logger.info(f'Review was added')

        context = {'reviews': mod.Review.objects.all().order_by('-date'), 'form': self.form_class}
        return render(request, self.template_name, context)


class AddQuestionView(View):
    template_name = "main/add_something.html"
    success_url = reverse_lazy('dictionary')
    form_class = QuestionForm

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.date = datetime.now()
            question.save()

            logger.info(f'Question was added {question.pk}')

            return redirect(self.success_url)

        logger.info(f'Question was NOT added')

        return render(request, self.template_name, {'form': form})

class AddAnswerView(View):
    template_name = "main/add_something.html"
    success_url = reverse_lazy('dictionary')
    form_class = AnswerForm

    def get(self, request, pk):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.date = datetime.now()
            answer.save()
            question = mod.Question.objects.get(pk=pk)
            question.answer = answer
            question.save()

            logger.info(f'Answer was added to question {question.pk}')

            return redirect(self.success_url)

        logger.info(f'Answer was NOT added to question')

        return render(request, self.template_name, {'form': form})

def update_vacancy(request, pk):
    logger.info('Update vacancy view was accessed')

    vacancy = mod.Vacancy.objects.get(pk=pk)

    if request.method == "GET":
        form = VacancyForm(initial={
            'employee_position': vacancy.employee_position,
            'number_of_this_position': vacancy.number_of_this_position,
            'vacancy_description': vacancy.vacancy_description,
        })

        context = {'form': form}
        return render(request, "main/add_something.html", context)

    else:
        form = VacancyForm(request.POST)

        if form.is_valid():
            vacancy.employee_position = form.cleaned_data['employee_position']
            vacancy.number_of_this_position = form.cleaned_data['number_of_this_position']
            vacancy.vacancy_description = form.cleaned_data['vacancy_description']
            vacancy.save()

            logger.info(f'Vacancy where pk={pk} was updated')

            return redirect('vacancies')

        logger.info('Vacancy where pk={pk} was NOT updated')

        return render(request, "main/add_something.html", {'form': form})


class AddEmployeePositionView(View):
    template_name = "main/add_something.html"
    form_class = EmployeePositionForm
    success_url = reverse_lazy('employee_positions')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            logger.info(f'Employee position was added')

            return redirect(self.success_url)

        logger.info(f'Employee position was NOT added')

        return render(request, self.template_name, {'form': form})


def delete_vacancy(request, pk):
    vacancy = mod.Vacancy.objects.get(pk=pk)
    vacancy.delete()

    logger.info(f'Vacancy was deleted')
    return redirect('vacancies')

class AddVacancyView(View):
    template_name = "main/add_something.html"
    form_class = VacancyForm
    success_url = reverse_lazy('vacancies')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            logger.info(f'Vacancy was added')

            return redirect(self.success_url)

        logger.info(f'Vacancy was not added')

        return render(request, self.template_name, {'form': form})


def update_employee_position(request, pk):
    employee_position = models.EmployeePosition.objects.get(pk=pk)

    if request.method == "GET":
        form = EmployeePositionForm(initial={
            'name': employee_position.name,
            'area': employee_position.salary,
        })

        context = {'form': form}
        return render(request, "main/add_something.html", context)

    else:
        form = EmployeePositionForm(request.POST)

        if form.is_valid():
            employee_position.name = form.cleaned_data['name']
            employee_position.salary = form.cleaned_data['salary']
            employee_position.save()

            logger.info(f'Employee position was updated')

            return redirect('employee_positions')

        logger.info(f'Employee position was NOT updated')

        return render(request, "main/add_something.html", {'form': form})


def delete_employee_position(request, pk):
    employee_position = models.EmployeePosition.objects.get(pk=pk)
    employee_position.delete()

    logger.info(f'Employee position was deleted')

    return redirect('employee_positions')


class EmployeePositionsView(View):
    template_name = "main/employee_positions.html"

    def get(self, request):
        logger.info(f'Employee positions view was accessed')

        context = {'employee_positions': models.EmployeePosition.objects.all()}
        return render(request, self.template_name, context)


def myzeum(request):
    halls = models.Hall.objects.all()
    exhibits = models.Exhibit.objects.all()
    exhibitions = models.Exhibitions.objects.all()
    employees = models.Employee.objects.all()
    today_date = datetime.now(pytz.timezone('UTC'))
    main_date = today_date - timedelta(days=180)

    show_recent_exhibits = request.GET.get('show_recent_exhibits', False)

    content = {"halls": halls, "exhibits": exhibits, "exhibitions": exhibitions, "employees": employees,
               'today_date': today_date, 'show_recent_exhibits': show_recent_exhibits, 'main_date': main_date}
    return render(request, "main/muzeum.html", content)


def exhibitions(request):
    halls = models.Hall.objects.all()
    exhibits = models.Exhibit.objects.all()
    exhibition = models.Exhibitions.objects.all()
    employees = models.Employee.objects.all()
    content = {"halls": halls, "exhibits": exhibits, "exhibitions": exhibition, "employees": employees}
    return render(request, "main/exhibitions.html", content)


class ProfileClientView(View):
    template_name = 'main/profile.html'
    context = 0

    def get(self, request):
        current_user = models.Client.objects.get(user=request.user)
        orders = mod.Order.objects.filter(client=current_user)

        tz = tzlocal.get_localzone()
        local_time = datetime.now(tz)
        now_time = datetime.now(tz)
        utc_time = datetime.now(tz=pytz.timezone('UTC'))

        text_cal = calendar.month(local_time.year, local_time.month)

        self.context = {
            'current_user': current_user,
            'orders': orders,
            'user_timezone': tz,
            'current_date_formatted': now_time.strftime("%m-%d-%Y %H:%M:%S %Z"),
            'calendar_text': text_cal,
            'utc_time': utc_time.strftime("%m-%d-%Y %H:%M:%S %Z"),
        }

        return render(request, self.template_name, self.context)


class ProfileEmployeeView(View):
    template_name = 'main/profile.html'

    def get(self, request):
        current_user = models.Employee.objects.get(user=request.user)
        exhibits = current_user.exhibits.all()
        exhibitionss = current_user.exhibitions.all()
        tz = tzlocal.get_localzone()
        local_time = datetime.now(tz)
        now_time = datetime.now(tz)
        utc_time = timezone.now().strftime('%d-%m-%Y %H:%M:%S')
        text_cal = calendar.month(local_time.year, local_time.month)

        context = {
            'current_user': current_user,
            'user_timezone': tz,
            'current_date_formatted': now_time.strftime("%d-%m-%Y %H:%M:%S %Z"),
            'calendar_text': text_cal,
            'utc_time': utc_time,
            'exhibit_for_employee': exhibits,
            'exhibition_for_employee': exhibitionss,
        }
        # for order in orders_by_client:
        #     print(order.client)

        return render(request, self.template_name, context)


class AddOrderView(View):
    template_name = "main/add_something.html"
    form_class = OrderForm
    success_url = reverse_lazy('client_profile')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.data)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = models.Client.objects.get(user=request.user)
            # order.date_time = datetime.now(timezone.utc)
            order.save()

            logger.info(f'Order was added')

            return redirect(self.success_url)

        context = {'form': self.form_class}

        logger.info(f'Order was NOT added')

        return render(request, self.template_name, context)


class OrderDetailView(View):
    template_name = "main/order_details.html"

    def get(self, request, pk):
        order = mod.Order.objects.get(pk=pk)
        exhibition = models.Exhibitions.objects.filter(order=order)
        context = {'order': order,
                   'exhibitions': exhibition}

        return render(request, self.template_name, context)


class AddExhibitionsView(View):
    template_name = "main/add_something.html"
    form_class = ExhibitionsForm
    success_url = reverse_lazy('client_profile')

    def get(self, request, pk):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            exhibition = models.Exhibitions(
                service_type=form.cleaned_data['service_type'],
                number=form.cleaned_data['number'],
            )
            exhibition.save()
            order = models.Order.objects.filter(pk=pk)[0]
            order.exhibitions.add(exhibition)
            # order_discount = (100 - (order.discounts.all()[0] + order.bonus.all()[0])) / 100
            # order.total_price += service.number * (service.service_type.price * order_discount)

            order.save()

            logger.info(f'Service was added')

            # order.total_price = order.get_total_price()
            # order.save()
            return redirect(self.success_url)

        logger.info(f'Service was NOT added')

        return render(request, self.template_name, {'form': form})


class AddExhibitionsTypeView(View):
    template_name = "main/add_something.html"
    form_class = ExhibitionsTypeForm
    success_url = reverse_lazy('exhibitions')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.data)

        if form.is_valid():
            form.save()

            logger.info(f'Service type was added')

            return redirect(self.success_url)

        logger.info(f'Service type was NOT added')

        return render(request, self.template_name, {'form': form})
#
# class ExhibitionsTypesView(View):
#     template_name = "main/services.html"
#
#     def get(self, request):
#         context = {'service_types': models.ServiceType.objects.all().order_by('-price')}
#         return render(request, self.template_name, context)

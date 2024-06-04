from datetime import datetime
from statistics import median, mean, mode

from django.db.models import Q, Avg, Max, Count, Sum, Prefetch, ExpressionWrapper, DecimalField, F
from django.db.models import FloatField

import matplotlib.pyplot as plt
import io
import base64
from urllib import parse
from collections import Counter
from main.models import Order
from myzei.models import Client, Exhibitions


# def get_orders_sorted_by_clients_and_dates():
#     orders_prefetch = Prefetch('order_set', queryset=Order.objects.order_by('date_time'))
#     clients_with_order_count = Client.objects.annotate(order_count=Count('order')).prefetch_related(
#         orders_prefetch)
#
#     return clients_with_order_count


def client_age_median():
    obj = Client.objects.filter(~Q(user__age=None))
    return median(obj.values_list('user__age', flat=True))


def client_age_mode():
    obj = Client.objects.filter(~Q(user__age=None))
    return mode(obj.values_list('user__age', flat=True))


def client_age_mean():
    obj = Client.objects.filter(~Q(user__age=None))
    return mean(obj.values_list('user__age', flat=True))

def get_order_with_highest_price():
    orders = Order.objects.all()

    if not orders:
        return None

    orders_with_prices = [(order, order.get_total_price()) for order in orders]
    sorted_orders = sorted(orders_with_prices, key=lambda x: x[1], reverse=True)
    highest_price_order = sorted_orders[0][0] if sorted_orders else None

    return highest_price_order.get_total_price()

def get_most_popular_exhibition():
    orders = Order.objects.all()
    order_names = [order.exhibitions.name for order in orders]
    count_dict = Counter(order_names)
    most_common_word = max(count_dict, key=count_dict.get)
    return most_common_word


def plot_halls():
    exhibition_counts = Exhibitions.objects.values('hall__name').annotate(total=Sum('people'))

    # Извлекаем названия залов и количество посетителей
    hall_names = [ec['hall__name'] for ec in exhibition_counts]
    visitor_counts = [ec['total'] for ec in exhibition_counts]

    # Создаем фигуру и график
    plt.figure(figsize=(10, 6))
    plt.bar(hall_names, visitor_counts)
    plt.xlabel('Name of hall')
    plt.ylabel('Number of visitors')
    plt.title('Hall occupancy')
    plt.xticks(rotation=45, ha='right')

    # Добавляем значения на столбцы
    for i, count in enumerate(visitor_counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    # Преобразуем график в формат base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = parse.quote(string)

    return url

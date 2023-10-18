from django.shortcuts import render
from django.http import HttpResponse
from pytz import timezone

# Create your views here.

def index(request):
    return HttpResponse("Hello World django")


def formatt_date_br(date):
    """
    Formata uma data e hora para o fuso horário de São Paulo.

    Args:
        data (datetime.datetime): O objeto de data e hora a ser formatado.

    Returns:
        datetime.datetime: O objeto de data e hora formatado no fuso horário de São Paulo.    
    """
    date_br = date.astimezone(timezone('America/Sao_Paulo'));
    formatted_date_br = date_br.strftime('%d/%m/%Y %H:%M:%S'); # Pra garantir que vai seguir este formato sempre
    return formatted_date_br

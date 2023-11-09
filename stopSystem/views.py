from django.conf import settings
from django.http import HttpResponse
from pytz import timezone
import subprocess
from django.contrib.auth.decorators import login_required

# from .signals import log_agricola
from .signals import fleet_create
from django.shortcuts import redirect


# # Create your views here.


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
    date_br = date.astimezone(timezone("America/Sao_Paulo"))
    formatted_date_br = date_br.strftime("%d/%m/%Y %H:%M:%S")
    # Pra garantir que vai seguir este formato sempre
    return formatted_date_br


# @login_required
def streamilit_view(request):
    # Especifique o caminho completo para o arquivo dashboards.py
    path_to_dashboards = settings.BASE_DIR / "streamlit_apps/dashboards.py"
    print("Caminho para dashboards.py:", path_to_dashboards)

    port = 8510

    # Adicione as opções para execução do Streamlit
    command = [
        "streamlit",
        "run",
        str(path_to_dashboards),
        "--server.headless",
        "true",
        "--server.enableCORS",
        "true",
        "--server.port",
        str(port),
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    endereco = "http://localhost:8510"
    # Obtenha a saída do Streamlit e retorne como resposta HTTP
    # output = result.stdout
    output = (
        f'<iframe src="{endereco}" width="100%" height="700" frameborder="0"></iframe>'
    )

    return HttpResponse(output)

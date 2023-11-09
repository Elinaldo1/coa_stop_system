from django import forms
from django.db.models import Subquery, OuterRef
from django.shortcuts import render
from django.utils import timezone
from typing import Any
from django.utils.translation import ngettext
from django.contrib import admin, messages
from django.contrib.admin.filters import SimpleListFilter
from .models import Fleet, Front, NewView, TypeLog
from .models import Operation
from .models import Location
from .models import LogAgricola
from .models import Category
from .models import StatusFleet
from .models import StopReason
from .models import StopGroup
from .models import Produto

# from .models import OnLogFleet
from . import views
from django.utils.translation import gettext as _


from django.http import HttpResponse
from openpyxl import Workbook

from django.db import models


class CreateLogAgricolaForm(forms.Form):
    status = forms.ModelChoiceField(queryset=StatusFleet.objects.all())
    description = forms.CharField(widget=forms.Textarea, required=False)
    stopReason = forms.ModelChoiceField(queryset=StopReason.objects.all())


def create_log_agricola(self, request, queryset):
    # Não funciona, pois esta ação é executada para renderizar o form.
    # quando dá o submit no form, ela já foi executada, então apenas fecha o form
    # e retorna tela de logs
    print("aplicando múltiplos inserts")
    print(request.POST)
    form = None
    fleets = []

    if "apply" in request.POST:
        print("aplicando múltiplos inserts")
        form = CreateLogAgricolaForm(request.POST)
        if form.is_valid():
            print("aplicando múltiplos inserts => form valido")
            for fleet in queryset:
                LogAgricola.objects.create(
                    fleetId=fleet.fleetId,
                    category_id=fleet.category_id,
                    status=form.cleaned_data["status"],
                    description=form.cleaned_data["description"],
                    stopReason=form.cleaned_data["stopReason"],
                    operationFront=form.cleaned_data["operationFront"],
                )
            self.message_user(request, "Registros de LogAgricola criados com sucesso.")
            return

    if not form:
        form = CreateLogAgricolaForm()

    return render(
        request,
        "stopSystem/create_log_agricola.html",
        {"form": form, "fleets": queryset, "opts": self.model._meta},
    )


create_log_agricola.short_description = (
    "Criar registros de LogAgricola para itens selecionados"
)


def exportar_para_xlsx(modeladmin, request, queryset):
    # Crie um objeto Workbook do openpyxl
    wb = Workbook()
    ws = wb.active

    # Defina o cabeçalho das colunas
    ws.append(
        ["frota", "frente", "stopReason", "description"]
    )  # Substitua pelos nomes reais dos campos do seu modelo

    # Preencha o restante das linhas com os dados do queryset
    for objeto in queryset:
        ws.append(
            [
                objeto.fleetId.fleet,
                objeto.operationFront.name,
                objeto.stopReason.reason,
                objeto.description,
                objeto.createdAt,
                objeto.updatedAt,
            ]
        )  # Substitua pelos nomes reais dos campos do seu modelo
    # Configure o nome do arquivo e o tipo de resposta
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=exportacao.xlsx"

    # Salve o arquivo Excel na resposta HTTP
    wb.save(response)

    return response


exportar_para_xlsx.short_description = "Exportar selecionados para XLSX"


@admin.action(description="alterar decrição para teste")
def alter_desc(self, request, queryset):
    queryset.update(description="testeeeeeeeeee")


class ReadOnlyAdminLogMixin:
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                "updatedAt",
                "fleetId",
                "stopReasonId",
                "categoryId",
                "operationFront",
            )
        return ("createdAt",)


class LogAgricolaAdmin(ReadOnlyAdminLogMixin, admin.ModelAdmin):
    list_display = [
        "fleet_id_display",
        "typeLog_display",
        "operation_display",
        # "stop_reason_display",
        "description",
        "dt_hh_createdAt",
        "dt_hh_updatedAt",
        "teste",
    ]
    # list_display = [
    #     "fleet_id_display",
    #     "typeLog_display",
    #     "operation_display",
    #     "operationFront",
    #     "stop_reason_display",
    #     "description",
    #     "dt_hh_createdAt",
    #     "dt_hh_updatedAt",
    #     "teste",
    # ]
    list_filter = ("typeLogId__type",)
    actions = [alter_desc, exportar_para_xlsx, create_log_agricola]
    # raw_id_fields = (
    #     "fleetId",
    #     "stopReason",
    #     "operationFront",
    #     "category_id",
    #     "operationFront",
    #     "status",
    # )
    search_fields = ("fleetId__fleet",)
    ordering = ("-id",)

    def operation_display(self, obj):
        return obj.operationId.operation  # Acessa o valor do campo ForeignKey

    operation_display.short_description = "Operacao"

    def fleet_id_display(self, obj):
        return obj.fleetId.fleet  # Acessa o valor do campo ForeignKey

    fleet_id_display.short_description = "Frota"

    def typeLog_display(self, obj):
        return obj.typeLogId.type  # Acessa o valor do campo ForeignKey

    typeLog_display.short_description = "Tipo de Log"

    def stop_reason_display(self, obj):
        return obj.stopReasonId.reason  # Acessa o valor do campo ForeignKey stopReason

    stop_reason_display.short_description = "Motivo Parada"

    def get_raw_id_display(self, obj, values):
        fleetId = Fleet.objects.get(pk=values[0])
        stopReasonId = StopReason.objects.get(pk=values[1])
        return f"{fleetId.fleet} by {stopReasonId.reason}"

    def teste(self, obj):
        if obj.updatedAt is not None:
            difference = obj.updatedAt - obj.createdAt
            return difference
        else:
            return obj.updatedAt

    teste.short_description = "stop_temp"

    def dt_hh_createdAt(sef, obj):
        return views.formatt_date_br(obj.createdAt)

    dt_hh_createdAt.short_description = "dT_início"

    def dt_hh_updatedAt(sef, obj):
        if obj.updatedAt is not None:
            return views.formatt_date_br(obj.updatedAt)
        else:
            return "EM ABERTO"

    dt_hh_updatedAt.short_description = "dt_fim"


class StatusFilter(SimpleListFilter):
    """
    Filtro personalizado para o status de um Log.

    Este filtro permite selecionar itens com base no status "EM ABERTO" ou "FECHADO".\n
    Quando o campo updatedAt do Log está null ou com uma data setada.
    """

    title = "STATUS"
    parameter_name = "dt_hh_updatedAt"

    def lookups(self, request, model_admin):
        """
        Retorna as opções de filtro disponíveis.

        Returns:
            list: Uma lista de tuplas contendo os valores de filtro e seus rótulos.
        """
        return (
            (True, "EM ABERTO"),
            (False, "FECHADO"),
        )

    def queryset(self, request: Any, queryset):
        """
        Realiza a filtragem com base no valor selecionado pelo usuário.

        Args:
            request: O objeto de solicitação.
            queryset: O queryset original.

        Returns:
            QuerySet: O queryset filtrado com base na seleção do usuário.
        """
        selected_value = self.value()
        if selected_value:
            selected_value = selected_value == "True"
            return queryset.filter(updatedAt__isnull=selected_value)

        return queryset


class OperationFilter(admin.SimpleListFilter):
    """
    Filtro personalizado para a operação de um Log.

    """

    title = "Operação"
    parameter_name = "operation"

    def lookups(self, request, model_admin):
        operations = Operation.objects.all()
        lookup_choices = [
            (str(operation.id), operation.operation) for operation in operations
        ]
        return lookup_choices

    def queryset(self, request, queryset):
        selected_value = self.value()
        if selected_value:
            return queryset.filter(operationFront=selected_value)
        return queryset


class Status2Filter(admin.SimpleListFilter):
    """
    Filtro personalizado para o tipo de log(PARADA, NOTIFICAÇÂO) de um Log.

    """

    title = "Tipo de Log"
    parameter_name = "typeLogId"

    def lookups(self, request, model_admin):
        typeLog = TypeLog.objects.all()

        # ===AJUST AQUI===
        lookup_choices = [(str(status.id), status.status) for status in typeLog]
        return lookup_choices

    def queryset(self, request, queryset):
        selected_value = self.value()
        if selected_value:
            return queryset.filter(status=selected_value)
        return queryset


"""

"""


class OnLogFleetAdmin(admin.ModelAdmin):
    """
    Uma view do banco que retorna o Log mais recente de cada frota

    Args:

    Attributes:

    Methods:
        - operation_display(self, obj): Obtém e retorna o valor do campo 'operation' da relação ForeignKey 'operationFront' no objeto 'Log'.

    """

    list_display = [
        "fleet_id_display",
        "category_display",
        "status_display",
        "operation_display",
        "operationFront",
        "stop_reason_display",
        "description",
        "dt_hh_createdAt",
        "dt_hh_updatedAt",
        "time_stop_opened",
    ]

    list_filter = [
        "fleetId",
        OperationFilter,
        StatusFilter,
        Status2Filter,
        "category_id",
        "stopReason",
    ]

    actions = [alter_desc, exportar_para_xlsx]
    raw_id_fields = (
        "fleetId",
        "stopReason",
        "operationFront",
        "category_id",
        "operationFront",
        "status",
    )
    search_fields = ("fleetId__fleet", "stopReason__reason", "description")
    ordering = ("-id",)

    def operation_display(self, obj):
        """
        Returns:
            O valor do campo 'operation' da relação ForeignKey 'operationFront' no objeto 'Log'.
        """
        return obj.operationFront.operation

    operation_display.short_description = "Operacao"

    def category_display(self, obj):
        return obj.category_id.name

    category_display.short_description = "Categoria"

    def fleet_id_display(self, obj):
        return obj.fleetId.fleet

    fleet_id_display.short_description = "Frota"

    def status_display(self, obj):
        return obj.status.status

    status_display.short_description = "Status"

    def stop_reason_display(self, obj):
        return obj.stopReason.reason  # Acessa o valor do campo ForeignKey stopReason

    stop_reason_display.short_description = "Motivo Parada"

    def get_raw_id_display(self, obj, values):
        fleetId = Fleet.objects.get(pk=values[0])
        stopReason = StopReason.objects.get(pk=values[1])
        return f"{fleetId.fleet} by {stopReason.reason}"

    def time_stop_opened(self, obj):
        if obj.updatedAt is not None:
            difference = obj.updatedAt - obj.createdAt
            return difference
        else:
            difference = timezone.now() - obj.createdAt
            return difference

    time_stop_opened.short_description = "stop_temp"

    def dt_hh_createdAt(sef, obj):
        return views.formatt_date_br(obj.createdAt)

    dt_hh_createdAt.short_description = "dT_início"

    def dt_hh_updatedAt(sef, obj):
        if obj.updatedAt is not None:
            return views.formatt_date_br(obj.updatedAt)
        else:
            return "EM ABERTO"

    dt_hh_updatedAt.short_description = "dt_fim"


class NewViewAdmin(admin.ModelAdmin):
    actions = []  # não exibe actions para o user executar
    list_display = ["frente"]
    readonly_fields = ["frente"]


class StopReasonAdmin(admin.ModelAdmin):
    list_display = ["id", "reason", "group"]
    ordering = ["reason"]


# Transform isto em uma view no banco
# class OperationFrontAdmin(admin.ModelAdmin):
#      list_display = ['name', 'operation', 'location']
#      ordering = ['operation', 'name']


class ReadOnlyAdminFleetMixin:
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                "updatedAt",
                "fleet",
                "stopReasonId",
                "operationId",
                "categoryId",
                "frontId",
                "statusId",
            )
        return ("createdAt",)


class FleetForm(forms.ModelForm):
    class Meta:
        model = Fleet
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        status_id = cleaned_data.get("statusId")
        stop_reason_id = cleaned_data.get("stopReasonId")

        if status_id and status_id.isRequiredStopReason and not stop_reason_id:
            self.add_error(
                "stopReasonId",
                "Este campo é obrigatório quando está parando uma frota.",
            )


class FleetAdmin(ReadOnlyAdminFleetMixin, admin.ModelAdmin):
    form = FleetForm
    actions = ["alter_desc"]
    raw_id_fields = ("stopReasonId", "statusId")
    list_display = (
        "fleet",
        "categoryId",
        "statusId",
        "stopReasonId",
        "operationId",
        "frontId",
        "locationId",
        "description",
    )
    list_filter = (
        "statusId__typeLog",
    )  # Filtrar com base no typeLog relacionado de StatusFleet
    search_fields = (
        "fleet",
        "categoryId__name",
        "statusId__status",
        "stopReasonId__reason",
        "operationId__operation",
        "frontId__front",
        "locationId__location",
    )

    @admin.action(description="Ativar frotas paradas")
    def alter_desc(self, request, queryset):
        # Filtra apenas os registros que selecionados que estão parados
        queryset = queryset.filter(
            statusId__typeLog__isStop=True
        )  # retorna todos os campos
        querysetIds = queryset.filter(statusId__typeLog__isStop=True).values(
            "id"
        )  # retorna o id

        # Subconsulta para obter os IDs dos logs mais recentes
        lastLogOfFleet = (
            LogAgricola.objects.filter(fleetId=OuterRef("fleetId"))
            .order_by("id")
            .values("id")[:1]
        )

        # Atualiza os logs de parada mais recentes de cada frota
        LogAgricola.objects.filter(
            fleetId__in=Subquery(querysetIds), id__in=Subquery(lastLogOfFleet)
        ).update(updatedAt=timezone.now(), description="ISTo deve ficar vazio")

        updated_count = queryset.update(description="liberar frota")
        # updated_count = querysetIds.update(description="testando liberar frota") # ver pq não funfa

        # Apenas
        # updated_count = 0
        # for obj in queryset:
        #     if obj.statusId.typeLog.isStop:
        #         obj.description = "super"
        #         obj.save()
        #         updated_count += 1

        self.message_user(
            request,
            ngettext(
                # %d: Este é um marcador de espaço reservado para um número inteiro
                # O valor real de updated será inserido no lugar de %d.
                "%d registro foi atualizado.",
                "%d registros foram atualizados.",
                updated_count,
            )
            % updated_count,
            messages.SUCCESS,
        )

    def get_actions(self, request):
        """
        Remove the action delete
        """
        actions = super().get_actions(request)
        del actions["delete_selected"]
        # if request.user.username[0].upper() == "J":
        #     if "delete_selected" in actions:
        return actions

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(FleetAdmin, self).get_form(request, obj, **kwargs)

    #     if (
    #         obj
    #         and hasattr(obj, "statusId")
    #         and not obj.statusId.typeLog.isRequiredStopReason
    #     ):
    #         print("Estou criando a frota e o motivo não é requerido")
    #         # Se o typeLog associado a este status não requer um motivo de parada, torne o campo stopReason opcional
    #         for field_name, field in form.base_fields.items():
    #             if field_name == "stopReasonId":
    #                 field.required = False

    #     print("verificando se o campo é obrigatório2")
    #     if obj:
    #         print(obj.statusId.typeLog.isRequiredStopReason)
    #     if obj and not obj.statusId.typeLog.isRequiredStopReason:
    #         print("typeLog.isRequiredStopReason = false")
    #         # Se o typeLog associado a este status não requer um motivo de parada, torne o campo stopReason opcional
    #         for field_name, field in form.base_fields.items():
    #             if field_name == "stopReasonId":
    #                 print("estou no campo stop")
    #                 field.required = False

    #     return form


class StatusFleetAdmin(admin.ModelAdmin):
    list_display = ["status", "typeLog_display", "isRequiredStopReason_display"]

    def typeLog_display(self, obj):
        return obj.typeLog.type

    typeLog_display.short_description = "Tipo Log"

    def isRequiredStopReason_display(self, obj):
        return obj.isRequiredStopReason

    isRequiredStopReason_display.short_description = "Requer Motivo Parada"


class ProdutoAdmin(admin.ModelAdmin):
    # Configurações do admin

    list_display = ["produto", "quantidade"]
    list_filter = ["produto"]

    class Media:
        css = {"all": ["admin_total.css"]}
        js = [
            "admin_total.js"
        ]  # Substitua 'admin_totals.js' pelo caminho correto para o seu arquivo JavaScript


admin.site.register(Produto, ProdutoAdmin)
# admin.site.register(PostTeste)
# admin.site.register(OnLogFleet)
# admin.site.register(OnLogFleet, OnLogFleetAdmin)#ajustar
admin.site.register(NewView)
# admin.site.register(NewView, NewViewAdmin)#ajustar
# admin.site.register(Post)
admin.site.register(Fleet, FleetAdmin)
# admin.site.register(OperationFront, OperationFrontAdmin)#ajustar
admin.site.register(Operation)
admin.site.register(Location)
# admin.site.register(LogAgricola)
admin.site.register(LogAgricola, LogAgricolaAdmin)  # ajustar
admin.site.register(Category)
admin.site.register(StatusFleet, StatusFleetAdmin)
admin.site.register(StopReason, StopReasonAdmin)
admin.site.register(StopGroup)
admin.site.register(TypeLog)
admin.site.register(Front)

from typing import Any
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from .models import Fleet
from .models import OperationFront
from .models import Operation
from .models import Location
from .models import LogAgricola
from .models import Category
from .models import StatusFleet
from .models import StopReason
from .models import StopGroup
from .models import OnLogFleet
from . import  views


from django.http import HttpResponse
from openpyxl import Workbook

def exportar_para_xlsx(modeladmin, request, queryset):

    # Crie um objeto Workbook do openpyxl
    wb = Workbook()
    ws = wb.active

    # Defina o cabeçalho das colunas
    ws.append(['frota', 'frente', 'stopReason', 'description'])  # Substitua pelos nomes reais dos campos do seu modelo

    # Preencha o restante das linhas com os dados do queryset
    for objeto in queryset:
        ws.append([
             
            objeto.fleetId.fleet, objeto.operationFront.name, objeto.stopReason.reason, objeto.description, objeto.createdAt, objeto.updatedAt
        ])  # Substitua pelos nomes reais dos campos do seu modelo
    # Configure o nome do arquivo e o tipo de resposta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exportacao.xlsx'

    # Salve o arquivo Excel na resposta HTTP
    wb.save(response)

    return response

exportar_para_xlsx.short_description = 'Exportar selecionados para XLSX'

    
@admin.action(description='alterar decrição para teste')
def alter_desc(self, request, queryset ):
        queryset.update(description="testeeeeeeeeee")


class ReadOnlyAdminLogMixin:

     def get_readonly_fields(self, request, obj=None):

          if obj:
               return ('createdAt', 'fleetId', 'stopReason', 'operationFront', 'category_id', 'operationFront', 'status')
          return('updatedAt',)


class LogAgricolaAdmin(ReadOnlyAdminLogMixin, admin.ModelAdmin):
    list_display = ['fleet_id_display', 'status_display', 'operation_display', 'operationFront', 'stop_reason_display', 'description', 'dt_hh_createdAt', 'dt_hh_updatedAt', 'teste']
    list_filter = ('fleetId', 'stopReason')
    actions = [alter_desc, exportar_para_xlsx]
    raw_id_fields = ('fleetId', 'stopReason', 'operationFront', 'category_id', 'operationFront', 'status')
    search_fields = ('fleetId__fleet', 'operation' 'stopReason__reason')
    ordering = ('-id',)

    def operation_display(self, obj):
        return obj.operationFront.operation  # Acessa o valor do campo ForeignKey fleetId
    operation_display.short_description = 'Operacao'


    def fleet_id_display(self, obj):
        return obj.fleetId.fleet  # Acessa o valor do campo ForeignKey fleetId
    fleet_id_display.short_description = 'Frota'


    def status_display(self, obj):
        return obj.status.status  # Acessa o valor do campo ForeignKey fleetId
    status_display.short_description = 'Status'

    def stop_reason_display(self, obj):
        return obj.stopReason.reason  # Acessa o valor do campo ForeignKey stopReason
    stop_reason_display.short_description = 'Motivo Parada'


    def get_raw_id_display(self, obj, values):
         fleetId = Fleet.objects.get(pk=values[0])
         stopReason = StopReason.objects.get(pk=values[1])
         return f"{fleetId.fleet} by {stopReason.reason}"

     
    def teste(self, obj):

        if obj.updatedAt is not None:
             difference = obj.updatedAt - obj.createdAt
             return difference
        else:
             
            return obj.updatedAt
    teste.short_description = 'stop_temp'
    
    def dt_hh_createdAt(sef, obj):
         return  views.formatt_date_br(obj.createdAt);
    dt_hh_createdAt.short_description = 'dT_início'

    def dt_hh_updatedAt(sef, obj):
         if obj.updatedAt is not None:
            return views.formatt_date_br(obj.updatedAt);
         else:
              return 'EM ABERTO'
         
    dt_hh_updatedAt.short_description = 'dt_fim'


class OperationsFilter(SimpleListFilter):
    title = 'Motivos'
    parameter_name = 'stopReason'

    def lookups(self, request, model_admin):
        print ('lookups')
        return (
            ('stopReason', 'stopReasonssss'),
            ('stopReason2', 'stopReasonssss2'),
        )
    def queryset(self, request: Any, queryset):
        print(queryset)
        return queryset

class OnLogFleetAdmin(admin.ModelAdmin):
    list_display = ['fleet_id_display', 'status_display', 'operation_display', 'operationFront', 'stop_reason_display', 'description', 'dt_hh_createdAt', 'dt_hh_updatedAt', 'teste']
    # list_filter = ('fleetId', OperationsFilter)
    actions = [alter_desc, exportar_para_xlsx]
    raw_id_fields = ('fleetId', 'stopReason', 'operationFront', 'category_id', 'operationFront', 'status')
    search_fields = ('fleetId__fleet', 'operation', 'stopReason__reason')
    ordering = ('-id',)

    def operation_display(self, obj):
        return obj.operationFront.operation  # Acessa o valor do campo ForeignKey fleetId
    operation_display.short_description = 'Operacao'


    def fleet_id_display(self, obj):
        return obj.fleetId.fleet  # Acessa o valor do campo ForeignKey fleetId
    fleet_id_display.short_description = 'Frota'

    def status_display(self, obj):
        return obj.status.status  # Acessa o valor do campo ForeignKey fleetId
    status_display.short_description = 'Status'

    def stop_reason_display(self, obj):
        return obj.stopReason.reason  # Acessa o valor do campo ForeignKey stopReason
    stop_reason_display.short_description = 'Motivo Parada'


    def get_raw_id_display(self, obj, values):
         fleetId = Fleet.objects.get(pk=values[0])
         stopReason = StopReason.objects.get(pk=values[1])
         return f"{fleetId.fleet} by {stopReason.reason}"

     
    def teste(self, obj):

        if obj.updatedAt is not None:
             difference = obj.updatedAt - obj.createdAt
             return difference
        else:
             
            return obj.updatedAt
    teste.short_description = 'stop_temp'
    
    def dt_hh_createdAt(sef, obj):
        return views.formatt_date_br(obj.createdAt)
    dt_hh_createdAt.short_description = 'dT_início'

    def dt_hh_updatedAt(sef, obj):
         if obj.updatedAt is not None:
            return views.formatt_date_br(obj.updatedAt)
         else:
              return 'EM ABERTO'
         
    dt_hh_updatedAt.short_description = 'dt_fim'

class NewViewAdmin(admin.ModelAdmin):
    actions = [] # não exibe actions para o user executar
    list_display = ['frente']
    readonly_fields = ['frente']
    

class StopReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'reason', 'group']
    ordering = ['reason']



class OperationFrontAdmin(admin.ModelAdmin):
     list_display = ['name', 'operation', 'location']
     ordering = ['operation', 'name']



# class PostTesteAdminForm(forms.ModelForm):
#     class Meta:
#         model = PostTeste
#         fields = '__all__'

#     def clean_title(self):
#         title = self.cleaned_data.get('title')
#         if len(title) < 10:
#             raise ValidationError('O título deve ter pelo menos 10 caracteres.')
#         return title

# class PostTesteAdmin(admin.ModelAdmin):
#     form = PostTesteAdminForm


# class PostTesteAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         try:
#             obj.full_clean()
#         except ValidationError as e:
#             form._errors = {'title': e.message_dict['title']}
#             return super().save_model(request, obj, form, change)

#         super().save_model(request, obj, form, change)

# admin.site.register(PostTeste, PostTesteAdmin)



# admin.site.register(PostTeste)
admin.site.register(OnLogFleet, OnLogFleetAdmin)
# admin.site.register(NewView, NewViewAdmin)
# admin.site.register(Post)
admin.site.register(Fleet)
admin.site.register(OperationFront, OperationFrontAdmin)
admin.site.register(Operation)
admin.site.register(Location)
admin.site.register(LogAgricola, LogAgricolaAdmin)
admin.site.register(Category)
admin.site.register(StatusFleet)
admin.site.register(StopReason, StopReasonAdmin)
admin.site.register(StopGroup)
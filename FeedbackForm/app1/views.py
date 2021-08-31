from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import FormCreateForm, FormChoiceMaker
from .models import TempModel
from django.db import connection


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = FormCreateForm
        return context

    def post(self, request):
        request.session['name'] = self.request.POST.get('title')
        return HttpResponseRedirect('/formmaker')


class FormMake(TemplateView):
    template_name = 'formcreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['name'] = FormChoiceMaker
        context['data'] = TempModel.objects.all()
        return context

    def post(self, request):
        data = TempModel(question=self.request.POST.get('question'), type=self.request.POST.get('type'),
                         options=self.request.POST.get('options'))
        data.save()
        return HttpResponseRedirect("/formmaker")


def add(request):
    data = TempModel.objects.all()
    cursor = connection.cursor()
    fields = {"1": "varchar(255)", "2": "varchar(255)", "3": "varchar(255)", "4": "varchar(255)", "5": "varchar(255)"}
    html_fields = {"1": "text"}
    temper = ''
    html_temp = ''
    for i in data:
        html_temp += f'<label> {i.question} </label> <input type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}"> <br> '
        temper += f'{i.question.replace(" ", "_")} {fields[i.type]},'
    cursor.execute(
        f"CREATE TABLE if not exists {request.session['name']} ({temper[:-1]})")
    print(html_temp)
    TempModel.objects.all().delete()
    #return render(request, "formtest.html", {"form": f"<form> {html_temp} </form>"})
    return HttpResponse(f"<form> {html_temp} </form>")

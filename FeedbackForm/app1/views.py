from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import FormCreateForm, FormChoiceMaker
from .models import TempModel
from django.db import connection

count = 1


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
        global count
        data = TempModel(s_no=count, question=self.request.POST.get('question'), type=self.request.POST.get('type'),
                         options=self.request.POST.get('options'))
        data.save()
        count += 1
        return HttpResponseRedirect("/formmaker")


def add(request):
    global count
    data = TempModel.objects.all()
    cursor = connection.cursor()
    fields = {"1": "varchar(255)", "2": "varchar(255)", "3": "varchar(255)", "4": "varchar(255)", "5": "varchar(255)"}
    html_fields = {"1": "text", "2": "radio", "3": "checkbox", "4": "radio",  "5": "radio"}
    temper = ''
    html_temp = ''
    for i in data:
        if html_fields[i.type] == "text":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label> <input class="form-control" type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}"> <br>'
        elif html_fields[i.type] == "radio":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label> <input class="form-control" type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}"> <br>'
        temper += f'{i.question.replace(" ", "_")} {fields[i.type]},'
    if temper:
        cursor.execute(
            f"CREATE TABLE if not exists {request.session['name']} ({temper[:-1]})")
    else:
        return HttpResponseRedirect('/formmaker')
    print(html_temp, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    TempModel.objects.all().delete()
    count = 1
    return render(request, "test.html", {"test": html_temp})
    # return HttpResponse(html_temp)
    # return render(request, "formcreate.html")

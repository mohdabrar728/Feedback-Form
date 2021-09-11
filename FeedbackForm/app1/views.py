from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import FormCreateForm, FormChoiceMaker, EmailAdderForm
from .models import TempModel, FormTokenModel, EmailTokenModel
from django.db import connection
from .tokens import account_activation_token
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

count = 1


def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/')


def mylogin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/home')
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/home')


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # TempModel.objects.all().delete()
        # FormTokenModel.objects.all().delete()
        # EmailTokenModel.objects.all().delete()
        context = super().get_context_data()
        context['form'] = FormCreateForm
        context['home'] = 'btn-dark'
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
        context['home'] = "btn-dark"
        return context

    def post(self, request):
        global count
        if "None" != self.request.POST.get('type'):
            print(self.request.POST.get('type'))
            data = TempModel(s_no=count, question=self.request.POST.get('question'), type=self.request.POST.get('type'),
                             options=self.request.POST.get('options'))
            data.save()
            count += 1
        return HttpResponseRedirect("/formmaker")


cursor = connection.cursor()


def add(request):
    global count
    data = TempModel.objects.all()
    fields = {"1": "varchar(255)", "2": "varchar(255)", "3": "varchar(255)", "4": "varchar(255)", "5": "varchar(255)"}
    html_fields = {"1": "text", "2": "radio", "3": "checkbox", "4": "radio", "5": "radio"}
    temper = ''
    html_temp = ''
    for i in data:
        if i.type == "1":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label> <input class="form-control" type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}"> <br>'
        elif i.type == "2":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label><br>'
            for opt in i.options.split(','):
                html_temp += f'<input type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}" value={opt} <label >{opt}</label><br>'
            html_temp += "<br>"
        elif i.type == "3":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label><br>'
            for opt in i.options.split(','):
                html_temp += f'<input type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}" value={opt} <label >{opt}</label><br>'
            html_temp += "<br>"
        elif i.type == "4":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label><br>'
            for opt in ['yes', 'no']:
                html_temp += f'<input type="{html_fields[i.type]}" name="{i.question.replace(" ", "_")}" value={opt}> <label >{opt}</label><br> '
            html_temp += f'<input class="form-control" type="text" name="{i.question.replace(" ", "_")}"><br>'
        elif i.type == "5":
            html_temp += f'<label class="form-label">{i.s_no}. {i.question} </label> <br> <textarea ' \
                         f'class="form-control" name="{i.question.replace(" ", "_")}" rows="4" cols="50"></textarea> ' \
                         f'<br> '
        temper += f'{i.question.replace(" ", "_")} {fields[i.type]},'
        print(temper, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    if temper:
        request.session[
            'temper'] = f"CREATE TABLE if not exists {request.session['name'].replace(' ', '_')} ({'email_token varchar(255),' + temper[:-1]}, PRIMARY KEY (email_token))"

    else:
        return HttpResponseRedirect('/formmaker')
    print(temper, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # TempModel.objects.all().delete()
    count = 1
    request.session['code'] = html_temp
    return HttpResponseRedirect('/formcheck')
    # return HttpResponse(html_temp)
    # return render(request, "formcreate.html")


def formcheck(request):
    data = EmailTokenModel.objects.all().filter(form_token=account_activation_token.make_token(request.session['name']))
    return render(request, "formcheck.html",
                  {"test": request.session['code'], "form": EmailAdderForm, "data": data, 'home': 'btn-dark'})


def formtokenview(request):
    if request.method == 'POST':
        form_name = request.session['name']
        form_token = account_activation_token.make_token(request.session['name'])
        form_code = request.session['code']
        request.session['token'] = form_token
        cursor.execute(request.session['temper'])
        data = FormTokenModel(form_name=form_name, form_token=form_token, form_code=form_code)
        data.save()
        TempModel.objects.all().delete()
        return HttpResponseRedirect('/formpreview')


def formpreview(request):
    data = FormTokenModel.objects.all()
    dropform = "<select name='select_form' id='id_select_form' class='form-select'><option value='None'>select an option</option>"
    for i in data:
        dropform += f"<option value='{i.form_name}'>{i.form_name}</option> "
    dropform += "</select>"
    if request.method == 'POST':
        form_name = request.POST.get('select_form')
        request.session['name_from_preview'] = form_name
        try:
            formdata = FormTokenModel.objects.get(form_name=form_name)
        except:
            return HttpResponseRedirect('/formpreview')
        request.session['token'] = formdata.form_token
        form = formdata.form_code
        request.session['code_form_preview'] = form
        return render(request, "formpreview.html", {'dropform': dropform, "form": form, "services": "btn-dark"})
    return render(request, "formpreview.html", {'dropform': dropform, "services": "btn-dark"})


def showmail(request):
    if request.method == 'POST':
        send_mail_data = EmailTokenModel.objects.all().filter(form_token=request.session['token'])
        for smd in send_mail_data:
            # try:
            uidb64 = smd.form_token
            print("uiddb64", uidb64)
            domain = get_current_site(request).domain
            link = reverse(
                'feedbackform', kwargs={'uidb64': uidb64, 'token': smd.email_token}
            )
            mail_subject = 'Submit your Feedback.'
            activate_url = 'http://' + domain + link
            message = 'Hi ' + smd.email_id + 'Please use this link to submit your feedback\n' + activate_url
            to_email = smd.email_id
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send(fail_silently=False)

            data = 'Please confirm your email address to complete the registration your account will be activated'
        # except Exception as error:
        #     user.delete()
        #     data = 'something went wrong unable to send a mail: '.format({error})

    return render(request, "showmail.html", {"email_form": EmailAdderForm,
                                          'data': EmailTokenModel.objects.all().filter(
                                              form_token=request.session['token']), 'home': 'btn-dark'})


def emailtokenview(request):
    if request.method == 'POST':
        data = EmailTokenModel(form_token=request.session['token'], email_id=request.POST.get('email'),
                               email_token=account_activation_token.make_token(request.POST.get('email')))
        data.save()
    return HttpResponseRedirect('/showmail')


def feedbackform(request, uidb64, token):
    formdata = FormTokenModel.objects.get(form_token=uidb64)
    table_name = formdata.form_name
    if request.method == 'POST':
        dicter = dict(request.POST)
        list_value = []
        for i in dicter.keys():
            convert_string = ",".join(dicter[i])
            list_value.append(convert_string)
        tuple_value = (token,) + tuple(list_value[1:])
        tuple_col = (token,) + tuple(list(dicter.keys())[1:])
        print(tuple_col)
        print(tuple_value)
        print(
            f"INSERT INTO feedback_form.{table_name.replace(' ', '_')} {('email_token',) + tuple_col} VALUES {tuple_value};")
        try:
            cursor.execute(
                f"INSERT INTO {table_name.replace(' ', '_')} VALUES {tuple_value};")
            return render(request, "formsubmitted.html")
        except:
            return render(request, "alreadysubmitted.html")
    return render(request, "feedbackform.html", {'form': formdata.form_code, 'table_name': table_name})


def stats(request):
    data = FormTokenModel.objects.all()
    dropform = "<select name='select_form' id='id_select_form' class='form-control'><option value='None'>Select an option</option> "
    for i in data:
        dropform += f"<option value='{i.form_name}'>{i.form_name}</option> "
    dropform += "</select>"
    if request.method == "POST":
        name = request.POST.get('select_form')
        try:
            token_of_form = FormTokenModel.objects.get(form_name=name).form_token
        except:
            return HttpResponseRedirect('/stats')
        total = len(EmailTokenModel.objects.all().filter(form_token=token_of_form))
        submitted = cursor.execute(f"SELECT * FROM {name.replace(' ', '_')}")
        pending = abs(total - submitted)
        try:
            average = (submitted / total) * 100
        except:
            average = 0
        cursor.execute(f"SHOW COLUMNS FROM feedback_form.{name.replace(' ', '_')};")
        data1 = cursor.fetchall()
        field_data1 = []
        for i in data1:
            field_data1.append(i[0])
        cursor.execute(f"SELECT * FROM feedback_form.{name.replace(' ', '_')}")
        data = cursor.fetchall()
        print(data)
        return render(request, "stats.html",
                      {'dropform': dropform, 'total': total, 'submitted': submitted, 'pending': pending,
                       'average': round(average), 'data': data, 'data1': field_data1, 'stats': 'btn-dark'})
    return render(request, "stats.html", {'dropform': dropform, 'stats': 'btn-dark'})


def formdata(request):
    data = FormTokenModel.objects.all()
    dropform = "<select name='select_form' id='id_select_form' class='form-control'><option value='None'>Select an option</option> "
    for i in data:
        dropform += f"<option value='{i.form_name}'>{i.form_name}</option> "
    dropform += "</select>"
    if request.method == "POST":
        name = request.POST.get('select_form')
        try:
            token_of_form = FormTokenModel.objects.get(form_name=name).form_token
        except:
            return HttpResponseRedirect('/formdata')
        cursor.execute(f"SHOW COLUMNS FROM feedback_form.{name.replace(' ', '_')};")
        data1 = cursor.fetchall()
        field_data1 = []
        for i in data1:
            field_data1.append(i[0])
        cursor.execute(f"SELECT * FROM feedback_form.{name.replace(' ', '_')}")
        data = cursor.fetchall()
        mdata = []
        count = 1
        for i in data:
            mdata.append((count,)+i[1:])
            count += 1
        print(mdata, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        return render(request, "formdata.html",
                      {'dropform': dropform, 'data': mdata, 'data1': field_data1, 'formdata': 'btn-dark',
                       'range': range(len(data))})
    return render(request, "formdata.html", {'dropform': dropform, 'formdata': 'btn-dark'})


def clear_tempdata(request):
    global count
    count = 1
    TempModel.objects.all().delete()
    return HttpResponseRedirect('/formmaker')

def cancel(request):
    global count
    count = 1
    TempModel.objects.all().delete()
    return HttpResponseRedirect('/home')

def formclone(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        original_table = request.session['name_from_preview'].replace(' ','_')
        cursor.execute(f"CREATE TABLE {new_name.replace(' ','_')} SELECT * FROM {original_table};")
        cursor.execute(f'DELETE FROM feedback_form.{new_name.replace(" ","_")}')
        form_token = account_activation_token.make_token(new_name)
        form_code = request.session['code_form_preview']
        # request.session['token'] = form_token
        # cursor.execute(request.session['temper'])
        data = FormTokenModel(form_name=new_name, form_token=form_token, form_code=form_code)
        data.save()
    return HttpResponseRedirect('/formpreview')
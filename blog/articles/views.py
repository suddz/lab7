from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Order


def archive(request):
    return render(request, 'archive.html', {"posts": Order.objects.all()})


def get_order(request, order_id):
    try:
        post = Order.objects.get(id=order_id)
        return render(request, 'order.html', {"post": post})
    except Order.DoesNotExist:
        raise Http404


def create_order(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # в словаре form хранится информация, введенная пользователем
            form = {
                'contract': request.POST["contract"],
                'item': request.POST["item"],
                'client': request.POST["client"],
                'phone': request.POST["phone"],
                'branch': request.POST["branch"],
                'service': request.POST["service"],
                'price': request.POST["price"],
                'urgency': request.POST["urgency"],
                'complexity': request.POST["complexity"],
                'discount': request.POST["discount"],
                'receive_date': request.POST["receive_date"],
                'return_date': request.POST["return_date"],
                'text': request.POST["text"],
            }
            required = ['contract', 'item', 'client', 'phone', 'branch', 'service', 'price',
                        'urgency', 'complexity', 'discount', 'receive_date', 'return_date',
                        'text']
            if all(form[name] for name in required):
                # проверка уникальности номера договора
                if Order.objects.filter(contract=form["contract"]).exists():
                    form['errors'] = "Договор с таким номером уже существует"
                    return render(request, 'create_order.html', {'form': form})
                try:
                    # если поля заполнены без ошибок, создается новая запись
                    order = Order.objects.create(
                        contract=form["contract"],
                        item=form["item"],
                        client=form["client"],
                        phone=form["phone"],
                        branch=form["branch"],
                        service=form["service"],
                        price=form["price"],
                        urgency=form["urgency"],
                        complexity=form["complexity"],
                        discount=form["discount"],
                        receive_date=form["receive_date"],
                        return_date=form["return_date"],
                        text=form["text"],
                        author=request.user
                    )
                except (ValueError, ValidationError):
                    form['errors'] = "Проверьте правильность чисел и дат"
                    return render(request, 'create_order.html', {'form': form})
                # переход на страницу созданной записи
                return redirect('get_order', order_id=order.id)
            else:
                # если введенные данные некорректны
                form['errors'] = "Не все поля заполнены"
                return render(request, 'create_order.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_order.html', {})
    else:
        raise Http404


def register(request):
    if request.method == "POST":
        form = {
            'username': request.POST["username"],
            'email': request.POST["email"],
            'password': request.POST["password"],
        }
        if form["username"] and form["email"] and form["password"]:
            try:
                User.objects.get(username=form["username"])
                # если пользователь существует, то ошибки не произойдет
                form['errors'] = "Пользователь с таким именем уже есть"
            except User.DoesNotExist:
                # логин свободен - регистрируем нового пользователя
                User.objects.create_user(form["username"], form["email"], form["password"])
                return redirect('login')
        else:
            form['errors'] = "Не все поля заполнены"
        return render(request, 'register.html', {'form': form})
    else:
        return render(request, 'register.html', {})


def user_login(request):
    if request.method == "POST":
        form = {
            'username': request.POST["username"],
            'password': request.POST["password"],
        }
        if form["username"] and form["password"]:
            user = authenticate(username=form["username"], password=form["password"])
            if user is not None:
                # аутентификация прошла успешно - авторизуем пользователя
                login(request, user)
                return redirect('archive')
            else:
                form['errors'] = "Нет аккаунта с таким сочетанием никнейма и пароля"
        else:
            form['errors'] = "Не все поля заполнены"
        return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {})

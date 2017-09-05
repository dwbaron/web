from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

    # 如果没有POST请求，用户正在注册页面，显示空白注册表单
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form})

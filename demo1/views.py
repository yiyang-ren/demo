from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from demo1.models import Score, Rank


# Create your views here.

# # 登陆
# @csrf_exempt
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = auth.authenticate(username=username, password=password)  # 根据获取的用户名密码去数据库查询，并返回user对象
#         if user is not None and user.is_active:
#             auth.login(request, user)
#             return redirect('upload/')
#         else:
#             return render(request, 'login.html')
#
#
# # 登出
# def logout(request):
#     auth.logout(request)  # 从请求中删除经过身份验证的用户的ID并刷新其会话数据。
#     return redirect('/')


@login_required(login_url='/')
@csrf_exempt
def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html', {'user': request.user, })
    if request.method == 'POST':
        # 接受页面上传的数据
        score = request.POST.get('score', '')
        if score:
            # 获取数据库的数据
            old_scor = Score.objects.filter(client=request.user).first()
            if old_scor:
                if old_scor.score != score:
                    old_scor.score = score
                    old_scor.save()
            else:
                Score.objects.create(client=request.user, score=score)
            # 排名表数据更新
            Rank.objects.all().delete()
            score_li = [score_obj.id for score_obj in Score.objects.all().order_by('-score')]
            n = 1
            for i in score_li:
                Rank.objects.create(c_id_id=i, rank=n)
                n = n + 1
            return JsonResponse({'status': 'sucess'})
        return JsonResponse({'status': 'error'})


@login_required(login_url='/')
@csrf_exempt
def show(request):
    context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                          Score.objects.all().order_by('-score')]}
    if request.method == 'GET':
        count = Score.objects.all().count()
        uscore = Score.objects.filter(client=request.user).first()
        uscore = {'ranking': uscore.rank.rank, 'score': uscore.score}
        return render(request, 'show.html', {'context': context, 'count': count, 'uscore': uscore})
    if request.method == 'POST':
        try:
            start = int(request.POST.get('start'))
            end = int(request.POST.get('end'))
        except ValueError as e1:
            return JsonResponse({'status': 'error'})
        context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                              Score.objects.all().order_by('-score')[start - 1:end]]}
        return JsonResponse({'status': 'ok', 'context': context})

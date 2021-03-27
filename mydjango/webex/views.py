from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.http import  HttpResponse
from .models import Article, Comment
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

# def index(request):
#    return HttpResponse("<h3>Привет, мир!</h3>")

# def test(request):
#    return HttpResponse("<h3>ТЕСТОВАЯ СТРАНИЦА</h3>")

def index(request):
    latest_artical_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'webex/list.html', {'latest_artical_list': latest_artical_list})



def test(request):
    return HttpResponse("<h3>ТЕСТОВАЯ СТРАНИЦА ДЛЯ ЗАПРОСА TEST</h3>")


def detal(request , article_id):

    try:
        a = Article.objects.get(id = article_id)

    except:
        raise Http404("Статья не найдена!")
    latest_comments_list = a.comment_set.order_by('-id')[:10]

    alist = list(a.article_text)

    par = []
    indb = [0]
    count = 0
    tab = '   '
    #for i in range(700):
    while '&' in alist:
            inde = alist.index('&')
            alist.pop(inde)
            out = alist[indb[count]:inde - 1]
            count = count + 1
            indb.append(inde)
            outs = tab + ''.join(out)
            par.append(outs)
    #Если нет разделения на абзацы с помощью символа &, то выводим статью полностью (как в БД)
    if count > 0:
        out = alist[inde:]
    else:
        out = alist
        outs = ''.join(out)
        par.append(outs)

    if request.user.is_authenticated == True:
        acc = account_check(request)
        return render(request, 'webex/blbla.html', {'article': a, 'latest_comments_list': latest_comments_list,'par':par, 'Acc': acc})
    else:
        return render(request, 'webex/blbla.html', {'article': a, 'latest_comments_list': latest_comments_list, 'par': par})

def leave_comment(request, article_id):
    # создаем комментарий к статье и запускаем процедуру detal, которая читает все комментарии, включая новый и
    # отправляет на blbla.html
    if request.user.is_authenticated == True:#20201223
        try:
            a = Article.objects.get(id=article_id)
        except:
            raise Http404("Статья не найдена!")
        #a.comment_set.create(author_name = request.POST['name'], comment_text = request.POST['text']) #20201223
        a.comment_set.create(author_name=request.user, comment_text=request.POST['text'])

        return HttpResponseRedirect(reverse('webex:detal', args = (a.id,)))
    else:#20201223
        return render(request, 'webex/auth_req.html')#20201223

def account_check(request):
        X = []
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")

        customer = a.customer_set.order_by('id')[:]

        for cus in customer:
            X.append(cus.account)

        if len(X) == 0:
            X.append("0")

        return (X[-1])

def smarp(request):
    return render(request, 'webex/smarp.pdf')


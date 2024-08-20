from django.shortcuts import render, HttpResponse

from .tasks import send_email


def send_mail_view(request):
    # 取出用户要发送的邮箱
    to_user = request.GET.get('user')
    # 异步发送
    res = send_email.delay(to_user)
    print(res.id)
    return HttpResponse('邮件已发送，id号为%s' % res.id)

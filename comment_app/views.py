from django.shortcuts import render


def comment_list(request):
    return render(request, 'comment_app/comment_list.html')

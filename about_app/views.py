from django.shortcuts import render
from django.views import View
from .models import TeamMember, Faq, TeamCategory


class AboutUs(View):
    def get(self, request):
        team_members = TeamMember.objects.all()
        return render(request, 'about_app/about.html', {'members': team_members})


class FaqView(View):
    def get(self, request):
        faq_list = Faq.objects.all()
        return render(request, 'about_app/faq.html', {'faq': faq_list})


class TeamView(View):
    def get(self, request):
        categories = TeamCategory.objects.all()
        return render(request, 'about_app/team.html', {"categories": categories})

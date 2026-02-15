from django.shortcuts import render, get_object_or_404
from .models import ChatLogModel
from django.views.generic import CreateView
from django.urls import reverse_lazy

def logs_view(request):
    logs = ChatLogModel.objects.all()
    return render(request, "logs/index.html", {"logs": logs})

def logs_list(request):
    logs = ChatLogModel.objects.all()
    return render(request, "logs/logs_list.html", {"logs": logs})

def logs_detail(request, pk):
    logs = get_object_or_404(ChatLogModel, pk=pk)
    return render(request, "logs/logs_detail.html", {"logs": logs})

class LogsCreate(CreateView):
    template_name = "logs/logs_create.html"
    model = ChatLogModel
    fields = ("title", "content")
    success_url = reverse_lazy("logs:logs_list")

# Create your views here.

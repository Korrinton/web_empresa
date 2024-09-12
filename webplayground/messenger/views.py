from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from messenger.models import Thread, Message
from django.http import Http404
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
# Create your views here.
@method_decorator(login_required, name='dispatch')
class ThreadListView(TemplateView):
    template_name = 'messenger/thread_list.html'


@method_decorator(login_required, name='dispatch')
class ThreadDetailView(DetailView):
    model = Thread

    def get_object(self, queryset=None):
        obj = super(ThreadDetailView, self).get_object(queryset)
        if self.request.user not in obj.users.all():
            raise Http404('You are not allowed to see this thread')
        return obj


def add_message(request, pk):
    Json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404 (Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content, thread=thread)
            thread.messages.add(message)
            Json_response['created']= True
            if len(thread.messages.all()) is 1:
                Json_response['first'] = True
    else:
        raise Http404('You are not allowed to see this thread')

    return JsonResponse(Json_response)

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user,request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from todoapp.forms import Todoform
from todoapp.models import Task
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView


class Tasklistview(ListView):
    model=Task
    template_name = 'home.html'
    context_object_name = 'task'

class TaskDetailview(DetailView):
    model=Task
    template_name='detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model=Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')


# Create your views here.
def addtask(request):
    task = Task.objects.all()
    if request.method == 'POST':
        name=request.POST.get('name','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        task1=Task(name=name,priority=priority,date=date)
        task1.save()
    return render(request,'home.html',{'task':task})

# def details(request):
#
#     return render(request,'detail.html',)

def delete(request,taskid):
    taskids=Task.objects.get(id=taskid)
    if request.method == 'POST':
        taskids.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,taskid):
    taskidss=Task.objects.get(id=taskid)
    form=Todoform(request.POST or None,instance=taskidss)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'taskid':taskidss,'forms':form})

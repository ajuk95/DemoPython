from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TodoForm
from . models import Task

from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


class TaskListView(ListView):
  model = Task
  template_name = 'home.html'
  context_object_name = 'tasks'

class TaskDetailView(DetailView):
  model = Task
  template_name = 'detail.html'
  context_object_name = 'task'

class TaskUpdateView(UpdateView):
  model = Task
  template_name = 'update.html'
  context_object_name = 'task'
  fields = ('name', 'priority', 'date')

  def get_success_url(self):
    return reverse_lazy('cbvdetail', kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
  model = Task
  template_name = 'delete.html'
  # context_object_name = 'task'
  success_url = reverse_lazy("cbvhome")


# Create your views here.
def home(request):
  tasks = Task.objects.all()
  context = {'tasks': tasks}
  if request.method=='POST':
    name = request.POST.get('task', '')
    priority = request.POST.get('priority', '')
    date = request.POST.get('date', '')
    task = Task(name=name, priority=priority, date=date)
    task.save()
    # return redirect('detail')
  return render(request, 'home.html', context=context)

def delete(request, task_id):
  task=Task.objects.get(id=task_id)
  if request.method=='POST':
    task.delete()
    return redirect('/')
  return render(request, 'delete.html')

def update(request, task_id):
  task=Task.objects.get(id=task_id)
  form = TodoForm(request.POST or None, instance=task)
  if form.is_valid():
    form.save()
    return redirect('/')
  return render(request, 'update.html', {'form': form, 'task': task})

# def detail(request):
#   tasks = Task.objects.all()
#   context = {'tasks': tasks}
#   return render(request, 'detail.html', context=context)
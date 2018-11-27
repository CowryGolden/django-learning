# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required    # 只允许登录用户访问的装饰器

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """ 学习笔记的主页 """
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):    # 运行topics()方法前先运行login_required()方法，该方法的代码检查用户是否已登录，仅当用户已登录时，Django才运行topics()的代码。如果用户未登录，就重定向到登录页面。 
    """ 显示所有的主题(只允许登录用户访问) """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')    # 用户只看到自己的主题
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """ 显示单个主题及其所有的条目 """
    # topic = Topic.objects.get(id=topic_id)
    topic = get_object_or_404(Topic, id=topic_id)    # 如果请求对象不存在就跳转到404错误页面
    # 确认请求的主题是否属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')    # date_added前面的减号表示按该字段降序排序
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """ 添加新主题 """
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """ 在特定的主题中添加新条目 """
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题是否属于当前用户
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """ 编辑既有条目 """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的主题是否属于当前用户
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
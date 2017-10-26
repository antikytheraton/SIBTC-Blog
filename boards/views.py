'''
from django.http.response import HttpResponse
def home(request):
    return HttpResponse('Hello, World!')
'''

'''
from django.http.response import HttpResponse
from boards.models import Board
def home(request):
    boards = Board.objects.all()
    board_names = list()
    
    for board in boards:
        board_names.append(board.name)

    response_html = '<br>'.join(board_names)

    return HttpResponse(response_html)
'''
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from boards.models import Board, Post, Topic
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards':boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board':board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first() # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
        return redirect('board_topics', pk=board.pk) # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board':board, 'form':form})

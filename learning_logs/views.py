from django.shortcuts import render,redirect,get_object_or_404,Http404
from .forms import TopicForm,EntryForm
from .models import Topic,Entry
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

from .models import Topic


def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)




def topic(request, topic_id):
    """Show a single topic and its entries."""

    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')

    context = {
        'topic': topic,
        'entries': entries
    }

    return render(request, 'learning_logs/topic.html', context)



# pythonCopy


def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted: create a blank form.
        form = TopicForm()
    else:
        # Data submitted: process the data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()  # save new Topic to database
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)



def new_entry(request, topic_id):
    """Add a new entry for a given topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        # No POST data, create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process it.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # don't save to database yet
            new_entry.topic = topic             # set the topic FK
            new_entry.save()                    # now save to database
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)



def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Populate form with the current entry (instance).
        form = EntryForm(instance=entry)
    else:
        # Bind form to POST data and the instance.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()  # save updates to the entry
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)





# @login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process form.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            # Associate the new topic with the logged-in user
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)



# @login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    # Ensure current user owns this topic.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)



def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Verify the user owns this topic (and hence the entry).
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
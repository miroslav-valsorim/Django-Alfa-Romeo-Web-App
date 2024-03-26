from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic as views

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
from alfa_romeo_web.accounts.models import Profile
from alfa_romeo_web.forum.forms import ProfileForm, AddTopicForm
from alfa_romeo_web.forum.models import ForumCategory, Post, Comment


def require_name(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.profile.first_name and user.profile.last_name:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_forum_credentials')

    return wrapper


@login_required
def credentials_needed(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('forum_main_page')
    else:
        form = ProfileForm(instance=user.profile)

    context = {
        'form': form
    }

    return render(request, 'forum/user_credentials_form.html', context)


@require_name
def forum_view(request):
    forums = ForumCategory.objects.all()
    num_posts = Post.objects.all().count()

    context = {
        "forums": forums,
        "num_posts": num_posts,
    }

    return render(request, 'forum/forum_main_page.html', context)


@login_required
def create_post(request):
    user = request.user

    if request.method == "POST":
        form = AddTopicForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user.profile
            post.save()

        return redirect("forum_main_page")

    else:
        form = AddTopicForm()

    context = {
        'form': form,
    }

    return render(request, 'forum/create_topic.html', context)


@login_required
def posts(request, slug):
    category = ForumCategory.objects.get(slug=slug)
    post = Post.objects.filter(categories=category, approved=True)
    context = {
        'category': category,
        'post': post,
    }

    return render(request, "forum/posts.html", context)


@login_required
def details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = Profile.objects.get(user=request.user)

    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    context = {
        "post": post,
        "title": post.title,
    }

    return render(request, "forum/details.html", context)


class StaffTopicsForApproval(CheckAdminOrStaffAccess, views.ListView):
    template_name = 'forum/staff_forum_page.html'
    queryset = Post.objects.all()
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all()
        order_by = self.request.GET.get('order_by', 'approved')

        if order_by == 'approved':
            queryset = queryset.order_by('approved')
        elif order_by == 'date':
            queryset = queryset.order_by('-date')
        elif order_by == 'closed':
            queryset = queryset.order_by('-closed')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_by'] = self.request.GET.get('order_by', 'approved')

        return context


class ForumTopicEditView(CheckAdminOrStaffAccess, views.UpdateView):
    queryset = Post.objects.all()
    template_name = "forum/staff_edit_post.html"
    fields = ("title", "content", "approved", "categories", "comments", "closed",)

    def get_success_url(self):
        return reverse('staff_forum')

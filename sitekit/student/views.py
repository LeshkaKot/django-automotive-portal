from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.db.transaction import commit
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from .forms import AddPostForm, UploadFileForm, ContactForm
from .models import Student, Category, TagPost, UploadFiles
from .utils import DataMixin
from django.core.cache import cache



class StudentHome(DataMixin, ListView):
    template_name = 'student/index.html'
    context_object_name = 'posts'
    title_page = 'Honda UA'
    cat_selected = 0


    def get_queryset(self):
        s_lst = cache.get("student_posts")
        if not s_lst:
            s_lst = Student.published.all().select_related('cat')
            cache.set("student_posts", s_lst, 60)
        return s_lst


class CarCategory(DataMixin, ListView):
    template_name = 'student/index.html'
    context_object_name = 'posts'



    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Student.published.filter(cat=self.category).select_related('cat')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.category.name, cat_selected=self.category.pk)



@login_required #(login_url="/admin/")
def about(request: HttpRequest):
    contact_list = Student.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/about.html', {'title': 'About the site', 'page_obj': page_obj})




def user_img(request: HttpRequest):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()

    else:
        form = UploadFileForm()
    return render(request, 'student/user_img.html', {'title': 'Send any picture☺', "form": form})



class ShowPost(DataMixin, DetailView):
    template_name = 'student/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)


    def get_object(self, queryset=None):
        return get_object_or_404(Student.published, slug=self.kwargs[self.slug_url_kwarg])




class ShowTagPosts(DataMixin, ListView):
    template_name = 'student/index.html'
    context_object_name = "posts"


    def get_queryset(self):
        self.obj_tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return Student.published.filter(tags=self.obj_tag).select_related('cat')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f"#{self.obj_tag}")




class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'student/addpage.html'
    title_page = "Add Post"
    #login_url = "/admin/"
    permission_required = 'student.add_student' # приложение.действие_табилца

    def form_valid(self, form):
        s = form.save(commit=False)
        s.author = self.request.user
        return super().form_valid(form)



class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Student
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = 'student/addpage.html'
    success_url = reverse_lazy('home')
    title_page = "Redact Post"
    permission_required = 'student.change_student'


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'student/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Feedback"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)



def login(request: HttpRequest):
    return HttpResponse("Authorization")



def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


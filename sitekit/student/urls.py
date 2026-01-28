from django.urls import path, re_path, register_converter
from . import views
from . import converters
from .converters import FourDigitYearConverter
from django.views.decorators.cache import cache_page

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    #path('', cache_page(30)(views.StudentHome.as_view()), name='home'),
    path('', views.StudentHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.CarCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.ShowTagPosts.as_view(), name="tag"),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name="edit_page"),
    path('user_img/', views.user_img, name='img'),
]
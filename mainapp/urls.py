from django.urls import path
from mainapp import views
urlpatterns = [
    path('', views.index, name='index'),
    path('search_ajax/', views.search_ajax, name='search_ajax'),
    path('book_summary_ajax/', views.book_summary_ajax, name='summary_ajax'),

    #genre urls
    path('art/',views.art,name="art"),
    path('biography/',views.biography,name="biography"),
    path('business/',views.business,name="business"),
    path('christian/',views.christian,name="christian"),
    path('comics/',views.comics,name="comics"),
    path('contemporary/',views.contemporary,name="contemporary"),
    path('cookbooks/',views.cookbooks,name="cookbooks"),
    path('crime/',views.crime,name="crime"),
    path('ebooks/',views.ebooks,name="ebooks"),
    path('fantasy/',views.fantasy,name="fantasy"),
    path('fiction/',views.fiction,name="fiction"),
    path('history/',views.history,name="history"),
    path('horror/',views.horror,name="horror"),
    path('manga/',views.manga,name="manga"),
    path('memoir/',views.memoir,name="memoir"),
    path('music/',views.music,name="music"),
    path('mystery/',views.mystery,name="mystery"),
    path('nonfiction/',views.nonfiction,name="nonfiction"),
    path('paranormal/',views.paranormal,name="paranormal"),
    path('psychology/',views.psychology,name="psychology"),
    path('philosophy/',views.philosophy,name="philosophy"),
    path('poetry/',views.poetry,name="poetry"),
    path('religion/',views.religion,name="religion"),
    path('romance/',views.romance,name="romance"),
    path('science/',views.science,name="science"),
    path('suspense/',views.suspense,name="suspense"),
    path('spirituality/',views.spirituality,name="spirituality"),
    path('sports/',views.sports,name="sports"),
    path('thriller/',views.thriller,name="thriller"),
    path('travel/',views.travel,name="travel"),
    path('classics/',views.classics,name="classics")

]
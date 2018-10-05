from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.views.generic import ListView
from blog_app.forms import CommentForm, ArticleGeoForm
from blog_app.models import Article, Comments, UserProfile, Likes


class Articles(ListView):
    model = Article
    template_name = 'articles.html'
    paginate_by = 2
    queryset = Article.objects.order_by('-article_date')#sort the latest date
    context_object_name = 'articles'

    def dispatch(self, request, *args, **kwargs):
        print(request)
        print(kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(Articles, self).get_context_data(**kwargs)
        user = self.request.user
        return context


def article(request, article_id=1):#default = article with id=1
    comment_form = CommentForm
    obj = get_object_or_404(Article, id=article_id)
    form_article = ArticleGeoForm(instance=obj)
    args = {}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    args['form'] = comment_form
    args['user'] = auth.get_user(request)
    args['point'] = form_article
    return render_to_response('article.html', args)


def addlike(request, article_id):
    back_url = request.META['HTTP_REFERER']
    try:
        user = UserProfile.objects.get(id=auth.get_user(request).id)
        try:
            a = Likes.objects.get(likes_article=Article.objects.get(id=article_id),
                             likes_user=UserProfile.objects.get(id=auth.get_user(request).id))
        except ObjectDoesNotExist:
            like_row = Likes.create(Article.objects.get(id=article_id), UserProfile.objects.get(id=auth.get_user(request).id))
            like_row.save()
            art = Article.objects.get(id=article_id)
            art.artticle_likes +=1
            art.save()
    except ObjectDoesNotExist:
        return redirect(back_url)
    return redirect(back_url)


def addcomment(request, article_id):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_article = Article.objects.get(id=article_id)
            comment.comments_user = UserProfile.objects.get(id=auth.get_user(request).id)
            form.save()
            art = Article.objects.get(id=article_id)
            art.article_comments += 1
            art.save()
        return redirect('/blog/articles/get/%s/' %article_id)


def about(request):
    return render_to_response('about.html', {'users': User.objects.all(), 'user': auth.get_user(request)})


def mainview(request):#default = article with id=1
    return render_to_response('main.html',)
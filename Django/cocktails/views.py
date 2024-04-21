from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from cocktails.models import Cocktail, Comment
from .forms import CocktailCreateUpdateForm
from django.urls import reverse_lazy, reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from cocktails.filters import FilteredCocktails
from django_filters.views import FilterView


class CocktailListView(FilterView):
    template_name = 'cocktail_list.html'
    model = Cocktail
    queryset = Cocktail.objects.prefetch_related("my_favorites")
    filterset_class = FilteredCocktails

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_archived=False).prefetch_related("my_favorites")
        return queryset


class CocktailCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_cocktail.html'
    model = Cocktail
    form_class = CocktailCreateUpdateForm
    success_url = reverse_lazy('cocktail-list')

    def form_valid(self, form):
        cocktail = form.save(commit=False)
        cocktail.creator = self.request.user
        cocktail.save()
        return super(CocktailCreateView, self).form_valid(form)


class MyCocktailListView(LoginRequiredMixin, ListView):
    template_name = 'cocktail_list.html'
    model = Cocktail
    queryset = Cocktail.objects.prefetch_related('my_favorites')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(creator=self.request.user)
        queryset = queryset.order_by('is_archived')
        return queryset


def archive(request, pk):
    user = request.user
    cocktail = get_object_or_404(Cocktail, pk=pk)
    if cocktail.creator == user:
        action = request.POST.get('action', 'archive')
        if action == 'archive':
            cocktail.is_archived = True
        elif action == 'off_archive':
            cocktail.is_archived = False
        cocktail.save()
    return HttpResponseRedirect(reverse_lazy('my-cocktail'))


class CocktailUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'create_cocktail.html'
    model = Cocktail
    form_class = CocktailCreateUpdateForm
    success_url = reverse_lazy('cocktail-list')

    def dispatch(self: SingleObjectMixin, request: HttpRequest, *args, **kwargs):
        cocktails: Cocktail = self.get_object()
        if cocktails.creator != request.user:
            return HttpResponseRedirect(reverse_lazy('cocktail', args={cocktails.pk}))
        return super().dispatch(request, *args, **kwargs)


class MyFavouriteCocktails(LoginRequiredMixin, ListView):
    template_name = 'my_favorite.html'
    model = Cocktail

    def get_queryset(self):
        queryset = self.request.user.liked_by.all()
        return queryset


@login_required
def add_like(request, pk):
    user = request.user
    cocktail = get_object_or_404(Cocktail, pk=pk)
    is_favorite = user in cocktail.my_favorites.all()
    if is_favorite:
        cocktail.my_favorites.remove(user)
    else:
        cocktail.my_favorites.add(user)
    cocktail.save()
    return HttpResponseRedirect(reverse_lazy('cocktail-list'))


class CocktailDet(DetailView):
    template_name = 'cocktail.html'
    model = Cocktail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cocktail = context['object']
        context['top_level_comments'] = (
            (Comment.objects.filter(cocktail=cocktail, parent__isnull=True)).
            select_related('creator', 'parent')).prefetch_related('replies')
        return context


@login_required
def add_comment(request, pk):
    user = request.user
    cocktail = get_object_or_404(Cocktail, pk=pk)

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')

        if comment_text:
            parent_comment = None
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
            comment = Comment.objects.create(
                text=comment_text,
                creator=user,
                cocktail=cocktail,
                parent=parent_comment,
            )
            comment.save()
            return HttpResponseRedirect(reverse('add-comment', args=[pk]) + f'#comment-{comment.pk}')
    return HttpResponseRedirect(reverse_lazy('cocktail', args=[pk]))


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user == comment.creator:
        comment.delete()
        return redirect('cocktail', pk=comment.cocktail.pk)

    return redirect('cocktail', pk=comment.cocktail.pk)

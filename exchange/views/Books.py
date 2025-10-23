'''
    Handles displaying books
'''
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

from ..models import Book, Exchange
from ..forms import CreateBookForm
    
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'books/book-create.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Fill in any auto-filled fields
        form.instance.owner = self.request.user
        
        return super().form_valid(form)
    
class InspectBook(DetailView):
    model = Book
    template_name = 'books/book-detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Initialize the new context variable
        context['user_active_request'] = None

        # Check if the user is authenticated (essential for this check)
        if self.request.user.is_authenticated:
            active_request = Exchange.objects.filter(
                book=self.object,
                requester=self.request.user,
                status__in=['PND', 'ACC'] 
            ).select_related('requester' ).first()

            if active_request:
                context['user_active_request'] = active_request
                
        return context
    
class GetOwnedBooks(LoginRequiredMixin, ListView):
    paginate_by = 50
    model = Book
    template_name = "books/book-owned.html"
    
    def get_queryset(self):
        qs = Book.objects.filter(owner = self.request.user).order_by("-created_at")
        
        query = self.request.GET.get('q')
        if query:
            # Use Q objects for OR lookups across multiple fields
            qs = qs.filter(
                Q(title__icontains=query) | 
                Q(author__icontains=query) |
                Q(isbn__iexact=query) # Exact match for ISBN search
            )
                
        return qs
    
class ListBooks(ListView):
    paginate_by = 50
    model = Book
    template_name = "books/book-list.html"
    def get_queryset(self, *args, **kwargs):         
        qs = Book.objects.filter(status = "AVL").order_by("-created_at")
        
        if self.request.user.is_authenticated:
            qs = qs.exclude(owner=self.request.user)
        
        query = self.request.GET.get('q')
        if query:
            # Use Q objects for OR lookups across multiple fields
            qs = qs.filter(
                Q(title__icontains=query) | 
                Q(author__icontains=query) |
                Q(isbn__iexact=query) # Exact match for ISBN search
            )
        
        return qs 
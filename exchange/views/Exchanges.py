'''
    Contains the views that handle making, accepting and rejecting new requests for book swaps
'''

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy 
from django.http import HttpRequest, HttpResponse, JsonResponse

from ..models import Exchange, Book

class ListExchangeRequests(LoginRequiredMixin, TemplateView):
    '''
        Shows all the exchanges made for books under the ownership of the given user
    '''
    login_url = reverse_lazy("account_login")
    model = Exchange
    template_name = "exchanges/exchanges-list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        all_requests = Exchange.objects.filter(
            Q(book__owner=user) | Q(requester=user)
        ).select_related(
            'book', 
            'requester', 
            'book__owner'
        ).order_by("-requested_at")

        incoming = []
        outgoing = []
        
        for req in all_requests:
            if req.requester == user:
                outgoing.append(req)
            
            if req.book.owner == user:
                incoming.append(req)

        # Filter exchanges where the book owner is the current user
        context['incoming_requests'] = incoming
        
        context['outgoing_requests'] = outgoing
        return context

def create_response(status_code, payload):
    '''
        Convenience method to streamline the returning of HTTP status messages.
        Only used for if this is a REST API rather than a template
    '''
    response = JsonResponse({
        "detail": "Cannot perform this action"
    })   
    response.status_code = status_code
    
    return response

@login_required
def request_exchange(request:HttpRequest, book_id):
    '''
        Allows a user to request a specific book from another user
    '''
    if request.method == "POST":
        target_book = get_object_or_404(Book, pk = book_id)
        
        # Prevent the owner from requesting a book they already have
        if target_book.owner == request.user:
            # Any exits can be replaced with this if this is moving to a REST API
            
            # return create_response(400, {
            #     "detail": "Cannot perform this action"
            # })
            
            messages.error(request, "Cannot perform this action")
            return redirect("book-detail", pk = target_book.pk)
            
        
        # Prevent duplicate exchanges for the same book
        if Exchange.objects.filter(book=target_book, requester=request.user, status__in=['PND', 'ACC']).exists():
            messages.error(request, "Cannot perform this action")
            return redirect("book-detail", pk = target_book.pk)
        
        # Books that aren't marked as ready to be exchanged should be blocked too
        if target_book.status != "AVL":
            messages.error(request, "Cannot perform this action")
            return redirect("book-detail", pk = target_book.pk)
        
        Exchange.objects.create(
            book=target_book,
            requester=request.user,
            status='PND'
        )
        
        messages.success(request, "Requested this book!")
        return redirect("exchange-list")
        
@login_required
def accept_request(request:HttpRequest, exchange_id):
    '''
        Handles allowing users to approve of an existing request
    '''
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    
    # If the request is for a book this user doesn't own then block it
    if exchange.book.owner != request.user:
        messages.error(request, "Cannot perform this action")
        return redirect("book-detail", pk = exchange.book.pk)
        
    # Any exchanges that aren't in the state to be rejected or accepted are blocked too
    if exchange.status != "PND":
        messages.error(request, "Cannot perform this action")
        return redirect("book-detail", pk = exchange.book.pk)
        
    exchange.status = "ACC"
    # Update the book too
    exchange.book.status = "EXC"
    exchange.save()
    
    # Update all other pending requests for this book
    Exchange.objects.filter(book=exchange.book, status='PND').exclude(pk=exchange.pk).update(status='REJ')

    messages.success(request, "Marked this book for exchange!")
    return redirect("exchange-list")

@login_required
def reject_request(request:HttpRequest, exchange_id):
    '''
        Handles the endpoint that allows users to reject requests
    '''
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    
    # If the request is for a book this user doesn't own then block it
    if exchange.book.owner != request.user:
        messages.error(request, "Cannot perform this action")
        return redirect("book-detail", pk = exchange.book.pk)
        
    # Any exchanges that aren't in the state to be rejected or accepted are blocked too
    if exchange.status != "PND":
        messages.error(request, "Cannot perform this action")
        return redirect("book-detail", pk = exchange.book.pk)
        
    exchange.status = "REJ"
    exchange.book.status = "AVL"
    exchange.save()
    
    messages.success(request, "Successfully rejected this request")
    return redirect("exchange-list")

@login_required
def finalise_request(request:HttpRequest, exchange_id):
    '''
        Signifies the end of the exchange when the lister physically exchanges
        books with the recipient
    '''
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    # If the request is for a book this user doesn't own then block it
    if exchange.book.owner != request.user:
        messages.error(request, "Cannot perform this action")
        return redirect("book-detail", pk = exchange.book.pk)
        
    # Any exchanges that aren't in the state to be finalised
    if exchange.status != "ACC":
        messages.error(request, "Cannot perform this action")
        return redirect("book-detail", pk = exchange.book.pk)
    
    exchange.status = "CMP"
    exchange.book.owner = exchange.requester
    
    exchange.book.save()
    exchange.save()
    
    messages.success(request, "Successfully finalised this request")
    return redirect("exchange-list")
from django.urls import path

from .views import Books, User, Exchanges

urlpatterns = [
    # Exchange
    path("request/new/<int:book_id>", Exchanges.request_exchange, name = "exchange-create"),
    path("request/accept/<int:exchange_id>", Exchanges.accept_request, name = "exchange-accept"),
    path("request/reject/<int:exchange_id>", Exchanges.reject_request, name = "exchange-reject"),
    path("request/finish/<int:exchange_id>", Exchanges.finalise_request, name = "exchange-finish"),
    path("request/list", Exchanges.ListExchangeRequests.as_view(), name = "exchange-list"),
    # Core views
    path("", Books.ListBooks.as_view(), name = "home"),
    path("book/new", Books.BookCreateView.as_view(), name = "book-create"),
    path("book/<int:pk>", Books.InspectBook.as_view(), name = "book-detail"),
    path("book/owned", Books.GetOwnedBooks.as_view(), name = "book-owned"),
]
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    # Add @receiver to auto-create Profile when User is created

class Book(models.Model):
    '''
        Represents one specific book owned by a user
    '''
    class BookStatus(models.TextChoices):
        '''
            BookStatus denotes the current status of the book as tracked by the system
            This is an extra layer of safety to prevent "double spends".
        '''
        AVAILABLE = 'AVL', 'Available'
        PENDING = 'PND', 'Pending Exchange'
        EXCHANGED = 'EXC', 'Exchanged'

    class BookCondition(models.TextChoices):
        NEW = 'NEW', 'New'      
        GOOD = 'GOD', 'Good'    
        FAIR = 'FAR', 'Fair'    
        DMG = "DMG", "Damaged"
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, blank=True, null=True, help_text="Used to auto-fill details")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_books')
    
    description = models.TextField(blank=True)
    
    condition = models.CharField(max_length=3, choices=BookCondition.choices, default=BookCondition.NEW)
    status = models.CharField(max_length=3, choices=BookStatus.choices, default=BookStatus.AVAILABLE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Exchanged is used to denote that a book has been successfully exchanged to another user
    exchanged = models.BooleanField(default = False)
    # Delivered is used to determine if an exchanged book has been delivered to the recipient (ie they now own it)
    delivered = models.BooleanField(default = True)
    
class Exchange(models.Model):
    class ExchangeStatus(models.TextChoices):
        PENDING = 'PND', 'Pending'
        ACCEPTED = 'ACC', 'Accepted'
        REJECTED = 'REJ', 'Rejected'
        COMPLETED = 'CMP', 'Completed' # This is used to signify that the lister has delivered the book to the recipient

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exchange_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_exchanges')
    status = models.CharField(max_length=3, choices=ExchangeStatus.choices, default=ExchangeStatus.PENDING)

    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only request a specific book once if and only if the status of that
        # request is not pending nor accepted
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'requester'],
                
                condition = models.Q(status__in=['PND', 'ACC']),
                name='unique_pending_or_accepted_exchange',
            )
        ]
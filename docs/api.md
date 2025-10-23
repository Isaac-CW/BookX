While the application currently does not use a REST API, the backend may be converted into one using Django-REST-Framework. As such, here is the API contract that may be used when available.

# Overview
The base route used is `/api`
## Routes
### Authentication
Authentication is powered by allauth which provides its own API for exchanging authentication tokens

### Book exchanges
Handles creating, querying and updating book exchange requests. The base route used is `/request/`

#### request/new/<book_id>
Creates a new book exchange request for the book with the given ID. @login_required
A user can only create an exchange for the given book if the user does not have a request
that's pending or accepted active for the given book.

###### CREATE
Code returns:
* 201 if the request is successfully made
* 400 If the user already has an existing request for the given book
* 401 If the user has not logged in / does not have permission to perform this action
* 404 If the book with the given book_id cannot be found

#### request/accept/<request_id>
Accepts the request with the given ID. @login_required
A user can only accept requests for books that they own; attempting to accept a request
the requester created will return unsuccessfully.

##### POST
Code returns:
* 202 if the user owns the book being requested and has not previously accepted/rejected this request
* 401 if the user is not the requester, is not logged in or does not have the permission to perform this action
* 404 if the request with the given ID cannot be found

#### request/reject/<request_id>
Rejects the request with the given ID. @login_required
A user can only reject requests for books that they own; attempting to reject a request
the requester created will return unsuccessfully.

##### POST
Code returns:
* 202 if the user owns the book being requested and has not previously accepted/rejected this request
* 401 if the user is not the requester, is not logged in or does not have the permission to perform this action
* 404 if the request with the given ID cannot be found

#### request/finish/<exchange_id>
Finalises the request by confirming that the book owner physically transferred the book to the requester @login_required
A user can only do this if the book's owner is the user

##### POST
Code returns:
* 202 if the user owns the book being requested
* 401 if the user is not the book owner, is not logged in or does not have the permission to perform this action
* 404 if the request with the given ID cannot be found

#### request/list/
Returns the list of requests made for books that the user owns. @login_required

##### GET
Each book exchange request is a JSON object that follows this schema
```
{
    book: Book_object
    requester: User_object
    pk: int,
    requested_at: date_time,
}
```
Returns two arrays of these objects in the following format
```
{
    incoming_requests: [requests],
    outgoing_requests: [requests],
}
```
Code returns:
* 200 if the user is logged in
* 401 if the user is not logged in or doesn't have permission to perform this action

### Books
Handles creating/listing books for exchange. The base URL for these requests are `/book/`
#### /book/list
Returns a list of all books available for exchange, excluding books owned by the current user (if the user is currently logged in). Can be searched
##### GET
The associated data should be formatted as so:
```
{
    title: str | null
    author: str | null
    isbn: str | null
}
```
Title and author are partially matched to all books which fit the query whereas isbn is exactly matched. Currently all 3 queries are OR'd together to match books.

The response is a JSON array of Book objects which match the query if given or all listed books not by the current user (if logged in)
Code returns:
* 200 if the request is successful.
* 401 if a search query (?q=...) is made without being logged in (the view currently supports anonymous access).

#### /book/new
Creates a new book listing owned by the logged-in user. @login_required
##### POST
Requires form data corresponding to the Book model fields (e.g., title, author, isbn, condition, description). The owner field is automatically set to the authenticated user.
Code returns:
* 201 if the book listing is successfully created.
* 400 if validation fails (e.g., required fields are missing).
* 401 if the user is not logged in.
#### /book/<book_id>
Retrieves the details for a specific book listing identified by its ID.
##### GET
The response is a JSON object representing the detailed Book instance.The response object also includes a special field if the user is logged in:
```
{
    // ... all Book fields (title, author, owner, status, etc.)
    user_active_request: {} | null
}
```
user_active_request is present if the current user has created a request that's currently pending or accepted for the given book.

Code returns:
* 200 if the book is found and successfully returned.
* 404 if the book with the given pk cannot be found.
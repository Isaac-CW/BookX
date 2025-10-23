# BookX
A proof of concept exercise

## Usage
### Requirements
The system requires Python3 3.11.2

The python requirements can be installed using the following operations (Assuming this is done from a virtual environment)
```
python3 -m pip install -r requirements.txt
```

### Running the server
To operate django, the following commands must be run in order
```
python3 manage.py migrate
python3 manage.py runserver
```
This will establish the local database and begin listening on the address shown in stdout

## Core features
The core goal of the application is to provide users with a sense of community around sharing and resharing books.

To this end, the following functional requirements are defined:
* The system shall allow users to list books they are willing to donate
  * No verification system to ensure that users only create listings for books they own is planned; similar to user-driven marketplaces like Facebook Marketplace or Ebay, similar technologies in place there for ensuring user trust can be implemented here.
  * Acceptance criteria: the user can create a listing for a book they own and the system shall show the new listing. Duplicate book listings are possible

* The system shall allow users to request another user to donate their listed book
  * Users cannot create active requests for the same book from the same user; if a request is denied, a user can create a new request
  * Acceptance criteria: Given a book listing, a user can request that book. The user who created that listing shall then be able to see that request and approve/deny it

* The system shall track requests made for books owned by each user
  * Users can make multiple requests for multiple books but cannot make the same request for the same book
  * Acceptance criteria: Given a book listing and a set of requests, the system shall display to the user all requests the user made

* The system shall track the state of requests made for each book
  * There are 4 states for a request:
    * Pending: A user has requested another user's book but the book owner has not responded
    * Rejected: The book owner has rejected the request
    * Accepted: The book owner has accepted the request but has not physically transferred the book to the requester
    * Finished: The book owner has transferred the book to the requester; they no longer own the book
  * Acceptace criteria: Given an existing valid request, the system shall display to both book owner and requester the state of the request; the owner may change the state of a pending request to accept or reject; the requester may change the state of the request from accepted to finish
    * Upon finishing the request, the book owner should no longer see the book as owned by them; the requester may see the book as owned by them

In short, the core features of the platform are:
* User accounts
* On behalf of a user, adding and tracking books that the user owns
* Tracking requests for books made between users
* Facilitate the exchange of books and track the status of each exchange (without enforcement or automated updating of status)

These core features have been implemented in the proof of concept

### Core demographic
The core demographic are people who are avid readers or are interested in reading more. There is no distinction between individuals in terms of socioeconomic status, culture, race or age. To this end, the application is aimed to be a web application that provides a simple-to-use interface that fosters a community of sharing and mutual enthusiasm for reading.

### Use cases

#### For book owners who are cleaning their bookshelves
* Scenario: Alice has finished reading a stack of mystery novels and wants to make space on her shelf without simply throwing them away.
* Action: Alice logs into BookX, uses the system to list her books, setting their condition (e.g., "Good").

#### For readers searching for a new book
* Scenario: Bob is looking for a specific classic, Moby Dick, which he saw a friend reading, but doesn't want to buy a new copy.
* Action: Bob uses the Search functionality to look up Moby Dick by title or ISBN. He finds a copy listed by user Carol and sends a request for the book who accepts it and transfers it to Bob.

## Technology
To achieve this goal, the following technology was used to create the application. A combination of familiarity and scalability was prioritized.

### Additional features
Alongside the implemented core features, there are additional features that complement them.
* Searching of books that may use title, author or ISBN to allow users to better find books they want to search for
* All tracked books are displayed to the user for convenient browsing
* Requests made by the user are collated and displayed as outgoing and incoming requests for better organisation
* The system maintains awareness of the status of requests and the UI reflects that. For instance, if a user has already made a request for a book that is currently pending or has already been accepted, the UI will reflect this if the user attempts to make a new request.

### Backend
The backend uses Django due to famliarity with both python and the framework compared to other batteries-included frameworks such as .NET and Spring. Django can be scaled without too much issue making it an ideal framework for building. Furthermore, all-auth is used to provide security features and reduce the burden of security on the project.

For data storage, sqlite was selected for the ease of use and compatibility with Django.

The files are organised using Django's standard structure with additional organisation for better modularity. Views are contained within a submodule and are separated by the models it operates on. Forms follow suit similarly. 

Database models are stored within models.py to centralise all the logic. However, this could be split into its own submodule for future expansion if the number of entities in the database increases as the application scales up.

### Frontend
For the proof of concept, the system is a monolith that uses Django's templating engine to render web pages directly from the backend. The system can be adapted to use a split frontend/backend stack to reduce the coupling of the two stacks using modern frameworks such as React or Angular. For styling, Bootstrap5 is used to minimise the burden of CSS and consistency.

### Future-proofing
Django's suitability for the project benefits scalability as django can be relatively easily scaled and can be converted to use Django-REST-Framework to convert the templating engine into a REST API. The database can be migrated to PostgresSQL which is supported by all major cloud providers.

A sample API documentation for the future REST API is given in docs/api.md

## Roadmap
The proof of concept can be expanded in several ways
* Geospatial queries
  * The location of the user can be enhanced using geospatial APIs to present a "books near you" field to better filter users' books. A key consideration of this is enhanced privacy measures needed to ensure sensitive data is held in compliance with Singaporean privacy laws.
    * This allows the informational burden on the user to be reduced by only showing listings created near the user's location.
* External APIs
  * Using the ISBN of a book, the title and author fields can be automatically populated using external lookups such as Google Books' API. This requires additional resources to maintain the API
  * Other popular platforms for books such as Goodreads can be interfaced with to boost engagement and allow the platform to reach a wider audience.
* Migration of platform to scalable technology
  * Currently, the proof of concept is a single application relying on Django's templating engine to dynamically populate the website with content. This can be migrated to a more modern stack by separating the frontend and backend, converting the Django backend to a REST API using Django-Rest-Framework and using a modern framework like React or Angular for the frontend. As of now, this separation is too complex for a proof of concept but the system can easily be adapted using the aforementioned Django-Rest application.
  * Currently, the database is hosted locally but can be easily adapted for an external databse provider such as AWS or Azure by changing the settings.py and including the key in the environment.
  * The platform can be containerized with docker for deployment to AWS
* Social features
  * More personalisation could be made through tracking the exchanges between users such as prioiritising a specific user's requests or allowing communication on the platform beforehand
  * Exchanges could be encouraged by implementing statistics such as "books given away" or "exchanged books" that users can display as badges.
    * Trust mechanisms to avoid the potential of scams or threats to the platform can leverage this.
"""bokks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bokksapp.views import homepage, search, genres, events, events_id, books, books_id, auth, cart, orders

urlpatterns = [
    # HOME
    path('', homepage.homepage, name='home'),
    # SEARCH
    path('search/', search.processRequest),
    # EVENTS
    path('events/', events.processRequest, name='events'),
    path('events/<int:id>', events_id.processRequest),
    path('events/<int:id>/<str:img_path>', events_id.get_image),

    # GENRES
    path('genres/', genres.process_request),
    # BOOKS
    path('books/', books.process_request),
    path('books/<int:id>', books_id.process_request),
    path('books/<int:id>/<str:img_path>', books_id.get_image),
    # CART
    path('cart/', cart.processRequest),
    path('cart/<str:title>', cart.deleteFromCart),
    # Orders
    path('orders/', orders.processRequest),
    path('orders/<int:id>', orders.getID),
    # AUTH
    path('profile', auth.profile),
    path('login', auth.login),
    path('logout', auth.logout)
]


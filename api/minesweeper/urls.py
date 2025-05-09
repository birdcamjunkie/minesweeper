"""
URL configuration for minesweeper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from games.views import create_game, get_game, update_cell

urlpatterns = [
    path("admin/", admin.site.urls),
    path("games", create_game, name="create_new_game"),
    path("games/<str:game_id>", get_game, name="get_game_by_id"),
    path(
        "games/<str:game_id>/cell<int:cell_id>",
        update_cell,
        name="update_cell_of_game_by_id",
    ),
]

import flet as ft
from pages.landing import Landing
from pages.welcome import Welcome
import os


# Définir des constantes pour les routes
WELCOME_ROUTE = "/welcome"
LANDING_ROUTE = "/"


def main(page: ft.Page):
    page.title = "FOMIGEST V2.0"
    page.fonts = {
        "Poppins Regular": "fonts/Poppins-Regular.ttf",
        "Poppins Bold": "fonts/Poppins-Bold.ttf",
        "Poppins SemiBold": "fonts/Poppins-SemiBold.ttf",
        "Poppins Black": "fonts/Poppins-Black.ttf",
        "Poppins Italic": "fonts/Poppins-Italic.ttf",
        "Poppins Medium": "fonts/Poppins-Medium.ttf",
        "Poppins ExtraBold": "fonts/Poppins-ExtraBold.ttf",
        "Poppins Light": "fonts/Poppins-Light.ttf",
    }
    page.theme = ft.Theme(font_family="Poppins-Medium")

    # Dictionnaire pour mapper les routes aux vues
    route_views = {
        LANDING_ROUTE: Landing,
        WELCOME_ROUTE: Welcome,
    }

    # Gérer les changements de route
    def route_change(event: ft.RouteChangeEvent):
        page.views.clear()  # Réinitialiser les vues
        current_route = event.route  # Récupérer la route depuis l'événement
        if current_route in route_views:
            page.views.append(route_views[current_route](page))
        else:
            # Rediriger vers une route par défaut si la route est inconnue
            page.views.append(Landing(page))
        page.update()

    # Gérer la navigation "retour"
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Assignation des callbacks
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Naviguer vers la route initiale
    page.go(page.route)



if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, port=port, view=ft.AppView.WEB_BROWSER)


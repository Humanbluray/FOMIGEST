import flet as ft
from pages.landing.landing import Landing, user_infos
from pages.welcome.welcome import Welcome
from pages.first_connexion.first_connexion import FirstLogin
import os


# Définir des constantes pour les routes
WELCOME_ROUTE = f"/welcome/{user_infos['username']}"
LANDING_ROUTE = "/"
FIRST_CONNEXION = "/first_connexion"


def main(page: ft.Page):
    page.title = "FOMIDERC Groupe services"
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
        FIRST_CONNEXION: FirstLogin
    }

    # Gérer les changements de route
    def route_change(event: ft.RouteChangeEvent):
        # initial route ...
        page.views.clear()
        page.views.append(Landing(page))
        page.update()

        if page.route == "/":
            page.views.append(Landing(page))
            page.update()

        if page.route == f"/welcome/{user_infos['username']}":
            if user_infos["status"]:
                page.views.append(Welcome(page))
            else:
                page.views.append(Landing(page))
            page.update()

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
    ft.app(target=main, port=port, assets_dir="assets")  # , view=ft.AppView.WEB_BROWSER)


import flet as ft
from pages.landing.landing import Landing, user_infos
from pages.welcome.welcome import Welcome
from pages.first_login.first_login import FirstLogin
import os


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
    page.theme = ft.Theme(font_family="Poppins Medium")

    # Cache des vues pour éviter de les recréer à chaque navigation
    views_cache = {
        "/": Landing(page),
        "/welcome": Welcome(page),
        "/first_login": FirstLogin(page)
    }

    def route_change(event: ft.RouteChangeEvent):
        page.views.clear()
        if event.route in views_cache:
            page.views.append(views_cache[event.route])
        else:
            page.views.append(ft.View(controls=[ft.Text("Page non trouvée", size=34)]))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, port=port, assets_dir="assets")  # , view=ft.AppView.WEB_BROWSER)


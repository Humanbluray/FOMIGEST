import time
import flet as ft
from utils import login_style, AnyButton
from utils.constantes import FIRST_COLOR
import backend as be

user_infos = {
    "username": "", "userlevel": "", "userlogin": "", "status": False,
    "usernom": "", "userprenom": "",
}
LOGO_URL = "https://byggqnusosovxulbchup.supabase.co/storage/v1/object/public/logos//logo.jpg"


class Landing(ft.View):
    def __init__(self, page: ft.Page):

        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            route="/", bgcolor="#f2f2f2"
        )
        self.page = page

        self.login = ft.TextField(
            **login_style, prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED, label="Login"
        )
        self.passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Pass",
            password=True, can_reveal_password=True
        )
        self.bt_connect = AnyButton(FIRST_COLOR, "check", "Connecter", "white", None,self.connexion)
        self.bt_first = AnyButton(FIRST_COLOR, "check", "Première connexion", "white", None, self.go_to_first)

        # Dialog box
        self.box = ft.AlertDialog(
            surface_tint_color="white",
            title=ft.Text("", size=20, font_family="Poppins Light"),
            content=ft.Text("", size=12, font_family="Poppins Medium"),
            actions=[
                ft.TextButton(
                    content=ft.Row(
                        [ft.Text("Quitter", size=12, font_family="Poppins Medium", color=FIRST_COLOR)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ), width=120,
                    on_click=self.close_box
                )
            ]
        )
        self.page.overlay.append(self.box)

        self.card = ft.Card(
            elevation=10, surface_tint_color="white",
            content=ft.Container(
                border_radius=16, padding=20, width=230, bgcolor="white",
                content=ft.Column(
                    controls=[
                        ft.Image(src=LOGO_URL, width=100, height=100),
                        ft.Text("Connexion", size=16, font_family="Poppins Bold"),
                        ft.Divider(height=1, color="transparent"),
                        self.login, self.passw, self.bt_connect, self.bt_first
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
        self.controls = [
            ft.Stack(
                controls=[
                    self.card,
                ], alignment=ft.alignment.center
            )
        ]

    def close_box(self, e):
        self.box.open = False
        self.box.update()

    def connexion(self, e):
        if be.check_login(self.login.value, self.passw.value):
            if be.search_user_infos(self.login.value)['statut'] == "actif".upper():
                details = be.search_user_infos(self.login.value)
                user_infos["username"] = details['nom']
                user_infos['usernom'] = details['nom']
                user_infos['userprenom'] = details["prenom"]
                user_infos["userlevel"] = details["niveau"]
                user_infos["userlogin"] = details["login"]
                user_infos["status"] = True
                self.page.go(f"/welcome/{user_infos['usernom']}")
                be.add_activity(user_infos["userlogin"], "Connexion".upper())
                time.sleep(10)
                user_infos["status"] = False

            else:
                user_infos["status"] = False
                self.box.title.value = "Erreur"
                self.box.content.value = "Contactez votre administrateur !"
                self.box.open = True
                self.box.update()

        else:
            user_infos["status"] = False
            self.box.title.value = "Erreur"
            self.box.content.value = "Login ou mot de passe incorrect(s)"
            self.box.open = True
            self.box.update()

    def go_to_first(self, e):
        self.page.go("/first_login")




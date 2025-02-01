import time
import flet as ft
import string
from backend import all_users
from utils import login_style, AnyButton, field_mail_style
from utils.constantes import FIRST_COLOR
import backend as be


class FirstLogin(ft.View):
    def __init__(self, page):

        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            route="/first_login", bgcolor="#f2f2f2"
        )
        self.page = page
        self.check_mail = ft.Icon(None, size=24, color="green")
        self.check_pass = ft.Icon(None, size=24, color="green")
        self.check_login = ft.Icon(None, size=24, color="green")
        self.check_confirm = ft.Icon(None, size=24, color="green")

        self.email = ft.TextField(
            **field_mail_style, prefix_icon=ft.icons.MAIL_OUTLINED, label="Login",
            on_change=self.changement_email, width=220
        )
        self.login = ft.TextField(
            **login_style, prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED, label="Login",
            width=220
        )
        self.passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Password", width=220,
            password=True, can_reveal_password=True
        )
        self.confirm_passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Confirmez", width=220,
            password=True, can_reveal_password=True
        )
        self.bt_connect = AnyButton(FIRST_COLOR, "check", "Connecter", "white", None,self.connexion)

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
                border_radius=16, padding=20, width=320, bgcolor="white",
                content=ft.Column(
                    controls=[
                        ft.Image(src="assets/images/logo.jpg", width=75, height=75),
                        ft.Divider(height=1, color="transparent"),
                        ft.Text("Saisir vos informations".upper(), size=14, font_family="Poppins Bold"),
                        ft.Divider(height=1, color="transparent"),
                        ft.Row([self.email, self.check_mail]),
                        ft.Row([self.login, self.check_login]),
                        ft.Row([self.passw, self.check_pass]),
                        ft.Row([self.confirm_passw, self.check_confirm]),
                        self.bt_connect,
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

    def changement_email(self, e):
        datas = be.all_users()
        emails = [data['email'] for data in datas]
        if self.email.value in emails and be.search_user_by_mail(self.email.value)["statut"] == "NOUVEAU":
            self.check_mail.name = ft.icons.CHECK_CIRCLE
            self.check_mail.update()
        else:
            self.check_mail.name = None
            self.check_mail.update()

    def changement_login(self, e):
        datas = be.all_users()
        logins = [data['login'] for data in datas]

        if self.login in logins:
            self.check_login.name = None
            self.check_login.update()
        else:
            self.check_login.name = ft.icons.CHECK_CIRCLE
            self.check_login.update()

    def changement_pass(self, e):
        nombres = string.digits
        majuscules = string.ascii_uppercase
        speciales = string.punctuation

        type_digits  = [letter for letter in self.passw.value if letter in nombres]
        type_majucules = [letter for letter in self.passw.value if letter in majuscules]
        type_speciales = [letter for letter in self.passw.value if letter in speciales]

        if len(self.passw.value) <= 8 or len(type_digits) == 0 or len(type_majucules) or len(type_speciales) == 0:
            pass
        
        else:
            # Mettre à jour
            pass

    def connexion(self, e):
        pass





import time
import flet as ft
from utils.useful_functions import is_correct_pasword
from utils import login_style, AnyButton, field_mail_style, readonly_date_style
from utils.constantes import FIRST_COLOR, SECOND_COLOR
import backend as be


class FirstLogin(ft.View):
    def __init__(self, page):

        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            route="/first_login", bgcolor="#f2f2f2"
        )
        self.page = page

        self.login = ft.TextField(
            **readonly_date_style, prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED, label="Login",
        )
        self.email = ft.TextField(
            **field_mail_style, prefix_icon=ft.icons.MAIL_OUTLINED, label="email",
            on_blur=self.changement_email
        )
        self.passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Password",
            on_blur=self.changement_pass
        )
        self.confirm_passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Confirmez",
            on_blur=self.changement_confirm
        )
        self.bt_connect = AnyButton(FIRST_COLOR, "check", "Valider", "white", None,self.connexion)
        self.bt_accueil = AnyButton(
            FIRST_COLOR, "check", "retour", "white", None,
            lambda e: self.page.go("/")
        )

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
        self.text = ft.Text(size=9, font_family="Poppins Italic", color="grey")
        self.card = ft.Card(
            elevation=10, surface_tint_color="white",
            content=ft.Container(
                border_radius=16, padding=20, width=250, bgcolor="white",
                content=ft.Column(
                    controls=[
                        ft.Text("Inscription".upper(), size=16, font_family="Poppins Bold"),
                        ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text("Email et login", size=12, font_family="Poppins Bold"),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),
                        self.email, self.login,
                        ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text("Mot de passe", size=12, font_family="Poppins Bold"),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),
                        ft.Text(
                            f"Le mot de passe doit contenir au moins\n"
                            f"un caractère spécial, un nombre et une majuscule",
                            size=8, font_family="Poppins Italic", color="grey"
                        ),
                        self.passw, self.confirm_passw,
                        ft.Divider(height=1, color="transparent"),
                        self.bt_connect, self.bt_accueil
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
            self.email.suffix_icon = ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED
            self.email.update()
            nom = be.search_user_by_mail(self.email.value)["nom"].lower()
            prenom = be.search_user_by_mail(self.email.value)["prenom"].lower()
            self.login.value = f"{prenom}.{nom}"
            self.login.update()
        else:
            self.email.suffix_icon = None
            self.email.update()

    def changement_pass(self, e):
        if is_correct_pasword(self.passw.value):
            self.passw.suffix_icon = ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED
            self.passw.update()
        else:
            # Mettre à jour
            self.passw.suffix_icon = None
            self.passw.update()
            self.box.title.value = "Erreur"
            self.box.content.value = (f"Le mot de passe doit contenir au moins:\n"
                                      "- Un chiffre\n"
                                      "- Une majuscule\n"
                                      "- Un caractère spécial")
            self.box.open = True
            self.box.update()

    def changement_confirm(self, e):
        if  self.passw.suffix_icon == ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED and self.confirm_passw.value == self.passw.value:
            self.confirm_passw.suffix_icon = ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED
            self.confirm_passw.update()
        else:
            self.confirm_passw.suffix_icon = None
            self.confirm_passw.update()

    def connexion(self, e):
        if self.confirm_passw.value == self.passw.value and self.email.suffix_icon == ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED:
            be.make_user_new(self.login.value, self.passw.value, self.email.value)
            self.box.title.value = "Activation"
            self.box.content.value = "Compte activé"
            self.box.open = True
            self.box.update()
            self.page.go("/")
        else:
            self.box.title.value = "Erreur"
            self.box.content.value = "Toutes les cases doivent être cochées"
            self.box.open = True
            self.box.update()





import flet as ft
from utils import login_style, AnyButton
from utils.constantes import FIRST_COLOR


class FirstLogin(ft.View):
    def __init__(self, page):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            route="/first_connexion", bgcolor="#f2f2f2"
        )
        self.page = page

        self.login = ft.TextField(
            **login_style, prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED, label="Login"
        )
        self.confirm_pass = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Confirmez",
            password=True, can_reveal_password=True
        )
        self.passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Pass",
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
        self.card = ft.Card(
            elevation=10, surface_tint_color="white",
            content=ft.Container(
                border_radius=16, padding=20, width=230, bgcolor="white",
                content=ft.Column(
                    controls=[
                        ft.Text("FOMIGEST".upper(), size=18, font_family="Poppins Bold"),
                        ft.Divider(height=1, color="transparent"),
                        ft.Column(
                            controls=[
                                ft.Text("ENtrez vos informations".upper(), size=11, font_family="Poppins Medium"),
                                ft.Divider(thickness=1, height=1),
                            ], spacing=0,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Divider(height=1, color="transparent"),
                        self.login, self.passw, self.confirm_pass, self.bt_connect,
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
        self.page.go("/welcome")




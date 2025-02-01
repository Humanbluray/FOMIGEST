import flet as ft
import datetime
from utils.lateral_menu import Menu
from utils.constantes import FIRST_COLOR, SECOND_COLOR, THIRD_COLOR
from pages.landing.landing import user_infos


class Welcome(ft.View):
    def __init__(self, page):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            route=f"/welcome/{user_infos['username']}",
            bgcolor="#f2f2f2"
        )
        self.user_infos = user_infos
        self.page = page
        self.menu = Menu(self, page)
        self.barre = ft.Container(
            content=ft.Column(controls=[self.menu]),
            border_radius=12, width=180,
        )
        self.contenu = ft.Container(
            border_radius=0, padding=0,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Text(""),
                        ], alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            )
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
        self.fp_print_devis = ft.FilePicker()
        self.fp_print_facture = ft.FilePicker()
        self.dp_paiement = ft.DatePicker(
            first_date=datetime.datetime(year=2025, month=1, day=1),
            last_date=datetime.datetime(year=2099, month=10, day=1),
        )

        for widget in (self.box, self.fp_print_devis, self.fp_print_facture, self.dp_paiement):
            self.page.overlay.append(widget)

        self.controls = [
            ft.Container(
                expand=True, margin=5,
                content=ft.Row(
                    controls=[self.barre,self.contenu],
                    spacing=10, vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
        ]

    def close_box(self, e):
        self.box.open = False
        self.box.update()




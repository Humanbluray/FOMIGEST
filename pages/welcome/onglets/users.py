from utils import *
import flet as ft
import backend as be
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


class FicheUser(ft.Container):
    def __init__(self, cp: object, infos: dict):
        super().__init__(
            padding=10,
        )
        self.cp = cp
        self.infos = infos
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            shape=ft.BoxShape.CIRCLE, width=50, border=ft.border.all(1, FIRST_COLOR),
                            bgcolor="white",
                            content=ft.Image(src="assets/images/homme.png", fit=ft.ImageFit.CONTAIN)
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(f"{infos['nom']} {infos['prenom']}", size=13, font_family="Poppins Medium"),
                                ft.Text(f"{infos['poste']}", size=12, font_family="Poppins Medium", color="grey")
                            ], spacing=3
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        CtButton("edit_outlined", None, "Modifier", infos, None),
                        CtButton("delete_outlined", None, "Modifier", infos, None),
                    ]
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )


class User(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp

        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
        self.table = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.main_window = ft.Container(
            expand=True,
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="white",
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor="#f0f0f6", padding=10, border_radius=16,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.PERSON, color="black"),
                                ft.Text("Utilisateurs".upper(), size=24, font_family="Poppins Bold"),
                            ]
                        )
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.search, self.results
                                ]
                            ),
                            AnyButton(FIRST_COLOR, "add", "Créer utilisateur", "white", 190, None)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    self.table
                ]
            )
        )
        self.content = ft.Stack(
            controls=[
                self.main_window
            ], alignment=ft.alignment.center
        )
        self.load_datas()

    def load_datas(self):
        users = be.all_users()

        for data in self.table.controls[:]:
            self.table.controls.remove(data)

        for user in users:
            self.table.controls.append(
                FicheUser(self, user)
            )

        self.results.value = f"{len(users)}"

    def filter_datas(self, e):
        pass


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
    def __init__(self, infos: dict):
        super().__init__(
            padding=10,
        )
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            shape=ft.BoxShape.CIRCLE, width=50, border=ft.border.all(1, FIRST_COLOR),
                            bgcolor="white",
                            content=ft.Image(src="assets/images/homme.png", fit=ft.ImageFit.CONTAIN)
                        ),
                        
                    ]
                )
            ]
        )


class User(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp

        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
        self.table = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Date".upper())),
                ft.DataColumn(ft.Text("numero".upper())),
                ft.DataColumn(ft.Text("client".upper())),
                ft.DataColumn(ft.Text("Montant".upper())),
                ft.DataColumn(ft.Text("Actions".upper())),
            ]
        )
        self.main_window = ft.Container(
            expand=True,
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="white",
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor="#f0f0f6", padding=10, border_radius=16,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.MONETIZATION_ON, color="black"),
                                ft.Text("Devis".upper(), size=24, font_family="Poppins Bold"),
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
                            AnyButton(FIRST_COLOR, "add", "Créer devis", "white", 175, self.open_new_window)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.ListView(expand=True, controls=[self.table])
                ]
            )
        )
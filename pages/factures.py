from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur


class Factures(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp

        self.main_window = ft.Container(
            expand=True,
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="white",
            content=ft.Column(
                controls=[

                ]
            )
        )

        self.content = ft.Column(

        )

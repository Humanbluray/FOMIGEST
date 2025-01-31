import flet as ft
from utils.constantes import FIRST_COLOR
from pages.welcome.onglets.clients import Clients
from pages.welcome.onglets.devis import Devis
from pages.welcome.onglets.stock import Stock
from pages.welcome.onglets.factures import Factures
from pages.welcome.onglets.fournisseurs import Fournisseurs
from pages.welcome.onglets.users import User
from pages.landing.landing import user_infos


class ItemMenu(ft.Container):
    def __init__(self, title: str, my_icon: str, selected_icon_color: str, selected_text_color: str):
        super(ItemMenu, self).__init__(
            on_hover=self.hover_ct,
            shape=ft.BoxShape.RECTANGLE,
            padding=ft.padding.only(10, 9, 0, 9),
            border_radius=16,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)
        )
        self.title = title
        self.my_icon = my_icon
        self.is_clicked = False
        self.selected_icon_color = selected_icon_color
        self.selected_text_color = selected_text_color

        self.visuel = ft.Icon(my_icon, size=18, color=selected_icon_color)
        self.name = ft.Text(title, size=12, font_family="Poppins Medium", color=selected_text_color)

        self.content = ft.Row(controls=[self.visuel, self.name], alignment=ft.MainAxisAlignment.START)

    def hover_ct(self, e):
        if e.data == "true":
            e.control.scale = 1.15
            e.control.visuel.color = FIRST_COLOR
            e.control.name.color = FIRST_COLOR
            e.control.bgcolor = "#f2f2f2"
            e.control.name.font_family = "Poppins Medium"
            e.control.visuel.update()
            e.control.name.update()
            e.control.update()
        else:
            if self.is_clicked:
                self.visuel.color = "white"
                self.name.font_family = "Poppins Bold"
                self.name.color = "white"
                self.bgcolor = FIRST_COLOR
                self.visuel.update()
                self.name.update()
                self.update()
            else:
                self.visuel.color = self.selected_icon_color
                self.name.font_family = "Poppins Medium"
                self.name.color = self.selected_text_color
                self.bgcolor = None
                self.visuel.update()
                self.name.update()
                self.update()

            e.control.scale = 1
            e.control.update()

    def set_is_clicked_true(self):
        self.is_clicked = True
        self.visuel.color = "white"
        self.name.font_family = "Poppins Bold"
        self.name.color = "white"
        self.bgcolor = FIRST_COLOR
        self.visuel.update()
        self.name.update()
        self.update()

    def set_is_clicked_false(self):
        self.is_clicked = False
        self.visuel.color = self.selected_icon_color
        self.bgcolor = None
        self.name.font_family = "Poppins Medium"
        self.name.color = self.selected_text_color
        self.visuel.update()
        self.name.update()
        self.update()


class Menu(ft.Card):
    def __init__(self, cp: object, page: ft.Page):
        super(Menu, self).__init__(
            elevation=0,
            expand=True,
        )
        self.page = page
        self.cp = cp  # Conteneur parent
        self.color_icon = ft.colors.BLACK38
        self.color_text = ft.colors.BLACK87

        self.clients = ItemMenu("clients".upper(), ft.icons.GROUP_WORK_OUTLINED, self.color_icon, self.color_text)
        self.fournisseurs = ItemMenu("Prestataires".upper(), ft.icons.GROUPS_2_OUTLINED, self.color_icon, self.color_text)
        self.stock = ItemMenu("stock".upper(), ft.icons.HOME_OUTLINED, self.color_icon, self.color_text)
        self.commandes = ItemMenu("commandes".upper(), ft.icons.BOOKMARK_BORDER_OUTLINED, self.color_icon, self.color_text)
        self.devis = ItemMenu("devis".upper(), ft.icons.MONETIZATION_ON_OUTLINED, self.color_icon, self.color_text)
        self.factures = ItemMenu("factures".upper(), ft.icons.PAYMENTS_OUTLINED, self.color_icon, self.color_text)
        self.users = ItemMenu("utilisateurs".upper(), ft.icons.PERSON_OUTLINE_OUTLINED, self.color_icon, self.color_text)

        self.children = [
            self.clients, self.fournisseurs, self.stock, self.commandes, self.devis, self.factures, self.users
        ]

        for item in self.children:
            item.on_click = self.cliquer_menu

        self.content = ft.Container(
            padding=ft.padding.only(20, 15, 20, 15),
            border_radius=12, bgcolor="white",
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(
                                padding=ft.padding.only(10, 5, 10, 5),
                                border_radius=10, bgcolor="#f2f2f2",
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=18, color="black87",
                                                tooltip=f"{user_infos['username']}".upper()),
                                        ft.Text(f"{user_infos['userlogin']}".upper(), size=12, font_family="Poppins Medium"),

                                    ], alignment=ft.MainAxisAlignment.START
                                )
                            ),
                            ft.Divider(height=2, color="transparent"),
                            ft.Divider(height=1, thickness=1),
                            ft.Divider(height=2, color="transparent"),
                            ft.Column(
                                controls=[
                                    self.clients, self.fournisseurs, self.stock, self.commandes,
                                    self.devis, self.factures, self.users
                                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            # ft.Container(
                            #     padding=ft.padding.only(10, 3, 10, 3), bgcolor="#f2f2f2",
                            #     border=ft.border.all(1, "grey"), border_radius=10,
                            #     content=ft.Row(
                            #         controls=[
                            #             ft.Icon(ft.icons.VERIFIED_USER_OUTLINED, size=16, color="black87"),
                            #             ft.Text(f"{user_infos['userlogin']}", size=12, font_family="Poppins Medium")
                            #         ], alignment=ft.MainAxisAlignment.CENTER, spacing=0
                            #     ),
                            # ),
                            ft.Divider(height=1, thickness=1),
                            ft.Column(
                                controls=[
                                    ft.Text("FOMIGEST V2.0", size=11, font_family="Poppins Medium"),
                                    ft.Text("BY VAN TECH", size=11, font_family="Poppins Medium"),
                                ], spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ], spacing=30,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    def cliquer_menu(self, e):
        for item in self.children:
            item.set_is_clicked_false()

        e.control.set_is_clicked_true()
        e.control.update()

        for row in self.cp.contenu.content.controls[:]:
            self.cp.contenu.content.controls.remove(row)

        if e.control.name.value == "Clients".upper():
            self.cp.contenu.content.controls.append(Clients(self.cp))
            self.cp.update()

        if e.control.name.value == "devis".upper():
            self.cp.contenu.content.controls.append(Devis(self.cp))
            self.cp.update()

        if e.control.name.value == "stock".upper():
            self.cp.contenu.content.controls.append(Stock(self.cp))
            self.cp.update()

        if e.control.name.value == "factures".upper():
            self.cp.contenu.content.controls.append(Factures(self.cp))
            self.cp.update()

        if e.control.name.value == "prestataires".upper():
            self.cp.contenu.content.controls.append(Fournisseurs(self.cp))
            self.cp.update()

        if e.control.name.value == "utilisateurs".upper():
            self.cp.contenu.content.controls.append(User(self.cp))
            self.cp.update()







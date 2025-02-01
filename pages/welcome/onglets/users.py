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
                            shape=ft.BoxShape.CIRCLE, width=50,
                            bgcolor="#f2f2f2",
                            content=ft.Image(src="assets/images/homme.png", fit=ft.ImageFit.CONTAIN)
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(f"{infos['nom']} {infos['prenom']}", size=13, font_family="Poppins Medium"),
                                ft.Text(f"{infos['poste']} | {infos['niveau']}", size=12, font_family="Poppins Medium", color="grey")
                            ], spacing=3
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        CtButton("edit_outlined", None, "Modifier", infos, self.open_edit_window),
                        CtButton("delete_outlined", None, "Modifier", infos, None),
                    ], spacing=0
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def open_edit_window(self, e):
        self.cp.edit_window.scale = 1
        self.cp.edit_window.update()

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
                            AnyButton(FIRST_COLOR, "add", "Créer utilisateur", "white", 190, self.open_new_window)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    self.table
                ]
            )
        )

        # new window ...
        self.new_nom = ft.TextField(**field_style, width=400, label="Nom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_prenom = ft.TextField(**field_style, width=400, label="Prenom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_email = ft.TextField(**field_mail_style, width=300, label="email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_poste = ft.TextField(**field_style, width=250, label="Prenom", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_niveau = ft.Dropdown(
            **drop_style, width=250, prefix_icon=ft.icons.SETTINGS_ACCESSIBILITY_OUTLINED,
            options=[
                ft.dropdown.Option("administrateur".upper()),
                ft.dropdown.Option("consultant".upper()),
                ft.dropdown.Option("operateur".upper())
            ]
        )
        self.new_bt_user = AnyButton(
            FIRST_COLOR, None, "Valider", "white", None, None
        )

        self.new_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=575,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", border_radius=16,
                content=ft.Container(
                    padding=10, bgcolor="white", border_radius=16,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor="#f0f0f6", padding=10, border_radius=16,
                                content=ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.icons.PERSON_ADD_ALT_1_OUTLINED, "black"),
                                                ft.Text("Nouvel utilisateur".upper(), size=14, font_family="Poppins Bold")
                                            ]
                                        ),
                                        ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                                      on_click=self.close_new_window)
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ),
                            ft.Container(
                                bgcolor="white", padding=20, border_radius=16,
                                content=ft.Column(
                                    controls=[
                                        self.new_nom, self.new_prenom, self.new_email,
                                        self.new_poste, self.new_niveau, self.new_bt_user
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        )

        # new window ...
        self.new_nom = ft.TextField(**field_style, width=400, label="Nom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_prenom = ft.TextField(**field_style, width=400, label="Prenom",
                                       prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_email = ft.TextField(**field_mail_style, width=300, label="email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_poste = ft.TextField(**field_style, width=250, label="Prenom", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_niveau = ft.Dropdown(
            **drop_style, width=250, prefix_icon=ft.icons.SETTINGS_ACCESSIBILITY_OUTLINED,
            label="Niveau d'accès",
            options=[
                ft.dropdown.Option("administrateur".upper()),
                ft.dropdown.Option("consultant".upper()),
                ft.dropdown.Option("operateur".upper())
            ]
        )
        self.new_bt_user = AnyButton(
            FIRST_COLOR, None, "Valider", "white", None, None
        )

        self.new_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=575,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", border_radius=16,
                content=ft.Container(
                    padding=10, bgcolor="white", border_radius=16,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor="#f0f0f6", padding=10, border_radius=16,
                                content=ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.icons.PERSON_ADD_ALT_1_OUTLINED, "black"),
                                                ft.Text("Nouvel utilisateur".upper(), size=14,
                                                        font_family="Poppins Bold")
                                            ]
                                        ),
                                        ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                                      on_click=self.close_new_window)
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ),
                            ft.Container(
                                bgcolor="white", padding=20, border_radius=16,
                                content=ft.Column(
                                    controls=[
                                        self.new_nom, self.new_prenom, self.new_email, self.new_poste, self.new_niveau,
                                        self.new_bt_user
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        )

        # edit window ...
        self.edit_nom = ft.TextField(**field_style, width=400, label="Nom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.edit_prenom = ft.TextField(**field_style, width=400, label="Prenom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.edit_email = ft.TextField(**field_mail_style, width=300, label="email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_poste = ft.TextField(**field_style, width=250, label="Prenom", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_niveau = ft.Dropdown(
            **drop_style, width=300, prefix_icon=ft.icons.SETTINGS_ACCESSIBILITY_OUTLINED, label="Modifier niveau accès",
            options=[
                ft.dropdown.Option("administrateur".upper()),
                ft.dropdown.Option("consultant".upper()),
                ft.dropdown.Option("operateur".upper())
            ]
        )
        self.edit_level = ft.TextField(**readonly_field_style, label="Niveau actuel")
        self.edit_bt_user = AnyButton(
            FIRST_COLOR, None, "Valider", "white", None, None
        )
        self.edit_desactivate_user = AnyButton(
            SECOND_COLOR, None, "Désactiver utilisateur", "white", None, None
        )
        self.edit_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=575,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", border_radius=16,
                content=ft.Container(
                    padding=10, bgcolor="white", border_radius=16,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor="#f0f0f6", padding=10, border_radius=16,
                                content=ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.icons.PERSON_ADD_ALT_1_OUTLINED, "black"),
                                                ft.Text("Editer utilisateur".upper(), size=14,
                                                        font_family="Poppins Bold")
                                            ]
                                        ),
                                        ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                                      on_click=self.close_edit_window)
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ),
                            ft.Container(
                                bgcolor="white", padding=20, border_radius=16,
                                content=ft.Column(
                                    controls=[
                                        self.edit_nom,
                                        self.edit_prenom, self.edit_email, self.edit_poste, self.edit_level, self.edit_niveau,
                                        self.edit_bt_user, self.edit_desactivate_user
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        )


        self.content = ft.Stack(
            controls=[
                self.main_window, self.new_window, self.edit_window
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

        self.results.value = f"{len(users)} Résultat(s)"

    def filter_datas(self, e):
        users = be.all_users()
        search = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: search in x["nom"] or search in x["prenom"], users))

        for data in self.table.controls[:]:
            self.table.controls.remove(data)

        for user in filtered_datas:
            self.table.controls.append(
                FicheUser(self, user)
            )

        self.results.value = f"{len(filtered_datas)} résultat(s)"
        self.results.update()
        self.table.update()

    def open_new_window(self, e):
        self.new_window.scale = 1
        self.new_window.update()

    def close_new_window(self, e):
        self.new_window.scale = 0
        self.new_window.update()

    def close_edit_window(self, e):
        self.edit_window.scale = 0
        self.edit_window.update()




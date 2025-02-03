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
            padding=10, on_click=self.open_activity_window
        )
        self.cp = cp
        self.infos = infos

        if infos['statut'] == 'ACTIF':
            icone = ft.icons.CHECK_CIRCLE_OUTLINE_SHARP
            color = ft.colors.BLACK87
        elif infos['statut'] == "INACTIF":
            icone = ft.icons.INDETERMINATE_CHECK_BOX
            color = ft.colors.RED_300
        else:
            icone = ft.icons.TIMELAPSE_OUTLINED
            color = ft.colors.BLUE_400

        self.content = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    icone, color, 16
                                ),
                                ft.Text(f"{infos['nom']} {infos['prenom']}", size=13, font_family="Poppins Bold"),
                            ]
                        ),
                        ft.Text(f"{infos['poste']} | {infos['niveau']}", size=12, font_family="Poppins Medium",
                                color="grey")
                    ], spacing=3
                ),
                ft.Row(
                    controls=[
                        CtButton("edit_outlined", None, "Modifier", infos, self.open_edit_window),
                        CtButton(ft.icons.DELETE_FOREVER_OUTLINED, None, "Désactiver", infos, self.descativer_user),
                    ], spacing=0
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def open_edit_window(self, e):
        self.cp.edit_nom.value = self.infos["nom"]
        self.cp.edit_prenom.value = self.infos["prenom"]
        self.cp.edit_email.value = self.infos["email"]
        self.cp.edit_poste.value = self.infos["poste"]
        self.cp.edit_level.value = self.infos["niveau"]

        for widget in (
            self.cp.edit_nom, self.cp.edit_prenom, self.cp.edit_level,
            self.cp.edit_poste, self.cp.edit_email
        ):
            widget.update()

        self.cp.edit_window.scale = 1
        self.cp.edit_window.update()

    def descativer_user(self, e):
        be.desactivate_user(self.infos['email'])
        self.cp.cp.box.title.value = "Confirmé"
        self.cp.cp.box.content.value = "Utilisateur désactivé"
        self.cp.cp.box.open = True
        self.cp.cp.box.update()

        self.cp.load_datas()
        self.cp.table.update()
        self.cp.results.update()

    def open_activity_window(self, e):
        self.cp.activity_window.scale = 1
        self.cp.activity_window.update()


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
        self.new_nom = ft.TextField(**field_style, width=250, label="Nom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_prenom = ft.TextField(**field_style, width=250, label="Prenom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_email = ft.TextField(**field_mail_style, width=250, label="email", prefix_icon=ft.icons.MAIL_OUTLINED)
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
            elevation=20, surface_tint_color="#f0f0f6", width=290, height=580,
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
        self.new_nom = ft.TextField(**field_style, width=250, label="Nom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_prenom = ft.TextField(**field_style, width=250, label="Prenom",
                                       prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.new_email = ft.TextField(**field_mail_style, width=250, label="email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_poste = ft.TextField(**field_style, width=250, label="Poste", prefix_icon=ft.icons.SUPERVISED_USER_CIRCLE_OUTLINED)
        self.new_niveau = ft.Dropdown(
            **drop_style, width=190, prefix_icon=ft.icons.SETTINGS_ACCESSIBILITY_OUTLINED,
            label="Niveau d'accès",
            options=[
                ft.dropdown.Option("administrateur".upper()),
                ft.dropdown.Option("consultant".upper()),
                ft.dropdown.Option("operateur".upper())
            ]
        )
        self.new_bt_user = AnyButton(
            FIRST_COLOR, None, "Valider", "white", 250, self.create_user
        )

        self.new_window = ft.Card(
            elevation=10, surface_tint_color="#f0f0f6", width=300, height=450,
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
                                                ft.Text("Nouveau".upper(), size=14,
                                                        font_family="Poppins Bold")
                                            ]
                                        ),
                                        ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                                      on_click=self.close_new_window)
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ),
                            ft.Container(
                                bgcolor="white", padding=10, border_radius=16,
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
        self.edit_nom = ft.TextField(**field_style, width=250, label="Nom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.edit_prenom = ft.TextField(**field_style, width=250, label="Prenom", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.edit_email = ft.TextField(**field_mail_style, width=250, label="email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_poste = ft.TextField(**field_style, width=250, label="Prenom", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_niveau = ft.Dropdown(
            **drop_style, width=190, prefix_icon=ft.icons.SETTINGS_ACCESSIBILITY_OUTLINED, label="Modifier niveau accès",
            options=[
                ft.dropdown.Option("administrateur".upper()),
                ft.dropdown.Option("consultant".upper()),
                ft.dropdown.Option("operateur".upper())
            ]
        )
        self.edit_level = ft.TextField(**readonly_date_style, label="Niveau d'acces actuel", width=250)
        self.edit_bt_user = AnyButton(
            FIRST_COLOR, None, "Valider Modifications", "white", None, None
        )
        self.edit_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=300, height=550,
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
                                bgcolor="white", padding=10, border_radius=16,
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ColoredCtButton(
                                                    ft.icons.RECYCLING_OUTLINED, "blue", "Récativer",
                                                    None, self.reactiver_user
                                                ),
                                                ColoredCtButton(
                                                    "delete_outlined", "red",
                                                    "Supprimer", None, self.delete_user
                                                ),
                                            ], spacing=5, alignment = ft.MainAxisAlignment.END
                                        ),
                                        self.edit_nom,
                                        self.edit_prenom, self.edit_email, self.edit_poste, self.edit_level, self.edit_niveau,
                                        self.edit_bt_user,
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        )

        # actvite
        self.activity_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=700, height=580,
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
                                                ft.Icon(ft.icons.HISTORY_OUTLINED, "black"),
                                                ft.Text("Activité".upper(), size=14,
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
                self.main_window, self.new_window, self.edit_window, self.activity_window
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

    def create_user(self, e):
        count = 0
        for widget in (self.new_nom, self.new_prenom, self.new_poste, self.new_email, self.new_niveau):
            if widget.value == "" or widget.value is None:
                count += 1

        if count == 0:
            be.add_user(
                self.new_nom.value, self.new_prenom.value, self.new_email.value,
                self.new_niveau.value, self.new_poste.value
            )
            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Utilisateur créé"
            self.cp.box.open = True
            self.cp.box.update()

            for widget in (self.new_nom, self.new_prenom, self.new_poste, self.new_email, self.new_niveau):
                widget.value = None
                widget.update()

            self.load_datas()
            self.table.update()
            self.results.update()
        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

    def delete_user(self, e):
        if be.search_user_by_mail(self.edit_email.value)['statut'] == "INACTIF":
            be.delete_user(self.edit_email.value)
            self.load_datas()
            self.table.update()
            self.results.update()

            self.edit_window.scale = 0
            self.edit_window.update()

            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Utilisateur supprimé"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Vous devez d'abord désactiver le compte avant suppression"
            self.cp.box.open = True
            self.cp.box.update()


    def reactiver_user(self, e):
        statut = be.search_user_by_mail(self.edit_email.value)['statut']

        if statut == "ACTIF":
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Cet utlisateur est déja actif"
            self.cp.box.open = True
            self.cp.box.update()

        elif statut == "NOUVEAU":
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Statut en attente de validation"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            be.reactivate_user(self.edit_email.value)
            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Utilisateur réactivé"
            self.cp.box.open = True
            self.cp.box.update()
            self.load_datas()
            self.table.update()
            self.results.update()

            self.edit_window.scale = 0
            self.edit_window.update()


from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur, ecrire_en_lettres


class FicheFourn(ft.Container):
    def __init__(self, cp: object, infos: dict):
        super().__init__(
            padding=10, bgcolor="white"
        )
        self.cp = cp
        self.infos = infos

        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            **readonly_field_style, width=300, value=infos["nom"],
                            label="Nom fournisseur", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED
                        ),
                        ft.TextField(
                            **readonly_field_style, width=120, label="initiales", value=infos["initiales"]
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        CtButton("edit_outlined", ft.colors.BLUE_300,"Modifier", infos, self.open_edit_window),
                        CtButton(ft.icons.LIST, ft.colors.BLACK45, "Voir commandes", infos, self.voir_commandes)
                    ], spacing=0
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def open_edit_window(self, e):
        self.cp.edit_window.scale = 1
        self.cp.edit_window.update()
        self.cp.edit_id.value = self.infos["id"]
        self.cp.edit_name.value = self.infos["nom"]
        self.cp.edit_ini.value = self.infos["initiales"]
        self.cp.edit_contact.value = self.infos["contact"]
        self.cp.edit_nui.value = self.infos["NUI"]
        self.cp.edit_rc.value = self.infos["RC"]
        self.cp.edit_courriel.value = self.infos["courriel"]
        self.cp.edit_commercial.value = self.infos["commercial"]

        for widget in [
            self.cp.edit_id,
            self.cp.edit_name, self.cp.edit_ini, self.cp.edit_contact, self.cp.edit_nui, self.cp.edit_rc,
            self.cp.edit_courriel, self.cp.edit_commercial,
        ]:
            widget.update()

    def voir_commandes(self, e):
        datas = be.all_commandes_by_fournisseur_id(e.control.data["id"])
        self.cp.fourn_num.value = e.control.data["nom"]
        self.cp.fourn_num.update()

        for row in self.cp.table_commandes.rows[:]:
            self.cp.table_commandes.rows.remove(row)

        for data in datas:
            self.cp.table_commandes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["date"])),
                        ft.DataCell(ft.Text(data["numero"])),
                        ft.DataCell(ft.Text(data["montant"])),
                    ]
                )
            )

        self.cp.table_commandes.update()
        self.cp.com_window.scale = 1
        self.cp.com_window.update()


class Fournisseurs(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp
        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
        #
        self.table = ft.ListView(expand=True, spacing=10, divider_thickness=1)
        self.main_window = ft.Container(
            expand=True,
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="white",
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        bgcolor="#f0f0f6", padding=10, border_radius=16,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.GROUPS, color="black"),
                                ft.Text("Prestataires".upper(), size=24, font_family="Poppins Bold"),
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
                            AnyButton(FIRST_COLOR, "add", "Nouveau fournisseur", "white", 200, self.open_new_window)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    self.table
                ]
            )
        )

        # Edit window ...
        self.edit_id = ft.Text("", size=11, visible=False)
        self.edit_name = ft.TextField(**field_style, width=400, label="Nom du fournisseur",
                                      prefix_icon=ft.icons.PERSON_PIN_OUTLINED)
        self.edit_ini = ft.TextField(**field_style, width=120, label="Initiales", )
        self.edit_contact = ft.TextField(**numbers_field_style, width=170, label="Contact",
                                         prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)
        self.edit_nui = ft.TextField(**field_style, width=200, label="NUI")
        self.edit_rc = ft.TextField(**field_style, width=200, label="RC")
        self.edit_courriel = ft.TextField(**field_style, width=200, label="Email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_commercial = ft.TextField(**field_style, width=400, label="Commercial",
                                            prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.bt_edit = AnyButton(FIRST_COLOR, "edit", "Modifier", "white", 170, self.update_fourn)
        self.edit_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=500,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), border_radius=16, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon("edit_outlined", "black"),
                                            ft.Text("Modifier fournisseur".upper(), size=14, font_family="Poppins Bold")
                                        ]
                                    ),
                                    ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="white",
                                                  on_click=self.close_edit_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            bgcolor="white", padding=20, border_radius=16,
                            content=ft.Column(
                                controls=[
                                    self.edit_id,
                                    self.edit_name, self.edit_ini, self.edit_contact, self.edit_nui, self.edit_rc,
                                    self.edit_courriel, self.edit_commercial,
                                    self.bt_edit,
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # new window ...
        self.new_name = ft.TextField(**field_style, width=400, label="Nom du fournisseur",
                                     prefix_icon=ft.icons.PERSON_PIN_OUTLINED)
        self.new_ini = ft.TextField(**field_style, width=120, label="Initiales", )
        self.new_contact = ft.TextField(**numbers_field_style, width=170, label="Contact",
                                        prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)
        self.new_nui = ft.TextField(**field_style, width=200, label="NUI")
        self.new_rc = ft.TextField(**field_style, width=200, label="RC")
        self.new_courriel = ft.TextField(**field_style, width=200, label="Email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_commercial = ft.TextField(**field_style, width=400, label="Commercial",
                                           prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.bt_new = AnyButton(FIRST_COLOR, "edit", "Créer", "white", 170, self.create_fourn)
        self.new_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=500,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            bgcolor="white", padding=ft.padding.only(10, 5, 10, 5), border_radius=16,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.PERSON_ADD_ALT_1, "black"),
                                            ft.Text("Créer fournisseur".upper(), size=14, font_family="Poppins Bold")
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
                                    self.new_name, self.new_ini, self.new_contact, self.new_nui, self.new_rc,
                                    self.new_courriel, self.new_commercial,
                                    self.bt_new,
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # Tables des commandes
        self.table_commandes = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("Date".upper())),
                ft.DataColumn(ft.Text("numero".upper())),
                ft.DataColumn(ft.Text("montant".upper())),
            ]
        )
        self.fourn_num = ft.Text(size=12, font_family="Poppins Medium", color="white")
        self.com_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=500,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6",
                content=ft.Container(
                    bgcolor="white", padding=20, border_radius=16,
                    content=ft.Column(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Text("Fournisseur", size=12, font_family="Poppins Medium"),
                                                    ft.Container(
                                                        padding=ft.padding.only(10, 3, 10, 3),
                                                        border_radius=101, bgcolor=SECOND_COLOR, content=ft.Row(
                                                            controls=[self.fourn_num]
                                                        )
                                                    )
                                                ]
                                            ),
                                            ft.IconButton(
                                                bgcolor="#f0f0f6", icon="close", icon_color=FIRST_COLOR, scale=0.6,
                                                on_click=self.close_com_window
                                            )
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                    ft.Column(
                                        controls=[
                                            ft.Text("Commandes", size=12, font_family="Poppins Medium", ),
                                            ft.Divider(height=1, thickness=1),
                                        ], spacing=0
                                    ),
                                    ft.Column(
                                        expand=True, scroll=ft.ScrollMode.AUTO,
                                        controls=[self.table_commandes]
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.edit_window, self.new_window, self.com_window
            ], alignment=ft.alignment.center
        )
        self.load_datas()

    def load_datas(self):
        datas = be.all_fournisseurs()
        self.results.value = f"{len(datas)} résultat(s)"

        for widget in self.table.controls[:]:
            self.table.controls.remove(widget)

        for data in datas:
            self.table.controls.append(
                FicheFourn(self, data)
            )

    def filter_datas(self, e):
        datas = be.all_fournisseurs()
        search = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: search in x["nom"] or search in x["initiales"], datas))

        self.results.value = f"{len(filtered_datas)} résultat(s)"
        self.results.update()

        for widget in self.table.controls[:]:
            self.table.controls.remove(widget)

        for data in filtered_datas:
            self.table.controls.append(
                FicheFourn(self, data)
            )
        self.table.update()

    def close_edit_window(self, e):
        self.edit_window.scale = 0
        self.edit_window.update()

    def close_new_window(self, e):
        self.new_window.scale = 0
        self.new_window.update()

    def open_new_window(self, e):
        self.new_window.scale = 1
        self.new_window.update()

    def close_com_window(self, e):
        self.com_window.scale = 0
        self.com_window.update()

    def create_fourn(self, e):
        if self.new_name.value is None or self.new_name.value == "":
            self.cp.box.title.value  = "Erreur"
            self.cp.box.content.value = "Le nom est obligatoire"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            be.add_fournisseur(
                self.new_name.value, self.new_ini.value, self.new_contact.value, self.new_nui.value,
                self.new_rc.value, self.new_courriel.value, self.new_commercial.value
            )
            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Fournisseur créé"
            self.cp.box.open = True
            self.cp.box.update()

            for widget in (
                self.new_name, self.new_ini, self.new_contact, self.new_nui,
                self.new_rc, self.new_courriel, self.new_commercial
            ):
                widget.value = None
                widget.update()

    def update_fourn(self, e):
        if self.edit_name.value is None or self.edit_name.value == "":
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Le nom est obligatoire"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            be.update_fournisseur_by_id(
                self.edit_name.value, self.edit_ini.value, self.edit_contact.value, self.edit_nui.value,
                self.edit_rc.value, self.edit_courriel.value, self.edit_commercial.value, int(self.edit_id.value)
            )
            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Fournisseur modifié"
            self.cp.box.open = True
            self.cp.box.update()

            self.edit_window.scale = 0
            self.edit_window.update()







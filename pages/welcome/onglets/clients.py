from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur


class FicheClient(ft.Container):
    def __init__(self, cp: object, infos: dict):
        super().__init__(padding=10, bgcolor="white", border_radius=10)
        self.cp = cp
        self.infos = infos

        statut = "A jour"
        self.couleur = "green"
        nb_factures = 0
        self.total_impaye = 0
        self.nb_total_fac = 0
        self.nb_total_fac_impaye = 0

        all_factures = be.all_factures_by_client_id(infos["id"])

        for fact in all_factures:
            self.nb_total_fac += 1

            if fact["mt_remise"] >= fact["regle"]:
                self.total_impaye += fact["mt_remise"] - fact["regle"]
                nb_factures += 1
                self.nb_total_fac_impaye += 1

        if self.total_impaye > 0:
            statut = "Pas à jour"
            self.couleur = "red"
            icone = ft.icons.INDETERMINATE_CHECK_BOX
        else:
            statut = "à jour"
            self.couleur = ft.colors.TEAL_500
            icone = ft.icons.CHECK_CIRCLE

        self.statut = statut.upper()

        self.notif = ft.Container(
            shape=ft.BoxShape.CIRCLE, bgcolor="red", padding=5,
            content=ft.Row(
                [ft.Text(f"{self.nb_total_fac_impaye}", size=10, color="white", font_family="Poppins Bold")],
                alignment=ft.MainAxisAlignment.CENTER)
        )

        if self.nb_total_fac_impaye == 0:
            self.notif.visible = False
        else:
            self.notif.visible = True

        self.content = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                          controls=[
                              ft.Icon(ft.icons.PERSON_OUTLINE_OUTLINED, size=18, color="black"),
                              ft.Text(infos["nom"], size=14, font_family="Poppins Medium")
                          ], spacing=3
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(icone, self.couleur, 20),
                                        ft.Text(value=f"Statut : {self.statut}", size=13, font_family="Poppins Bold", color="black")
                                    ],
                                ),
                                ft.Text(value=f"Dette: {ajout_separateur(self.total_impaye)} XAF", color="grey", size=12, font_family="Poppins Italic")
                            ], spacing=0
                        )
                    ]
                ),

                ft.Row(
                    controls=[
                        CtButton(
                            ft.icons.EDIT_OUTLINED, ft.colors.BLUE_300, "Editer", infos,
                            self.open_edit_window
                        ),
                        CtButton(
                            ft.icons.PAYMENT_OUTLINED, ft.colors.BLUE_300, "Editer", infos,
                            self.voir_factures
                        ),
                    ], spacing=2
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

    def voir_factures(self, e):
        self.cp.client.value = self.infos["nom"]
        self.cp.client.update()

        datas = be.all_factures_by_client_id(self.infos["id"])
        total_factures = 0
        total_impayes = 0
        total_reste = 0

        for row in self.cp.table_factures.rows[:]:
            self.cp.table_factures.rows.remove(row)

        for data in datas:
            total_factures += 1
            total_reste += data["reste"]

            if int(total_reste) > 0:
                total_impayes += 1
                my_icon = ft.icons.STOP_CIRCLE_OUTLINED
                my_color = ft.colors.RED
            else:
                my_icon = ft.icons.CHECK_CIRCLE
                my_color = ft.colors.BLACK

            self.cp.table_factures.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["date"])),
                        ft.DataCell(ft.Text(data["numero"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["total"]))),
                        ft.DataCell(ft.Text(ajout_separateur(data["regle"]))),
                        ft.DataCell(ft.Text(ajout_separateur(data["total"]- data["regle"]))),
                        ft.DataCell(ft.Icon(my_icon, my_color, 20))
                    ]
                )
            )

        self.cp.table_factures.update()
        self.cp.factures_window.scale = 1
        self.cp.factures_window.update()


class Clients(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp  # Container parent

        # Main window ...
        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
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
                                ft.Icon(ft.icons.PERSON, color="black"),
                                ft.Text("Clients".upper(), size=24, font_family="Poppins Bold"),
                            ]
                        )
                    ),
                    ft.Divider(height=2, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.search, self.results
                                ], spacing=20
                            ),
                            AnyButton(FIRST_COLOR, "add", "Nouveau client", "white", 200, self.open_new_window)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.table
                ]
            )
        )

        # Edit window ...
        self.edit_id = ft.Text("", size=11, visible=False)
        self.edit_name = ft.TextField(**field_style, width=400, label="Nom du client", prefix_icon=ft.icons.PERSON_PIN_OUTLINED)
        self.edit_ini = ft.TextField(**field_style, width=120, label="Initiales",)
        self.edit_contact = ft.TextField(**numbers_field_style, width=170, label="Contact",prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)
        self.edit_nui = ft.TextField(**field_style, width=200, label="NUI")
        self.edit_rc = ft.TextField(**field_style, width=200, label="RC")
        self.edit_courriel = ft.TextField(**field_mail_style, width=200, label="Email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_commercial = ft.TextField(**field_style, width=400, label="Commercial", prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.bt_edit = AnyButton(FIRST_COLOR, "edit", "Modifier", "white", 170, self.update_client)
        self.edit_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=440, height=575,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", border_radius=16, expand=True,
                content=ft.Container(
                    padding=10, border_radius=16, bgcolor="white", expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor="#f0f0f6", padding=10, border_radius=16,
                                content=ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.icons.PERSON, color="black"),
                                                ft.Text("Modifier".upper(), size=18, font_family="Poppins Bold"),
                                            ]
                                        ),
                                        ft.IconButton(
                                            bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.7,
                                            icon=ft.icons.CLOSE, on_click=self.close_edit_window
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ),
                            ft.Container(
                                bgcolor="white", padding=20, border_radius=16,
                                content=ft.Column(
                                    expand=True, scroll=ft.ScrollMode.AUTO,
                                    controls=[
                                        self.edit_id,
                                        self.edit_name, self.edit_ini, self.edit_contact, self.edit_nui, self.edit_rc, self.edit_courriel, self.edit_commercial,
                                        self.bt_edit,
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        )

        # new window ...
        self.new_name = ft.TextField(**field_style, width=400, label="Nom du client",
                                      prefix_icon=ft.icons.PERSON_PIN_OUTLINED)
        self.new_ini = ft.TextField(**field_style, width=120, label="Initiales", )
        self.new_contact = ft.TextField(**field_style, width=200, label="Contact",
                                         prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)
        self.new_nui = ft.TextField(**field_style, width=200, label="NUI")
        self.new_rc = ft.TextField(**field_style, width=200, label="RC")
        self.new_courriel = ft.TextField(**field_style, width=200, label="Email", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_commercial = ft.TextField(**field_style, width=400, label="Commercial",
                                            prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED)
        self.bt_new = AnyButton(FIRST_COLOR, "edit", "Créer", "white", 170, self.create_client)
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
                                                ft.Icon(ft.icons.PERSON_ADD_ALT_1, "black"),
                                                ft.Text("Nouveau client".upper(), size=18, font_family="Poppins Bold")
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
        )

        # Factures window...
        self.table_factures = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("Date".upper())),
                ft.DataColumn(ft.Text("Numéro".upper())),
                ft.DataColumn(ft.Text("Total".upper())),
                ft.DataColumn(ft.Text("Perçu".upper())),
                ft.DataColumn(ft.Text("reste".upper())),
                ft.DataColumn(ft.Text("Statut".upper())),
            ]
        )
        self.client = ft.Text("", size=12, font_family="Poppins Medium", color="white")
        self.total_percu = ft.Text("", size=18, font_family="Poppins Medium", color="black45")
        self.total_reste = ft.Text("", size=18, font_family="Poppins Medium", color="black45")
        self.factures_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=900, height=500,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), border_radius=16, bgcolor="white",
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.PAYMENTS_OUTLINED, "black"),
                                            ft.Text("Factures".upper(), size=14, font_family="Poppins Bold")
                                        ]
                                    ),
                                    ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="white", on_click=self.close_factures_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            bgcolor="white", padding=20, border_radius=16, expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"Client: ".upper(), size=12, font_family="Poppins Medium"),
                                            ft.Container(
                                                padding=ft.padding.only(10, 3, 10, 3), border_radius=10,
                                                bgcolor=SECOND_COLOR, content=ft.Row(
                                                    controls=[self.client],
                                                    alignment=ft.MainAxisAlignment.CENTER
                                                )
                                            )
                                        ]
                                    ),
                                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                    ft.Container(
                                        padding=ft.padding.only(10, 5, 10, 5),
                                        border_radius=10, expand=True, border=ft.border.all(1, "grey"),
                                        content=ft.ListView(expand=True, controls=[self.table_factures])
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.edit_window, self.new_window, self.factures_window,
            ], alignment=ft.alignment.center
        )
        self.load_datas()

    def load_datas(self):
        all_clients = be.all_clients()
        self.results.value = f"{len(all_clients)} Résultats"

        for row in self.table.controls[:]:
            self.table.controls.remove(row)

        for client in all_clients:
            self.table.controls.append(FicheClient(self, client))

    def filter_datas(self, e):
        all_clients = be.all_clients()
        search = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: search in x["nom"], all_clients ))

        self.results.value = f"{len(filtered_datas)} Résultats"
        self.results.update()

        for row in self.table.controls[:]:
            self.table.controls.remove(row)

        for client in filtered_datas:
            self.table.controls.append(FicheClient(self, client))

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

    def update_client(self, e):
        if self.edit_name.value == "" or self.edit_name is None:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Veuillez entrer un nom"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            be.update_client(
                self.edit_name.value, self.edit_ini.value, self.edit_contact.value, self.edit_nui.value,
                self.edit_rc.value, self.edit_courriel.value, self.edit_commercial.value, int(self.edit_id.value)
            )
            be.add_activity(self.cp.utilisateur["userlogin"], f"Modification du client {self.edit_name.value}")
            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Client modifié"
            self.cp.box.open = True
            self.cp.box.update()

            self.search.value = None
            self.search.update()
            self.load_datas()
            self.table.update()
            self.results.update()
            self.edit_window.scale = 0
            self.edit_window.update()

    def create_client(self, e):
        if self.new_name.value == "" or self.new_name is None:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Veuillez entrer un nom"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            if self.new_ini.value in be.recherche_initiales():
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "Ces initiales sont déjà utilisées"
                self.cp.box.open = True
                self.cp.box.update()
            else:
                be.add_client(
                    self.new_name.value, self.new_ini.value, self.new_contact.value, self.new_nui.value,
                    self.new_rc.value, self.new_courriel.value, self.new_commercial.value,
                )
                be.add_activity(self.cp.utilisateur["userlogin"], f"Création du client {self.new_name.value}")
                self.cp.box.title.value = "Validé"
                self.cp.box.content.value = "Nouveau client créé"
                self.cp.box.open = True
                self.cp.box.update()

                for widget in (self.new_name, self.new_ini, self.new_contact, self.new_nui, self.new_rc, self.new_courriel, self.new_commercial):
                    widget.value = None
                    widget.update()

                self.load_datas()
                self.table.update()
                self.results.update()

    def close_factures_window(self, e):
        self.factures_window.scale = 0
        self.factures_window.update()

    def update_devis(self, e):
        pass

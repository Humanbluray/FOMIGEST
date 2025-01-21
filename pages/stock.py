from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur


class Stock(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp

        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
        self.table = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("Référence".upper())),
                ft.DataColumn(ft.Text("Désignation".upper())),
                ft.DataColumn(ft.Text("Nature".upper())),
                ft.DataColumn(ft.Text("qté".upper())),
                ft.DataColumn(ft.Text("prix".upper())),
                ft.DataColumn(ft.Text("".upper()))
            ]
        )
        self.main_window = ft.Container(
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="white",
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Liste des articles".upper(), size=16, font_family="Poppins Bold"),
                            ft.Divider(height=1, thickness=1)
                        ], spacing=0
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Row([self.search, self.results], spacing=10),
                            AnyButton(FIRST_COLOR, "add", "Nouvel entrée directe", "white", 220, None)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Stack(
                        expand=True,
                        controls=[
                            ft.ListView(expand=True, controls=[self.table]),
                            ft.FloatingActionButton(
                                bgcolor="black",on_click=self.open_new_ref_window,
                                content=ft.Row([ft.Icon(ft.icons.ADD, color="white")],
                                               alignment=ft.MainAxisAlignment.CENTER),
                                bottom=10, scale=0.8, right=10, tooltip="Ajouter référence",
                                opacity=0.8
                            )
                        ], alignment=ft.alignment.bottom_right
                    )
                ]
            )
        )

        # Nouvelle ref window ...
        self.new_ref = ft.TextField(**field_style, width=200, label="Reference", prefix_icon=ft.icons.LABEL_OUTLINED)
        self.new_des = ft.TextField(**field_style, width=600, label="Désignation", prefix_icon=ft.icons.DISCOUNT_OUTLINED)
        self.new_nature  = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.NATURE, width=150, label="Nature",
            options=[ft.dropdown.Option("STOCK"), ft.dropdown.Option("NON STOCK")]
        )
        self.new_unite = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.AD_UNITS, width=150, label="Unité",
            options=[ft.dropdown.Option("U"), ft.dropdown.Option("L"), ft.dropdown.Option("KG"), ft.dropdown.Option("ML")]
        )
        self.new_ref_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=640, height=360,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Text("Nouvel Article".upper(), size=14, font_family="Poppins Medium"),
                                    ft.IconButton("close", bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.6, on_click=self.close_new_ref_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.only(15, 10, 15, 10), bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.new_ref, self.new_des, self.new_nature, self.new_unite,
                                    AnyButton(FIRST_COLOR, "check", "Valider", "white", 170, self.add_new_article)
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # edit ref window ...
        self.edit_id = ft.TextField(**inactive_field_style, width=100, label="ID")
        self.edit_ref = ft.TextField(**inactive_field_style, width=200, label="Reference", prefix_icon=ft.icons.LABEL_OUTLINED)
        self.edit_des = ft.TextField(**field_style, width=600, label="Désignation",
                                    prefix_icon=ft.icons.DISCOUNT_OUTLINED)
        self.edit_nature = ft.TextField(**inactive_field_style, width=100, label="Nature")
        self.edit_unite = ft.TextField(**inactive_field_style, width=100, label="Unité")
        self.edit_ref_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=640, height=390,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Text("Modifier Article".upper(), size=14, font_family="Poppins Medium"),
                                    ft.IconButton("close", bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.6,
                                                  on_click=self.close_edit_ref_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.only(15, 10, 15, 10), bgcolor="white", border_radius=12,
                            content=ft.Column(
                                controls=[
                                    self.edit_id, self.edit_ref, self.edit_des, self.edit_nature, self.edit_unite,
                                    AnyButton(FIRST_COLOR, "edit_outlined", "Modifier", "white", 170, self.update_reference)
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # Historique window
        self.histo_ref = ft.Text(size=12, font_family="Poppins Medium", color="white")
        self.histo_des = ft.TextField(**readonly_field_style2, width=500, label="Désignation", prefix_icon=ft.icons.DISCOUNT_OUTLINED)
        self.histo_unite = ft.TextField(**readonly_field_style2, width=100, label="Unité")
        self.histo_qte = ft.TextField(**readonly_field_style2, width=100, label="Stock")
        self.histo_prix = ft.TextField(**readonly_field_style2, width=200, label="Prix")

        self.histo_table = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("Date".upper())),
                ft.DataColumn(ft.Text("type".upper())),
                ft.DataColumn(ft.Text("N° mvt".upper())),
                ft.DataColumn(ft.Text("Qté avant".upper())),
                ft.DataColumn(ft.Text("Qté mvt".upper())),
                ft.DataColumn(ft.Text("Qté après".upper())),
            ]
        )
        self.histo_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=750, height=600,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(10, 5, 10, 5), bgcolor="white", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Text("Historique d'article".upper(), size=14, font_family="Poppins Medium"),
                                    ft.IconButton("close", bgcolor="#f0f0f6", icon_color=FIRST_COLOR, scale=0.6,
                                                  on_click=self.close_histo_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.only(15, 10, 15, 10), bgcolor="white", border_radius=12,
                            expand=True,
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Référence".upper(), size=12, font_family="Poppins Medium"),
                                            ft.Container(
                                                padding=ft.padding.only(10, 3, 10, 3), bgcolor=SECOND_COLOR,
                                                border_radius=10,
                                                content=ft.Row([self.histo_ref], alignment=ft.MainAxisAlignment.CENTER)
                                            )
                                        ]
                                    ),
                                    self.histo_des,
                                    ft.Row(
                                        controls=[self.histo_unite, self.histo_qte, self.histo_prix]
                                    ),
                                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                    ft.Column(
                                        controls=[
                                            ft.Text("table des mouvements".upper(), size=11, font_family="Poppins Medium", weight=ft.FontWeight.BOLD),
                                            ft.Divider(height=1, thickness=1),
                                        ], spacing=0
                                    ),
                                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                    ft.Container(
                                        padding=ft.padding.only(10, 5, 10, 5), border=ft.border.all(1, "grey"), border_radius=12,
                                        expand=True,
                                        content=ft.ListView(expand=True, controls=[self.histo_table])
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # Content ...
        self.content = ft.Stack(
            controls=[
                self.main_window, self.new_ref_window, self.edit_ref_window, self.histo_window
            ], alignment=ft.alignment.center
        )
        self.load_lists()
        self.load_datas()

    def load_lists(self):
        pass

    def load_datas(self):
        datas = be.all_references()
        self.results.value = f"{len(datas)} Référence(s)"

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in datas:
            if data["nature"].lower() == "stock":
                nature = "S"
            else:
                nature = "N"

            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["reference"])),
                        ft.DataCell(ft.Text(data["designation"])),
                        ft.DataCell(ft.Text(nature)),
                        ft.DataCell(ft.Text(data["qte"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["prix"]))),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    CtButton("edit_outlined", "Modifier", data, self.open_edit_ref_window),
                                    CtButton(ft.icons.LIST, "Historique", data, self.show_historique)
                                ], spacing=0, alignment=ft.MainAxisAlignment.END
                            )
                        )
                    ]
                )
            )

    def filter_datas(self, e):
        datas = be.all_references()
        search = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: search in x["reference"] or search in x["designation"], datas))
        self.results.value = f"{len(filtered_datas)} Référence(s)"

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in filtered_datas:
            if data["nature"].lower() == "stock":
                nature = "S"
            else:
                nature = "N"
            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["reference"])),
                        ft.DataCell(ft.Text(data["designation"])),
                        ft.DataCell(ft.Text(nature)),
                        ft.DataCell(ft.Text(data["qte"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["prix"]))),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    CtButton("edit_outlined", "Modifier", data, self.open_edit_ref_window),
                                    CtButton(ft.icons.LIST, "Historique", data, self.show_historique)
                                ], spacing=0, alignment=ft.MainAxisAlignment.END
                            )
                        )
                    ]
                )
            )

        self.results.update()
        self.table.update()

    def open_new_ref_window(self, e):
        self.new_ref_window.scale = 1
        self.new_ref_window.update()

    def close_new_ref_window(self, e):
        self.new_ref_window.scale = 0
        self.new_ref_window.update()

    def open_edit_ref_window(self, e):
        self.edit_unite.value = e.control.data['unite']
        self.edit_nature.value = e.control.data["nature"]
        self.edit_id.value = e.control.data['id']
        self.edit_ref.value = e.control.data['reference']
        self.edit_des.value = e.control.data["designation"]

        for widget in (self.edit_id, self.edit_ref, self.edit_des, self.edit_nature, self.edit_unite):
            widget.update()

        self.edit_ref_window.scale = 1
        self.edit_ref_window.update()

    def close_edit_ref_window(self, e):
        self.edit_ref_window.scale = 0
        self.edit_ref_window.update()

    def add_new_article(self, e):
        count = 0
        for widget in (self.new_ref, self.new_des, self.new_unite, self.new_nature):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            all_datas = be.all_references()
            list_ref = [data["reference"] for data in all_datas]

            if self.new_ref.value in list_ref:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "La référence existe déja"
                self.cp.box.open = True
                self.cp.box.update()
            else:
                be.add_ref(self.new_ref.value, self.new_des.value, self.new_nature.value, self.new_unite.value)
                self.cp.box.title.value = "Validé"
                self.cp.box.content.value = "Nouvel article créé"
                self.cp.box.open = True
                self.cp.box.update()

                for widget in (self.new_ref, self.new_des, self.new_nature, self.new_unite):
                    widget.value = None
                    widget.update()

        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Tous les champs sont obligatoires"
            self.cp.box.open = True
            self.cp.box.update()

    def update_reference(self, e):
        if self.edit_des.value == "" or self.edit_des.value  is None:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Le champs désignation est obligatoire"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            be.update_ref_by_name(self.edit_des.value, int(self.edit_id.value))
            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = "Article mis à jour"
            self.cp.box.open = True
            self.cp.box.update()

    def show_historique(self, e):
        datas = be.all_historique_by_ref(e.control.data["reference"])
        self.histo_des.value = e.control.data["designation"]
        self.histo_qte.value = e.control.data["qte"]
        self.histo_prix.value = ajout_separateur(e.control.data["prix"])
        self.histo_unite.value = e.control.data["unite"].upper()
        self.histo_ref.value = e.control.data["reference"]

        for widget in (self.histo_ref, self.histo_des, self.histo_qte, self.histo_prix, self.histo_unite):
            widget.update()

        for row in self.histo_table.rows[:]:
            self.histo_table.rows.remove(row)

        for data in datas:
            if data["mouvement"] == "S":
                qte_mvt = 0 - data["qte_mvt"]
            else:
                qte_mvt = data["qte_mvt"]

            self.histo_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data['date'])),
                        ft.DataCell(ft.Text(data['mouvement'])),
                        ft.DataCell(ft.Text(data['num_mvt'])),
                        ft.DataCell(ft.Text(data['qte_avant'])),
                        ft.DataCell(ft.Text(f"{qte_mvt}")),
                        ft.DataCell(ft.Text(data['qte_apres'])),
                    ]
                )
            )

        self.histo_table.update()
        self.histo_window.scale = 1
        self.histo_window.update()

    def close_histo_window(self, e):
        self.histo_window.scale = 0
        self.histo_window.update()
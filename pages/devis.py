from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur, ecrire_en_lettres


class OneArticle(ft.Container):
    def __init__(self, cp: object, ref: str, des: str, prix: int):
        super().__init__(
            padding=ft.padding.only(10, 3, 10, 3),
        )
        self.cp = cp
        self.ref = ref
        self.des = des
        self.prix = ft.TextField(**numbers_field_style, value="", width=100, label="Prix")
        self.qte = ft.TextField(**numbers_field_style, value="", width=80, label="Qté")
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(**readonly_field_style, value=ref, width=170, label="Référence", tooltip=f"Prix: {ajout_separateur(prix)}"),
                        ft.TextField(**readonly_field_style, value=des, width=300, label="Nom pièce"),
                        self.qte, self.prix
                    ]
                ),
                CtButton("add", "Ajouter", None, self.add_article_to_list)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def add_article_to_list(self, e):
        count = 0
        for widget in (self.qte, self.prix):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            self.cp.table_selected.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.ref)),
                        ft.DataCell(ft.Text(self.des)),
                        ft.DataCell(ft.Text(f"{self.qte.value}")),
                        ft.DataCell(ft.Text(f"{self.prix.value}")),
                    ]
                )
            )
            self.cp.table_selected.update()
            for widget in (self.prix, self.qte):
                widget.value = None
                widget.update()


class AddOneArticle(ft.Container):
    def __init__(self, cp: object, ref: str, des: str, prix: int):
        super().__init__(
            padding=ft.padding.only(10, 3, 10, 3),
        )
        self.cp = cp
        self.ref = ref
        self.des = des
        self.prix = ft.TextField(**numbers_field_style, value="", width=100, label="Prix")
        self.qte = ft.TextField(**numbers_field_style, value="", width=80, label="Qté")
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(**readonly_field_style, value=ref, width=170, label="Référence", tooltip=f"Prix: {ajout_separateur(prix)}"),
                        ft.TextField(**readonly_field_style, value=des, width=300, label="Nom pièce"),
                        self.qte, self.prix
                    ]
                ),
                CtButton("add", "Ajouter", None, self.add_article_to_list)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def add_article_to_list(self, e):
        count = 0
        for widget in (self.qte, self.prix):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            self.cp.edit_table.controls.append(
                EditOneArticle(self.cp, self.ref, self.des, int(self.qte.value), int(self.prix.value))
            )
            self.cp.edit_table.update()
            self.cp.cp.box.title.value = "Validé"
            self.cp.cp.box.content.value = "Article ajouté"
            self.cp.cp.box.open=True
            self.cp.cp.box.update()

            somme = 0
            nb_ref = 0
            for widget in self.cp.edit_table.controls[:]:
                somme += (int(widget.art_prix.value) * int(widget.art_qte.value))
                nb_ref += 1

            self.cp.edit_montant.value = somme
            total = int(somme - (somme * int(self.cp.edit_remise.value) / 100))
            self.cp.edit_lettres.value = ecrire_en_lettres(total)
            self.cp.edit_nb_ref.value = f"{nb_ref} article(s)"

            for widget in (self.cp.edit_nb_ref, self.cp.edit_montant, self.cp.edit_lettres):
                widget.update()

            for widget in (self.prix, self.qte):
                widget.value = None
                widget.update()

        else:
            self.cp.cp.box.title.value = "Erreur"
            self.cp.cp.box.content.value = "Qté et prix sont obligatoires"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()


class EditOneArticle(ft.Container):
    def __init__(self, cp: object, ref: str, des: str, qte: int, prix: int):
        super().__init__(
            padding=ft.padding.only(10, 3, 10, 3),
        )
        self.cp = cp
        self.ref = ref
        self.des = des
        self.prix = prix
        self.qte = qte
        self.status = False
        self.art_ref = ft.TextField(**readonly_field_style, value=ref, width=140, label="Référence",)
        self.art_des = ft.TextField(**readonly_field_style, value=des, width=300, label="Nom pièce", tooltip=f"{des}")
        self.art_qte = ft.TextField(**numbers_field_style, value=f"{qte}", width=80, label="Qté", disabled=True)
        self.art_prix = ft.TextField(**numbers_field_style, value=f"{prix}", width=100, label="Qté", disabled=True)
        self.bt_modif = CtButton(ft.icons.CHECK, "Modifier", None, self.edit_article)
        self.bt_modif.visible = False
        self.bt_allow_modif = CtButton("edit_outlined", "Modifier", None, self.allow_edit)
        self.bt_allow_modif.visible = True
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[self.art_ref, self.art_des, self.art_qte, self.art_prix]
                ),
               ft.Row(
                   controls=[
                       self.bt_modif, self.bt_allow_modif,
                       CtButton("delete_outlined", "Modifier", None, self.delete_article)
                   ], spacing=0
               )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def allow_edit(self, e):
        # if not self.status == "edit_outlined":
        self.bt_modif.visible = True
        self.bt_modif.update()
        e.control.visible = False
        e.control.update()
        self.status = True
        for widget in (self.art_qte, self.art_prix):
            widget.disabled = False
            widget.update()

    def edit_article(self, e):
        e.control.visible = False
        e.control.update()
        self.bt_allow_modif.visible = True
        self.bt_allow_modif.update()
        self.status = False
        for widget in (self.art_qte, self.art_prix):
            widget.disabled = True
            widget.update()

        somme = 0
        nb_ref = 0

        if len(self.cp.edit_table.controls[:]) == 0:
            self.cp.edit_montant.value = "0"
            self.cp.edit_lettres.value = ecrire_en_lettres(0)
            self.cp.edit_nb_ref.value = f"Aucune ligne(s)"

        else:
            for widget in self.cp.edit_table.controls[:]:
                somme += (int(widget.art_prix.value) * int(widget.art_qte.value))
                nb_ref += 1

            self.cp.edit_montant.value = f"{somme}"
            total = int(somme - (somme * int(self.cp.edit_remise.value) / 100))
            self.cp.edit_lettres.value = ecrire_en_lettres(total)
            self.cp.edit_nb_ref.value = f"{nb_ref} ligne(s)"

        for widget in (self.cp.edit_nb_ref, self.cp.edit_montant, self.cp.edit_lettres):
            widget.update()

        self.cp.edit_table.update()

    def delete_article(self, e):
        self.cp.edit_table.controls.remove(self)
        somme = 0
        nb_ref = 0

        if len(self.cp.edit_table.controls[:]) == 0:
            self.cp.edit_montant.value = "0"
            self.cp.edit_lettres.value = ecrire_en_lettres(0)
            self.cp.edit_nb_ref.value = f"Aucune ligne(s)"

        else:
            for widget in self.cp.edit_table.controls[:]:
                somme += (int(widget.art_prix.value) * int(widget.art_qte.value))
                nb_ref += 1

            self.cp.edit_montant.value = f"{somme}"
            total = int(somme - (somme * int(self.cp.edit_remise.value) / 100))
            self.cp.edit_lettres.value = ecrire_en_lettres(total)
            self.cp.edit_nb_ref.value = f"{nb_ref} ligne(s)"

        for widget in (self.cp.edit_nb_ref, self.cp.edit_montant, self.cp.edit_lettres):
            widget.update()

        self.cp.edit_table.update()


class Devis(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp
        self.nb_devis = ft.Text("", size=18, font_family="Poppins Medium")
        self.nb_devis_expires = ft.Text("", size=18, font_family="Poppins Medium")
        self.nb_devis_encours = ft.Text("", size=18, font_family="Poppins Medium")
        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
        self.table = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("Date".upper())),
                ft.DataColumn(ft.Text("numero".upper())),
                ft.DataColumn(ft.Text("client".upper())),
                ft.DataColumn(ft.Text("Montant".upper())),
                ft.DataColumn(ft.Text("statut")),
                ft.DataColumn(ft.Text("")),
            ]
        )
        self.main_window = ft.Container(
            expand=True,
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="#f2f2f2",
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Chiffres".upper(), size=13, font_family="Poppins Medium"),
                            ft.Divider(height=1, thickness=1),
                        ], spacing=0
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Nombre de devis", size=12, font_family="Poppins-Medium", italic=True),
                                    self.nb_devis
                                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Devis expirés", size=12, font_family="Poppins-Medium", italic=True),
                                    self.nb_devis_expires
                                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Devis en cours", size=12, font_family="Poppins-Medium", italic=True),
                                    self.nb_devis_encours
                                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ], spacing=50
                    ),
                    ft.Container(
                        padding=10, border_radius=10, bgcolor="white", expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
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

                ]
            )
        )

        # New devis window ...
        self.new_devis_num = ft.Text("", size=12, font_family="Poppins Medium")
        self.new_objet = ft.TextField(
            **field_style, width=300, label="Objet du devis",
        )
        self.new_client = ft.Dropdown(**drop_style, label="Client", width=400, prefix_icon=ft.icons.PERSON_SEARCH_OUTLINED)
        self.new_nb_ref = ft.Text("", size=12, font_family="Poppins Medium", italic=True, color="grey")
        self.new_table = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.new_num = ft.Text("", size=12, font_family="Poppins Medium", color="white", )
        self.new_montant = ft.TextField(**readonly_field_style, width=140, prefix_icon=ft.icons.PRICE_CHANGE_OUTLINED,
                                         label="Montant")
        self.new_lettres = ft.TextField(**readonly_field_style, width=700, prefix_icon=ft.icons.LABEL_OUTLINED,
                                         label="Montant en lettres")
        self.new_objet = ft.TextField(**field_style, width=700, label="Objet du devis",
                                       prefix_icon=ft.icons.MAIL_OUTLINED)
        self.new_notabene = ft.TextField(**field_style, width=700, label="NB", prefix_icon=ft.icons.NOTES_OUTLINED)
        self.new_paiement = ft.TextField(**numbers_field_style, width=110, label="Paiement",
                                          prefix_icon=ft.icons.WATCH_LATER_OUTLINED)
        self.new_validite = ft.TextField(**numbers_field_style, width=120, label="validité",
                                          prefix_icon=ft.icons.EVENT_AVAILABLE)
        self.new_point_liv = ft.TextField(**field_style, width=200, label="pt. livraison",
                                           prefix_icon=ft.icons.LOCATION_ON_OUTLINED)
        self.new_delai = ft.TextField(**field_style, width=150, label="Délai livraison",
                                       prefix_icon=ft.icons.TIMELAPSE_OUTLINED)
        self.new_remise = ft.TextField(**numbers_field_style, width=110, label="remise",
                                        prefix_icon=ft.icons.KEYBOARD_DOUBLE_ARROW_DOWN)
        self.bt_create_dev = AnyButton(FIRST_COLOR, "check", "Créer devis", "white", 180, None)
        self.new_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=900, height=650,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    expand=True, scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(
                            bgcolor="white", padding=ft.padding.only(10, 5, 10, 5), border_radius=16,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.NOTE_ADD_OUTLINED, "black"),
                                            ft.Text("Créer devis".upper(), size=14,
                                                    font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2", on_click=self.close_new_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            bgcolor="white", padding=20, border_radius=16, expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            self.new_client,
                                                            ft.Text("Devis N°".upper(), size=12, font_family="Poppins Medium"),
                                                            ft.Container(
                                                                padding=ft.padding.only(10, 3, 10, 3), border_radius=10,
                                                                bgcolor=ft.colors.DEEP_ORANGE, content=ft.Row(
                                                                    controls=[self.new_num],
                                                                    alignment=ft.MainAxisAlignment.CENTER
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            self.new_nb_ref
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Stack(
                                        controls=[
                                            ft.Container(
                                                height=240, padding=ft.padding.only(10, 3, 10, 3),
                                                border_radius=16,
                                                expand=True,
                                                border=ft.border.all(1, "grey"), content=self.new_table
                                            ),
                                            ft.FloatingActionButton(
                                                bgcolor="black", on_click=self.open_new_add_ref_window,
                                                content=ft.Row([ft.Icon(ft.icons.ADD, color="white")],
                                                               alignment=ft.MainAxisAlignment.CENTER),
                                                bottom=10, scale=0.8, right=10, tooltip="Ajouter référence",
                                                opacity=0.95
                                            )
                                        ], alignment=ft.alignment.bottom_right
                                    ),
                                    ft.Row([self.new_objet]),
                                    ft.Row([self.new_paiement, self.new_delai, self.new_point_liv,
                                            self.new_validite, self.new_remise]),
                                    self.new_notabene,
                                    ft.Row([self.new_montant, self.new_lettres]),
                                    self.bt_create_dev
                                ]
                            )
                        )
                    ]
                )
            )
        )
        # Ajouter new reference window ...
        self.new_add_select_article = ft.TextField(**search_field_style, width=300, on_change=self.filter_selection_new,
                                               prefix_icon="search")
        self.new_table_add_ref = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.new_add_ref_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=800, height=550,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Container(
                    expand=True, padding=10, border_radius=16, bgcolor="white",
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Ajouter article".upper(), size=14, font_family="Poppins Medium"),
                                    ft.Divider(height=1, thickness=1),
                                ], spacing=0
                            ),
                            self.new_add_select_article,
                            ft.Container(
                                border_radius=12, border=ft.border.all(1, "grey"), expand=True,
                                padding=ft.padding.only(10, 5, 10, 5),
                                content=self.new_table_add_ref
                            ),
                            ft.Row(
                                [AnyButton(FIRST_COLOR, "close", "Fermer", "white", 170, self.close_new_add_ref_window)],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ]
                    )
                )
            )
        )

        # Edit window ...
        self.edit_bt_facture = ft.Container(padding=ft.padding.only(10, 3, 10, 3), border_radius=10)
        self.edit_nb_ref = ft.Text("", size=12, font_family="Poppins Medium", italic=True, color="grey")
        self.edit_table = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.edit_num = ft.Text("", size=12, font_family="Poppins Medium", color="white",)
        self.edit_montant = ft.TextField(**readonly_field_style, width=140, prefix_icon=ft.icons.PRICE_CHANGE_OUTLINED, label="Montant")
        self.edit_lettres = ft.TextField(**readonly_field_style, width=700, prefix_icon=ft.icons.LABEL_OUTLINED, label="Montant en lettres")
        self.edit_objet = ft.TextField(**field_style, width=700, label="Objet du devis", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_notabene = ft.TextField(**field_style, width=700, label="NB", prefix_icon=ft.icons.NOTES_OUTLINED)
        self.edit_paiement = ft.TextField(**numbers_field_style, width=110, label="Paiement", prefix_icon=ft.icons.WATCH_LATER_OUTLINED)
        self.edit_validite = ft.TextField(**numbers_field_style, width=120, label="validité", prefix_icon=ft.icons.EVENT_AVAILABLE)
        self.edit_point_liv = ft.TextField(**field_style, width=200, label="pt. livraison", prefix_icon=ft.icons.LOCATION_ON_OUTLINED)
        self.edit_delai = ft.TextField(**field_style, width=150, label="Délai livraison", prefix_icon=ft.icons.TIMELAPSE_OUTLINED)
        self.edit_remise = ft.TextField(**numbers_field_style, width=110, label="remise", prefix_icon=ft.icons.KEYBOARD_DOUBLE_ARROW_DOWN)
        self.bt_valid_modif = AnyButton(FIRST_COLOR, "check", "Valider Modifications", "white", 230, None)
        self.edit_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=900, height=650,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            bgcolor="white", padding=ft.padding.only(10, 5, 10, 5), border_radius=16,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.EDIT_OUTLINED, "black"),
                                            ft.Text("Modifier devis".upper(), size=14,
                                                    font_family="Poppins Medium")
                                        ]
                                    ),
                                    ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                                  on_click=self.close_edit_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            bgcolor="white", padding=20, border_radius=16, expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text("Devis N°".upper(), size=12,
                                                                    font_family="Poppins Medium"),
                                                            ft.Container(
                                                                padding=ft.padding.only(10, 3, 10, 3), border_radius=10,
                                                                bgcolor=SECOND_COLOR, content=ft.Row(
                                                                    controls=[self.edit_num,], alignment=ft.MainAxisAlignment.CENTER
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                    self.edit_bt_facture
                                                ]
                                            ),
                                            self.edit_nb_ref
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Stack(
                                        controls=[
                                            ft.Container(
                                                height=240, padding=ft.padding.only(10, 3, 10, 3),
                                                border_radius=16,
                                                expand=True,
                                                border=ft.border.all(1, "grey"), content=self.edit_table
                                            ),
                                            ft.FloatingActionButton(
                                                bgcolor="black", on_click=self.open_add_ref_window,
                                                content=ft.Row([ft.Icon(ft.icons.ADD, color="white")],
                                                               alignment=ft.MainAxisAlignment.CENTER),
                                                bottom=10, scale=0.8, right=10, tooltip="Ajouter référence", opacity=0.95
                                            )
                                        ], alignment=ft.alignment.bottom_right
                                    ),
                                    self.edit_objet,
                                    ft.Row([self.edit_paiement, self.edit_delai, self.edit_point_liv,
                                            self.edit_validite, self.edit_remise]),
                                    self.edit_notabene,
                                    ft.Row([self.edit_montant, self.edit_lettres]),
                                    self.bt_valid_modif
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # Ajouter reference window ...
        self.add_select_article = ft.TextField(**search_field_style, width=300, on_change=self.filter_selection, prefix_icon="search")
        self.table_edit_ref = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.edit_ref_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=800, height=550,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6", expand=True,
                content=ft.Container(
                    expand=True, padding=10, border_radius=16, bgcolor="white",
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Ajouter article".upper(), size=14, font_family="Poppins Medium"),
                                    ft.Divider(height=1, thickness=1),
                                ], spacing=0
                            ),
                            self.add_select_article,
                            ft.Container(
                                border_radius=12, border=ft.border.all(1, "grey"), expand=True,
                                padding=ft.padding.only(10, 5, 10, 5),
                                content=self.table_edit_ref
                            ),
                            ft.Row(
                                [AnyButton(FIRST_COLOR, "close", "Fermer", "white", 170, self.close_add_ref_window)],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ]
                    )
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.new_window, self.new_add_ref_window, self.edit_window, self.edit_ref_window,
            ], alignment=ft.alignment.center
        )
        self.load_datas()
        self.load_lists()

    def load_lists(self):
        datas = be.all_references()

        for widget in self.new_table_add_ref.controls[:]:
            self.new_table_add_ref.controls.remove(widget)

        for data in datas:
            self.new_table_add_ref.controls.append(
                OneArticle(self, data["reference"], data["designation"], data["prix"])
            )

        for widget in self.new_table_add_ref.controls[:]:
            self.new_table_add_ref.controls.remove(widget)

        for data in datas:
            self.table_edit_ref.controls.append(
                AddOneArticle(self, data["reference"], data["designation"], data["prix"])
            )

    def load_datas(self):
        datas = be.all_devis()
        self.results.value = f"{len(datas)} Résultat(s)"
        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in datas:
            if data["statut"].lower() != "non facturé":
                icone = ft.icons.CHECK_CIRCLE
                couleur = "green"
            else:
                icone = None
                couleur = None

            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["date"])),
                        ft.DataCell(ft.Text(data["numero"])),
                        ft.DataCell(ft.Text(data["client"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["montant"]))),
                        ft.DataCell(ft.Icon(icone, couleur, 16)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    CtButton("edit_outlined", "Modifier", data, self.open_edit_window),
                                    CtButton(ft.icons.ADD_BUSINESS_OUTLINED, "Facturer", data, None)
                                ], alignment=ft.MainAxisAlignment.END, spacing=2,
                            )
                        )
                    ]
                )
            )
        datas = be.all_references()
        # for widget in self.table_articles.controls[:]:
        #     self.table_articles.controls.remove(widget)
        #
        # for data in datas:
        #     self.table_articles.controls.append(
        #         OneArticle(self, data["reference"], data["designation"], data["prix"])
        #     )

    def filter_datas(self, e):
        datas = be.all_devis()
        search = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: search in x['client'] or search in x["numero"], datas))

        self.results.value = f"{len(filtered_datas)} Résultat(s)"
        self.results.update()

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in filtered_datas:
            if data["statut"].lower() != "non facturé":
                icone = ft.icons.CHECK_CIRCLE
                couleur = "green"
            else:
                icone = None
                couleur = None

            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["date"])),
                        ft.DataCell(ft.Text(data["numero"])),
                        ft.DataCell(ft.Text(data["client"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["montant"]))),
                        ft.DataCell(ft.Icon(icone, couleur, 18)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    CtButton("edit_outlined", "Modifier", data, self.open_edit_window),
                                    CtButton(ft.icons.ADD_BUSINESS_OUTLINED, "Facturer", data, None)
                                ], alignment=ft.MainAxisAlignment.END, spacing=2,
                            )
                        )
                    ]
                )
            )

        self.table.update()

    def filter_selection(self, e):
        selected = self.add_select_article.value if self.add_select_article.value is not None else ""
        datas = be.all_references()

        for widget in self.table_edit_ref.controls[:]:
            self.table_edit_ref.controls.remove(widget)

        filtered_datas = list(filter(lambda x: selected in x['designation'], datas))

        for data in filtered_datas:
            self.table_edit_ref.controls.append(
                OneArticle(self, data["reference"], data["designation"], data["prix"])
            )
        self.table_edit_ref.update()

    def filter_selection_new(self, e):
        selected = self.new_add_select_article.value if self.new_add_select_article.value is not None else ""
        datas = be.all_references()

        for widget in self.new_table_add_ref.controls[:]:
            self.new_table_add_ref.controls.remove(widget)

        filtered_datas = list(filter(lambda x: selected in x['designation'], datas))

        for data in filtered_datas:
            self.new_table_add_ref.controls.append(
                OneArticle(self, data["reference"], data["designation"], data["prix"])
            )
        self.new_table_add_ref.update()


    def open_new_window(self, e):
        self.new_window.scale = 1
        self.new_window.update()

    def open_edit_window(self, e):
        datas = be.select_one_devis(e.control.data["numero"])
        self.edit_objet.value = f"{datas["objet"]}"
        self.edit_notabene.value = f"{datas["note_bene"]}"
        self.edit_paiement.value = f"{datas["paiement"]}"
        self.edit_validite.value = f"{datas["validite"]}"
        self.edit_point_liv.value = f"{datas["point_liv"]}"
        self.edit_delai.value = f"{datas["delai"]}"
        self.edit_remise.value = f"{datas["remise"]}"
        self.edit_montant.value = f"{datas["montant"]}"
        self.edit_num.value = f"{datas["numero"]}"
        self.edit_lettres.value = ecrire_en_lettres(int(datas["montant"]))

        for widget in (
            self.edit_objet, self.edit_delai, self.edit_validite, self.edit_remise, self.edit_montant,
            self.edit_paiement, self.edit_point_liv, self.edit_notabene, self.edit_num, self.edit_lettres,
        ):
            widget.update()

        details = be.find_devis_details(e.control.data["numero"])
        self.edit_nb_ref.value = f"{len(details)} ligne(s)"
        self.edit_nb_ref.update()

        for widget in self.edit_table.controls[:]:
            self.edit_table.controls.remove(widget)

        for detail in details:
            designation = be.search_designation(detail["reference"])
            self.edit_table.controls.append(
                EditOneArticle(self, detail["reference"], designation, detail["qte"], detail["prix"])
            )

        if e.control.data["statut"].lower() == "facturé":
            self.edit_bt_facture.content = ft.Row(
                controls=[
                    ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED, color="white", size=16),
                    ft.Text("facturé".upper(), size=12, font_family="Poppins Medium", color="white",)
                ], spacing=5
            )
            self.edit_bt_facture.bgcolor = ft.colors.LIGHT_GREEN
            self.edit_bt_facture.update()
            self.bt_valid_modif.visible = False
            self.bt_valid_modif.update()

        else:
            self.edit_bt_facture.content = ft.Row(
                controls=[
                    ft.Icon(ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED, color="white", size=16),
                    ft.Text("non facturé".upper(), size=12, font_family="Poppins Medium", color="white",)
                ], spacing=5
            )
            self.edit_bt_facture.bgcolor = "red"
            self.edit_bt_facture.update()
            self.bt_valid_modif.visible = True
            self.bt_valid_modif.update()

        self.edit_table.update()
        self.edit_window.scale = 1
        self.edit_window.update()

    def close_new_window(self, e):
        self.new_window.scale = 0
        self.new_window.update()

    def close_edit_window(self, e):
        self.edit_window.scale = 0
        self.edit_window.update()

    def close_add_ref_window(self, e):
        self.edit_ref_window.scale = 0
        self.edit_ref_window.update()

    def open_add_ref_window(self, e):
        self.edit_ref_window.scale = 1
        self.edit_ref_window.update()

    def close_new_add_ref_window(self, e):
        self.new_add_ref_window.scale = 0
        self.new_add_ref_window.update()

    def open_new_add_ref_window(self, e):
        self.new_add_ref_window.scale = 1
        self.new_add_ref_window.update()

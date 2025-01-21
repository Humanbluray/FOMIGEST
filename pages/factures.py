from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur, ecrire_en_lettres


class OneArticle(ft.Container):
    def __init__(self, cp: object, ref: str, des: str, qte: int, prix: int):
        super().__init__(
            padding=ft.padding.only(10, 3, 10, 3),
        )
        self.cp = cp
        self.ref = ref
        self.des = des
        self.prix = prix
        self.qte = qte

        self.art_ref = ft.TextField(**readonly_field_style, value=ref, width=140, label="Référence",)
        self.art_des = ft.TextField(**readonly_field_style, value=des, width=300, label="Nom pièce", tooltip=f"{des}")
        self.art_qte = ft.TextField(**readonly_field_style, value=f"{qte}", width=80, label="Qté")
        self.art_prix = ft.TextField(**readonly_field_style, value=f"{ajout_separateur(prix)}", width=100, label="Prix")

        self.content = ft.Row(
            controls=[self.art_ref, self.art_des, self.art_qte, self.art_prix],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )


class Factures(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
        self.cp = cp
        self.search = ft.TextField(**search_field_style, width=300, prefix_icon="search", on_change=self.filter_datas)
        self.results = ft.Text("", size=12, font_family="Poppins Medium")
        self.table = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("numero".upper())),
                ft.DataColumn(ft.Text("devis".upper())),
                ft.DataColumn(ft.Text("Montant".upper())),
                ft.DataColumn(ft.Text("Mt. payé".upper())),
                ft.DataColumn(ft.Text("reste".upper())),
                ft.DataColumn(ft.Text("")),
            ]
        )
        self.main_window = ft.Container(
            expand=True,
            padding=ft.padding.only(20, 15, 20, 15), border_radius=10, bgcolor="white",
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Liste des factures".upper(), size=16, font_family="Poppins Bold"),
                            ft.Divider(height=1, thickness=1),
                        ], spacing=0
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.search, self.results
                                ]
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.ListView(expand=True, controls=[self.table])
                ]
            )
        )
        self.pay_facture = ft.Text("", size=12, font_family="Poppins Medium", color="white")
        self.pay_montant = ft.TextField(**readonly_date_style, width=170, label="Total facture", prefix_icon=ft.icons.ATTACH_MONEY_OUTLINED)
        self.pay_deja_paye = ft.TextField(**readonly_date_style, width=170, label="Déja payé", prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED)
        self.pay_solde = ft.Checkbox(
            check_color=SECOND_COLOR, fill_color="#f0f0f6", label="Solde la facture",
            label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
            on_change=self.changement_solde
        )
        self.pay_mode = ft.Dropdown(
            **drop_style, width=200, label="Mode de paiement", prefix_icon=ft.icons.CREDIT_CARD_OUTLINED,
            options=[
                ft.dropdown.Option("virement".upper()),
                ft.dropdown.Option("espèces".upper()),
                ft.dropdown.Option("Orange Money".upper()),
                ft.dropdown.Option("MTN Mobile Money".upper()),
            ]
        )
        self.cp.dp_paiement.on_change = self.changement_date
        self.bt_select_date = ft.IconButton(
            ft.icons.CALENDAR_MONTH_OUTLINED, icon_color="black", scale=0.65,
            on_click=lambda _: self.cp.dp_paiement.pick_date()
        )
        self.pay_selected_date = ft.TextField(**readonly_date_style, label="Date", width=200, prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED)
        self.pay_button = AnyButton(
            FIRST_COLOR, "check", "Valider paiement", "white", 185,
            self.create_paiement
        )
        self.pay_a_regler = ft.TextField(**numbers_field_style, width=180, label="Montant règlement", prefix_icon=ft.icons.ATTACH_MONEY_OUTLINED)
        self.new_paiement_window = ft.Container(
            bgcolor="#f0f0f6", width=300, height=530,border_radius=16,
            padding=10, expand=True,
            shadow=ft.BoxShadow(spread_radius=5, blur_radius=15, color=ft.colors.BLACK38),
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        bgcolor="white", padding=ft.padding.only(10, 5, 10, 5), border_radius=16,
                        content=ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.icons.NOTE_ADD_OUTLINED, "black"),
                                        ft.Text("Nouveau paiement".upper(), size=14,
                                                font_family="Poppins Medium")
                                    ]
                                ),
                                ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                              on_click=self.close_new_paiement)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ),
                    ft.Container(
                        bgcolor="white", padding=20, border_radius=16, expand=True,
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    padding=ft.padding.only(10, 3, 10, 3), border_radius=10, bgcolor=SECOND_COLOR,
                                    content=ft.Row([self.pay_facture], alignment=ft.MainAxisAlignment.CENTER)
                                ),
                                self.pay_montant, self.pay_deja_paye, self.pay_solde,
                                self.pay_a_regler, self.pay_mode,
                                ft.Stack(
                                    controls=[self.pay_selected_date, self.bt_select_date],
                                    alignment=ft.alignment.center_right
                                ),
                                self.pay_button
                            ], spacing=15
                        )
                    )
                ]
            )
        )

        # Edit window ...
        self.edit_bt_facture = ft.Container(padding=ft.padding.only(10, 3, 10, 3), border_radius=10)
        self.edit_nb_ref = ft.Text("", size=12, font_family="Poppins Medium", italic=True, color="grey")
        self.edit_table = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.edit_num = ft.Text("", size=12, font_family="Poppins Medium", color="white")
        self.edit_dev = ft.Text("", size=12, font_family="Poppins Medium", color="white")
        self.edit_statut = ft.Text("", size=12, font_family="Poppins Medium", color="white")
        self.edit_icon_statut = ft.Icon(color="white", size=16)
        self.edit_montant = ft.TextField(**readonly_date_style, width=170, prefix_icon=ft.icons.PRICE_CHANGE_OUTLINED, label="Montant")
        self.edit_lettres = ft.TextField(**readonly_field_style, width=700, prefix_icon=ft.icons.LABEL_OUTLINED, label="Montant en lettres")
        self.edit_objet = ft.TextField(**readonly_date_style, width=700, label="Objet", prefix_icon=ft.icons.MAIL_OUTLINED)
        self.edit_bc = ft.TextField(**readonly_date_style, width=200, label="BC client", prefix_icon=ft.icons.NOTES_OUTLINED)
        self.edit_ov = ft.TextField(**readonly_date_style, width=200, label="OV", prefix_icon=ft.icons.NOTES)
        self.edit_delai = ft.TextField(**readonly_date_style, width=150, label="Délai livraison", prefix_icon=ft.icons.TIMELAPSE_OUTLINED)
        self.edit_remise = ft.TextField(**readonly_date_style, width=100, label="remise", value="0", prefix_icon=ft.icons.KEYBOARD_ARROW_DOWN_OUTLINED)
        self.ct_statut = ft.Container(
            padding=ft.padding.only(10, 3, 10, 3), border_radius=10,
            content=ft.Row(
                controls=[
                    self.edit_icon_statut,
                    self.edit_statut
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.bt_print_options = AnyButton(FIRST_COLOR, "print_outlined", "Imprimer facture", "white", 230, self.open_impression_window)
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
                                            ft.Text("Détails facture".upper(), size=14,
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
                                                            ft.Text("Facture N°".upper(), size=12, font_family="Poppins Medium"),
                                                            ft.Container(
                                                                padding=ft.padding.only(10, 3, 10, 3), border_radius=10,
                                                                bgcolor=SECOND_COLOR, content=ft.Row(
                                                                    controls=[self.edit_num, ],
                                                                    alignment=ft.MainAxisAlignment.CENTER
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text("Devis N°".upper(), size=12,
                                                                    font_family="Poppins Medium"),
                                                            ft.Container(
                                                                padding=ft.padding.only(10, 3, 10, 3), border_radius=10,
                                                                bgcolor=ft.colors.DEEP_ORANGE, content=ft.Row(
                                                                    controls=[self.edit_dev],
                                                                    alignment=ft.MainAxisAlignment.CENTER
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text("Statut".upper(), size=12,font_family="Poppins Medium"),
                                                            self.ct_statut
                                                        ]
                                                    ),
                                                    self.edit_bt_facture
                                                ]
                                            ),
                                            self.edit_nb_ref
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Container(
                                        height=240, padding=ft.padding.only(10, 3, 10, 3),
                                        border_radius=16,
                                        expand=True,
                                        border=ft.border.all(1, "grey"), content=self.edit_table
                                    ),
                                    self.edit_objet,
                                    ft.Row(
                                        controls=[
                                            self.edit_ov, self.edit_delai, self.edit_remise, self.edit_bc,
                                        ]
                                    ),

                                    ft.Row([self.edit_montant, self.edit_lettres]),
                                    ft.Row([self.bt_print_options], spacing=20)
                                ]
                            )
                        )
                    ]
                )
            )
        )

        # Paiements window
        self.vp_numero = ft.Text(size=12, font_family="Poppins Medium", color="white")
        self.vp_statut = ft.Text(size=12, font_family="Poppins Medium", color="white")
        self.vp_table = ft.DataTable(
            **datatable_style,
            columns=[
                ft.DataColumn(ft.Text("date".upper())),
                ft.DataColumn(ft.Text("type".upper())),
                ft.DataColumn(ft.Text("montant".upper())),
            ]
        )
        self.vp_icone_statut = ft.Icon(size=16, color="white")
        self.vp_ct_statut =  ft.Container(
            border_radius=10,
            padding=ft.padding.only(10, 3, 10, 3),
            content=ft.Row(
                [
                    self.vp_icone_statut,
                    self.vp_statut
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        self.paiements_window = ft.Container(
            bgcolor="#f0f0f6", width=600, height=400,border_radius=16,
            padding=10, expand=True,
            shadow=ft.BoxShadow(spread_radius=5, blur_radius=15, color=ft.colors.BLACK38),
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        bgcolor="white", padding=ft.padding.only(10, 5, 10, 5), border_radius=16,
                        content=ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.icons.NOTE_ADD_OUTLINED, "black"),
                                        ft.Text("Paiements".upper(), size=14,
                                                font_family="Poppins Medium")
                                    ]
                                ),
                                ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                              on_click=self.close_paiements_window)
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
                                                ft.Text("Numéro de facture:".upper(), size=12,
                                                        font_family="Poppins Medium"),
                                                ft.Container(
                                                    bgcolor=SECOND_COLOR, border_radius=10,
                                                    padding=ft.padding.only(10, 3, 10, 3),
                                                    content=ft.Row([self.vp_numero],
                                                                   alignment=ft.MainAxisAlignment.CENTER)
                                                )
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Text("Statut:".upper(), size=12,
                                                        font_family="Poppins Medium"),
                                                self.vp_ct_statut
                                            ]
                                        ),
                                    ]
                                ),
                                ft.Container(
                                    padding=ft.padding.only(10, 5, 10, 5), border_radius=10,
                                    border=ft.border.all(1, "grey"), expand=True,
                                    content=ft.ListView(expand=True, controls=[self.vp_table])
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # options d'impression window
        self.regime = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(
                        **radio_style, value="S", label="Simplifié".upper()
                    ),
                    ft.Radio(
                        **radio_style, value="R", label="Réel".upper()
                    )
                ]
            )
        )
        self.tva = ft.Checkbox(
            label_style=ft.TextStyle(size=12, font_family="Poppins Medium"), active_color="white",
            check_color=FIRST_COLOR,
            label="TVA", label_position=ft.LabelPosition.RIGHT
        )
        self.ir = ft.Checkbox(
            label_style=ft.TextStyle(size=12, font_family="Poppins Medium"), active_color="white",
            check_color=FIRST_COLOR,
            label="IR", label_position=ft.LabelPosition.RIGHT
        )
        self.impression_window = ft.Card(
            elevation=20, surface_tint_color="#f0f0f6", width=350, height=320,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            content=ft.Container(
                padding=10, bgcolor="#f0f0f6",
                content=ft.Container(
                    padding=10, border_radius=16, bgcolor="white",
                    content=ft.Column(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Options d'impressions".upper(), size=14,
                                                    font_family="Poppins Medium"),
                                            ft.IconButton("close", FIRST_COLOR, scale=0.6, bgcolor="#f2f2f2",
                                                          on_click=self.close_impression_window)
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Divider(height=1, thickness=1),
                                ], spacing=0
                            ),
                            ft.Divider(height=3, color=ft.colors.TRANSPARENT),
                            ft.Column(
                                controls=[
                                    ft.Text("choix du régime".upper(), size=11, font_family="Poppins Bold"),
                                    ft.Divider(height=1, thickness=1),
                                ], spacing=0
                            ),
                            self.regime,
                            ft.Divider(height=3, color=ft.colors.TRANSPARENT),
                            ft.Column(
                                controls=[
                                    ft.Text("TVA et IR".upper(), size=11, font_family="Poppins Bold"),
                                    ft.Divider(height=1, thickness=1),
                                ], spacing=0
                            ),
                            ft.Row([self.tva, self.ir]),
                            ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                            AnyButton(FIRST_COLOR, ft.icons.LOCAL_PRINTSHOP_OUTLINED, "Imprimer", "white", 280, None)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.new_paiement_window, self.edit_window, self.impression_window, self.paiements_window
            ], alignment=ft.alignment.center
        )
        self.load_datas()

    def load_datas(self):
        datas = be.all_factures()
        self.results.value = f"{len(datas)} résultat(s)"

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in datas:
            if data["mt_remise"] > data["regle"]:
                statut = "en cours"
                icone = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
                couleur = "red"
                pay_bt = CtButton(ft.icons.ADD_CARD_OUTLINED, "Paiement", data, self.open_new_paiement)
            else:
                statut = "soldée"
                icone = ft.icons.CHECK
                couleur = "green"
                pay_bt = CtButton(None, "", data, None)

            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Icon(icone, couleur, 18)),
                        ft.DataCell(ft.Text(data["numero"])),
                        ft.DataCell(ft.Text(data["devis"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["mt_remise"]))),
                        ft.DataCell(ft.Text(ajout_separateur(data["regle"]))),
                        ft.DataCell(ft.Text(f"{ajout_separateur(data['mt_remise'] - data['regle'])}")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    CtButton(ft.icons.EDIT_OUTLINED, "Voir details", data, self.open_edit_window),
                                    pay_bt,
                                    CtButton(ft.icons.LIST, "paiements", data, self.voir_paiements)
                                ], spacing=0, alignment=ft.MainAxisAlignment.END
                            )
                        ),
                    ]
                )
            )

    def filter_datas(self, e):
        datas = be.all_factures()
        search = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: search in x["numero"] or search in x["devis"] or search in x["nom_client"], datas))

        self.results.value = f"{len(filtered_datas)} résultat(s)"
        self.results.update()

        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        for data in filtered_datas:
            if data["mt_remise"] > data["regle"]:
                statut = "en cours"
                icone = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
                couleur = "red"
                pay_bt = CtButton(ft.icons.ADD_CARD_OUTLINED, "Paiement", data, self.open_new_paiement)
            else:
                statut = "soldée"
                icone = ft.icons.CHECK
                couleur = "green"
                pay_bt = CtButton(None, "", data, None)

            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Icon(icone, couleur, 18)),
                        ft.DataCell(ft.Text(data["numero"])),
                        ft.DataCell(ft.Text(data["devis"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["mt_remise"]))),
                        ft.DataCell(ft.Text(ajout_separateur(data["regle"]))),
                        ft.DataCell(ft.Text(f"{ajout_separateur(data['mt_remise'] - data['regle'])}")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    CtButton(ft.icons.EDIT_OUTLINED, "Voir details", data, self.open_edit_window),
                                    pay_bt,
                                    CtButton(ft.icons.LIST, "paiements", data, self.voir_paiements)
                                ], spacing=0, alignment=ft.MainAxisAlignment.END
                            )
                        ),
                    ]
                )
            )

        self.table.update()

    def open_new_paiement(self, e):
        self.pay_facture.value = e.control.data["numero"]
        self.pay_facture.update()
        self.pay_deja_paye.value = f"{e.control.data['regle']}"
        self.pay_deja_paye.update()
        self.pay_montant.value = f"{e.control.data['mt_remise']}"
        self.pay_montant.update()
        self.new_paiement_window.scale = 1
        self.new_paiement_window.update()

    def close_new_paiement(self, e):
        self.new_paiement_window.scale = 0
        self.new_paiement_window.update()

    def create_paiement(self, e):
        if self.pay_a_regler.value is None or self.pay_a_regler.value == "":
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Attention au montant"
            self.cp.box.open = True
            self.cp.box.update()

        elif int(self.pay_a_regler.value) > (int(self.pay_montant.value) - int(self.pay_deja_paye.value)):
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = "Solde payé > au montant de la facture !"
            self.cp.box.open = True
            self.cp.box.update()

        else:
            be.add_reglement(
                self.pay_facture.value, int(self.pay_a_regler.value), self.pay_mode.value, self.pay_selected_date.value
            )
            self.cp.box.title.value = "Confirmé"
            self.cp.box.content.value = "Paiement sauvegardé"
            self.cp.box.open = True
            self.cp.box.update()

            for widget in (
                self.pay_deja_paye, self.pay_montant, self.pay_facture, self.pay_mode,
                self.pay_a_regler, self.pay_solde, self.pay_selected_date
            ):
                widget.value = None
                widget.update()

            self.new_paiement_window.scale = 0
            self.new_paiement_window.update()

            self.load_datas()
            self.table.update()
            self.results.update()

    def changement_date(self, e):
        self.pay_selected_date.value = str(self.cp.dp_paiement.value)[0:10]
        self.pay_selected_date.update()

    def changement_solde(self, e):
        if self.pay_solde.value:
            self.pay_a_regler.value = f"{int(self.pay_montant.value) - int(self.pay_deja_paye.value)}"
            self.pay_a_regler.update()
        else:
            self.pay_a_regler.value = None
            self.pay_a_regler.update()

    def open_edit_window(self, e):
        # remplissage des détails de la facture
        self.edit_num.value = f"{e.control.data['numero']}"
        self.edit_dev.value = f"{e.control.data['devis']}"

        if e.control.data["reste"] == 0:
            self.edit_icon_statut.name = ft.icons.CHECK
            self.edit_statut.value = "soldée".upper()
            self.ct_statut.bgcolor = "green"
        else:
            self.edit_icon_statut.name = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
            self.edit_statut.value = "En cours".upper()
            self.ct_statut.bgcolor = "red"

        self.edit_objet.value = e.control.data["objet"]
        self.edit_delai.value = e.control.data["delai"]
        self.edit_remise.value = f"{e.control.data['remise']}"
        self.edit_montant.value = f"{e.control.data['mt_remise']}"
        self.edit_lettres.value = ecrire_en_lettres(e.control.data["mt_remise"])
        self.edit_bc.value = e.control.data["bc_client"]
        self.edit_ov.value = e.control.data["ov"]

        self.edit_lettres.update()
        self.edit_bc.update()
        self.edit_ov.update()
        self.edit_remise.update()
        self.edit_montant.update()
        self.edit_delai.update()
        self.edit_objet.update()
        self.edit_statut.update()
        self.edit_icon_statut.update()
        self.edit_num.update()
        self.edit_dev.update()
        self.ct_statut.update()

        # Remplissage des détails de la table
        details = be.factures_details(e.control.data["numero"])
        for widget in self.edit_table.controls[:]:
            self.edit_table.controls.remove(widget)

        for detail in details:
            self.edit_table.controls.append(
                OneArticle(self, detail["reference"], detail["designation"], detail["qte"], detail["prix"])
            )

        self.edit_table.update()
        self.edit_window.scale = 1
        self.edit_window.update()

    def close_edit_window(self, e):
        self.edit_window.scale = 0
        self.edit_window.update()

    def open_impression_window(self, e):
        self.impression_window.scale = 1
        self.impression_window.update()

    def close_impression_window(self, e):
        self.impression_window.scale = 0
        self.impression_window.update()

    def voir_paiements(self, e):
        self.vp_numero.value = e.control.data["numero"]

        if e.control.data["reste"] == 0:
            self.vp_statut.value = "soldée".upper()
            self.vp_icone_statut.name = ft.icons.CHECK
            self.vp_ct_statut.bgcolor = "green"
        else:
            self.vp_statut.value = "en cours".upper()
            self.vp_icone_statut.name = ft.icons.INDETERMINATE_CHECK_BOX_OUTLINED
            self.vp_ct_statut.bgcolor = "red"

        for row in self.vp_table.rows[:]:
            self.vp_table.rows.remove(row)

        datas = be.all_reglements_by_facture(e.control.data["numero"])

        for data in datas:
            self.vp_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["date"])),
                        ft.DataCell(ft.Text(data["type"])),
                        ft.DataCell(ft.Text(ajout_separateur(data["montant"]))),
                    ]
                )
            )

        self.vp_table.update()

        self.vp_numero.update()
        self.vp_statut.update()
        self.vp_icone_statut.update()
        self.vp_ct_statut.update()
        self.paiements_window.scale = 1
        self.paiements_window.update()

    def close_paiements_window(self, e):
        self.paiements_window.scale = 0
        self.paiements_window.update()

    def imprimer_devis(self, e: ft.FilePickerResultEvent):
        regime = self.regime.value
        tva = self.tva.value
        ir = self.ir.value

        # Cas du régime simplifié
        if self.regime.value == "S":

            # Si la TVA est Active
            if tva is True:
                # Erreur
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "Pas de TVA dans le régime simplifié"
                self.cp.box.open = True
                self.cp.box.update()

            # Si la TVA n'est pas active
            else:
                # Si l'IR est active
                if ir is True:
                    pass

                # Si l'IR n'est pos active
                else:
                    pass

        # Cas du régime réel
        else:
            # Si la TVA est Active
            if tva is True:
                if ir is True:
                    pass

                # Si l'IR n'est pos active
                else:
                    pass

            # Si la TVA n'est pas active
            else:
                # Si l'IR est active
                if ir is True:
                    pass

                # Si l'IR n'est pos active
                else:
                    pass



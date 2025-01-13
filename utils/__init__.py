import flet as ft
from utils.constantes import FIRST_COLOR, SECOND_COLOR, THIRD_COLOR

datatable_style: dict = dict(
    data_text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    heading_text_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="grey"),
)

search_field_style: dict = dict(
    dense=True,
    border_color="#f2f2f2", bgcolor="#f2f2f2",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=8, border_width=1, cursor_color=SECOND_COLOR, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
field_style: dict = dict(
    dense=True,
    focused_border_color=FIRST_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=8, border_width=1, cursor_color=SECOND_COLOR, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
numbers_field_style: dict = dict(
    dense=True,
    focused_border_color=FIRST_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=8, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=2,
    input_filter=ft.NumbersOnlyInputFilter(), text_align=ft.TextAlign.RIGHT.RIGHT
)
login_style: dict = dict(
    dense=True,
    focused_border_color=FIRST_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=2,
)
inactive_field_style: dict = dict(
    dense=True, disabled=True,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=8, border_width=1,
    capitalization=ft.TextCapitalization.CHARACTERS
)
readonly_field_style: dict = dict(
    dense=True, read_only=True,
    border_color=None, bgcolor=None, border=ft.InputBorder.NONE,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=8, border_width=1, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)

date_field_style: dict = dict(
    height=45,
    focused_border_width=2, focused_border_color=FIRST_COLOR,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins Medium"),
    border_radius=8, border_width=1, cursor_color=SECOND_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)

drop_style: dict = dict(
    dense=True, height=45, border_radius=12,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="black"),
    focused_border_color=FIRST_COLOR, border_width=1,
    focused_border_width=2,
)

radio_style = dict(
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    fill_color=SECOND_COLOR
)


class AnyButton(ft.ElevatedButton):
    def __init__(self, theme_color:str, my_icon: str, title: str, text_color: str, my_width, click):
        super().__init__(
            bgcolor=theme_color,
            height=40, width=my_width, elevation=1,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=22)
            ),
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            content=ft.Row(
                controls=[
                    ft.Icon(my_icon, color="white", size=16),
                    ft.Text(title, size=12, font_family="Poppins Medium", color=text_color)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8
            ),
            on_click=click, on_hover=self.hover_bt
        )

    def hover_bt(self, e):
        if e.data == "true":
            self.scale = 1.1
            self.update()
        else:
            self.scale = 1
            self.update()


class CtButton(ft.Container):
    def __init__(self, my_icon, my_tool,my_datas, on_click_function,):
        super().__init__(
            border_radius=6, padding=5,
            on_click=on_click_function,
            scale=ft.transform.Scale(0.9),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            on_hover=self.hover_ct,
            data=my_datas,
            tooltip=my_tool,
            content=ft.Icon(
                my_icon,
                color=ft.colors.BLACK45,
            )
        )
        self.my_icon = my_icon

    def hover_ct(self, e):
        if e.data == "true":
            self.scale = 1.2
            self.update()
        else:
            self.scale = 0.9
            self.update()

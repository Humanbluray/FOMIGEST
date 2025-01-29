import flet as ft


class Vue(ft.Container):
    def __init__(self):
        super().__init__(
        )

        self.content = ft.Stack(
            controls=[
                ft.Image(src="assets/images/background.jpg"),
                ft.Column(
                    controls=[
                        ft.Row([Test(), Test(), Test()], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.START)
                    ]
                )
            ]
        )


class Test(ft.Container):
    def __init__(self):
        super().__init__(
            padding=ft.padding.only(10, 5, 10, 5),
            bgcolor=None, border_radius=16,
            width=150, height=50, on_hover=self.on_hover_ct
        )

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Menu 1", font_family="Poppins Medium",
                        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)),
                        ft.IconButton(ft.icons.KEYBOARD_ARROW_DOWN_OUTLINED, scale=0.7, bgcolor=None)
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Column(
                    controls=[
                        ft.Text("Menu 2", font_family="Poppins Medium"),
                        ft.Text("Menu 3", font_family="Poppins Medium"),
                        ft.Text("Menu 4", font_family="Poppins Medium"),
                        ft.Text("Menu 5", font_family="Poppins Medium"),
                        ft.Text("Menu 6", font_family="Poppins Medium"),
                    ]
                )
            ]
        )

    def on_hover_ct(self, e):
        if e.data == "true":
            self.height = None
            self.update()
        else:
            self.height = 40
            self.update()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Poppins Regular": "fonts/Poppins-Regular.ttf",
        "Poppins Bold": "fonts/Poppins-Bold.ttf",
        "Poppins SemiBold": "fonts/Poppins-SemiBold.ttf",
        "Poppins Black": "fonts/Poppins-Black.ttf",
        "Poppins Italic": "fonts/Poppins-Italic.ttf",
        "Poppins Medium": "fonts/Poppins-Medium.ttf",
        "Poppins ExtraBold": "fonts/Poppins-ExtraBold.ttf",
        "Poppins Light": "fonts/Poppins-Light.ttf",
    }
    page.add(Vue())


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
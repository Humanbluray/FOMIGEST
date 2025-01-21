from utils import *
import flet as ft
import backend as be
from utils.useful_functions import ajout_separateur


class Stock(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True)
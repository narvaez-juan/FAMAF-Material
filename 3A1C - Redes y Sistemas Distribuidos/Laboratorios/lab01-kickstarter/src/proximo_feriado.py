import requests
from datetime import date


def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"


months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
    'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]
days = [
    'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'
]
type_of_holidays = ['inamovible', 'trasladable', 'nolaborable', 'puente']
"""
Tipos de feriado aceptados por la api.
"""


def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]


class NextHoliday:
    def __init__(self):
        self.loading = True
        self.found = False
        """
        Si se ha encontrado el holiday o no.
        """
        self.year = date.today().year
        """
        Año correspondiente.
        """
        self.holiday = None
        """
        Feriado a devolver.
        """

    def get_month_next_holiday(self):
        return months[self.holiday['mes'] - 1]

    def set_next(
            self, holidays, type_holiday:str='inamovible', day=None, month=None):
        """
        Setea el feriado que cumple el filtro solicitado.

        `holidays`: json - todos los feriados del año correspondiente.

        `type_holiday`: string - Valores esperados: inamovible,
        trasladable, nolaborable, puente

        `day`: string | int - día a filtrar.

        `month`: string | int - mes a filtrar.
        """
        day = None if day == 'None' else day
        month = None if month == 'None' else month

        if day is not None and month is not None:
            try:
                c_date = {
                'day': int(day),
                'month': int(month)
            }
            except ValueError:
                now = date.today()
                c_date = {
                    'day': now.day,
                    'month': now.month
                }
        else:
            now = date.today()
            c_date = {
                'day': now.day,
                'month': now.month
            }

        for h in holidays:
            if (h['tipo'] == type_holiday) and (h['mes'] == c_date['month'] and h['dia'] > c_date['day'] or h['mes'] > c_date['month']):  # noqa
                self.holiday = h
                self.loading = False
                self.found = True
                return

    def fetch_holidays(self):
        """
        Obtiene todos los feriados del año.
        """
        return requests.get(get_url(self.year)).json()

    def next_holiday_json(self):
        """
        Devuelve en formato json el feriado seleccionado en `self.holiday`.
        """
        if self.found:
            day_name = f"{day_of_week(self.holiday['dia'], self.holiday['mes'], self.year)}"  # noqa
            day_and_month = f"{self.holiday['dia']} de {self.get_month_next_holiday()}"  # noqa
            return {
                "dia": self.holiday['dia'],
                "mes": self.holiday['mes'],
                "fecha": f"{day_name} {day_and_month}",
                "motivo": self.holiday['motivo'],
                "tipo": self.holiday['tipo'],
                "año": self.year
            }, 200
        else:
            return {
                "error": "No se ha encontrado un feriado del tipo solicitado."
            }, 404

    def render(self):
        if self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(
                self.holiday['dia'], self.holiday['mes'], self.year))
            print(self.holiday['dia'])
            print(self.get_month_next_holiday())
            print("Tipo:")
            print(self.holiday['tipo'])

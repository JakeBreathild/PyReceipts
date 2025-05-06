from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Label, Footer, Header, DataTable, Input, Static
from msl.odt import Document
#Matrix to keep DataTable Data
Matrix = [("Nombre", "Fecha", "Precio")]
day = 0
month = 0
year = 0
city = ""
account = 0
company = ""
nit = ""
owe = ""
cc = ""
firstday = 0
lastday = 0
quantity = ""
name = ""
total = 0
class Setup(Static):
    def compose(self) -> ComposeResult:
        yield Label("Configuracion Inicial")
        yield Input(placeholder="Dia de entrega", id="day", type="number")
        yield Input(placeholder="Mes", id="month", type="number")
        yield Input(placeholder="Año", id="year", type="number")
        yield Input(placeholder="Ciudad", id="city", type="text")
        yield Input(placeholder="Numero de Cuenta", id="account", type="number")
        yield Input(placeholder="Empresa", id="company", type="text")
        yield Input(placeholder="NIT", id="nit", type="text")
        yield Input(placeholder="Debe A", id="owe", type="text")
        yield Input(placeholder="Cedula", id="cc", type="text")
        yield Input(placeholder="Primer dia del Mes", id="firstday", type="number")
        yield Input(placeholder="Ultimo dia del Mes", id="lastday", type="number")
        yield Button("Finalizar Configuracion", id="config")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "config":
            self.add_class("hide")
            self.query_ancestor("PyReceipts").query_one(AfterSetup).remove_class("hide")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        global day, month, year, city, account, company, nit, owe, cc, firstday, lastday
        input_id = event.input.id
        if input_id == "day":
            day = int(event.value)
        elif input_id == "month":
            month = int(event.value)
        elif input_id == "year":
            year = int(event.value)
        elif input_id == "city":
            city = event.value
        elif input_id == "account":
            account = int(event.value)
        elif input_id == "company":
            company = event.value
        elif input_id == "nit":
            nit = event.value
        elif input_id == "owe":
            owe = event.value
        elif input_id == "cc":
            cc = event.value
        elif input_id == "firstday":
            firstday = int(event.value)
        elif input_id == "lastday":
            lastday = int(event.value)




class AfterSetup(Static):
    global day, month, year, city, account, company, nit, owe, cc, firstday, lastday
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Nombre", id="name", type="text")
        yield Input(placeholder="Fecha", id="date", type="text")
        yield Input(placeholder="Precio", id="price", type="integer")
        yield Label("Total: ", id="total")
        yield Input(placeholder="(Llenar antes de generar archivo) Cantidad en Letras", id="quantity")
        yield Button("Generar Recibo", id="generate")
        yield Label(city, id="test")
        yield CustomDataTable(id="table")


    def on_mount(self) -> None:
        self.add_class("hide")

class CustomDataTable(Static):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(DataTable())

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        for col in Matrix:
            table.add_columns(*Matrix[0])



class PyReceipts(App):

    CSS_PATH = "PyReceipts.css"
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield Setup(id="setup")
        yield AfterSetup(id="after")




if __name__ == "__main__":
    PyReceipts().run()
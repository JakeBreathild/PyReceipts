from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Label, Footer, Header, DataTable, Input, Static
from msl.odt import Document
#Matrix to keep DataTable Data
Matrix = [("Nombre", "Fecha", "Precio")]
class Setup(Static):
    def compose(self) -> ComposeResult:
        yield Label("Configuracion Inicial: ")
        yield Input(placeholder="Dia")
        yield Input(placeholder="Mes")
        yield Input(placeholder="Año")
        yield Input(placeholder="Ciudad")
        yield Input(placeholder="Numero de Cuenta")
        yield Input(placeholder="Empresa")
        yield Input(placeholder="NIT")
        yield Input(placeholder="Ciudad")
        yield Input(placeholder="Debe A")
        yield Input(placeholder="Cedula")
        yield Input(placeholder="Primer dia del Mes")
        yield Input(placeholder="Ultimo dia del Mes")

class InputField(Static):
    pass

class CustomDataTable(Static):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(DataTable())

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        for col in Matrix:
            table.add_columns(*Matrix[0])

class PyReceipts(App):

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        inputname = Input(placeholder="Nombre", id="name",)
        inputdate = Input(placeholder="Fecha", id="date")
        inputprice = Input(placeholder="Precio", id="price")
        yield inputname
        yield inputdate
        yield inputprice
        yield Label("Total: ",id="total")
        yield Input(placeholder="(Llenar antes de generar archivo) Cantidad en Letras", id="quantity")
        yield CustomDataTable(id="table")
        yield Setup(id="setup")


if __name__ == "__main__":
    PyReceipts().run()
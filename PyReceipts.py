from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Label, Footer, Header, DataTable, Input, Static
from msl.odt import Document
import string
#Matrix for table columns
Matrix = [("Nombre", "Fecha", "Precio", "Total")]
ROWS = []
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
last_name = ""
total = 0
price = 0
date = 0
doc = Document("cuenta generada.odt")
first_time = True
first_time2 = True
class Setup(Static):
    def compose(self) -> ComposeResult:
        yield Label("Configuracion Inicial")
        yield Input(placeholder="Dia de entrega", id="day", type="number")
        yield Input(placeholder="Mes", id="month", type="text")
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
            self.query_one("#day").remove()
        elif input_id == "month":
            month = event.value
            self.query_one("#month").remove()
        elif input_id == "year":
            year = int(event.value)
            self.query_one("#year").remove()
        elif input_id == "city":
            city = event.value
            self.query_one("#city").remove()
        elif input_id == "account":
            account = int(event.value)
            self.query_one("#account").remove()
        elif input_id == "company":
            company = event.value
            self.query_one("#company").remove()
        elif input_id == "nit":
            nit = event.value
            self.query_one("#nit").remove()
        elif input_id == "owe":
            owe = event.value
            self.query_one("#owe").remove()
        elif input_id == "cc":
            cc = event.value
            self.query_one("#cc").remove()
        elif input_id == "firstday":
            firstday = int(event.value)
            self.query_one("#firstday").remove()
        elif input_id == "lastday":
            lastday = int(event.value)
            self.query_one("#lastday").remove()




class AfterSetup(Static):
    global day, month, year, city, account, company, nit, owe, cc, firstday, lastday
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Nombre", id="name", type="text")
        yield Input(placeholder="Dia", id="date", type="integer")
        yield Input(placeholder="Precio", id="price", type="integer")
        yield Button("Agregar", id="add")
        yield Input(placeholder="(Llenar antes de generar archivo) Cantidad en Letras", id="quantity")
        yield Button("Generar Recibo", id="generate")
        yield CustomDataTable(id="table")


    def on_mount(self) -> None:
        self.add_class("hide")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        global name, quantity, price, date, last_name, first_time
        input_id = event.input.id
        if input_id == "name":
            if first_time:
                name = event.value
                last_name = name
                first_time = False
            else:
                last_name = name
                name = event.value
            self.query_one("#name").disabled = True
        elif input_id == "date":
            date = int(event.value)
            self.query_one("#date").disabled = True
        elif input_id == "price":
            price = int(event.value)
            self.query_one("#price").disabled = True
        elif input_id == "quantity":
            quantity = event.value
            self.query_one("#quantity").blur()


    def on_button_pressed(self, event: Button.Pressed) -> None:
        global Matrix, total, name, date, price, company, ROWS, last_name, doc, first_time2
        button_id = event.button.id
        if button_id == "add":
            total = price + total
            ROWS.append((name, date, "$" + str(price), "$" + str(total)))
            self.query_one("#table").query_one(DataTable).clear()
            self.query_one("#table").query_one(DataTable).add_rows(ROWS)
            self.query_one("#name").disabled = False
            self.query_one("#date").disabled = False
            self.query_one("#price").disabled = False

            if first_time2:
                doc.addheading1(str(name))
                doc.addtext("Dia:\t\t\t\t\t\tCantidad:\n{0}\t\t\t\t\t\t${1}".format(str(date), str(price)))
                first_time2 = False
            elif last_name == name:
                doc.addtext("{0}\t\t\t\t\t\t${1}".format(str(date), str(price)))
            else:
                doc.addheading1(str(name))
                doc.addtext("Dia:\t\t\t\t\t\tCantidad:\n{0}\t\t\t\t\t\t${1}".format( str(date), str(price)))

        elif button_id == "generate":
            doc.addpagebreak()
            doc.addtext("{0}, {1} DE {2} DEL {3}\n\n".format(str(city).upper(), str(day), str(month).upper(), str(year)))
            doc.addtext("CUENTA DE COBRO N# {0}\n\n\n{1}\nNIT. {2}\n\n\n\n\nDEBE A\n{3}\n\n\nCC. {4}\n\n\n\n\n".format(str(account), str(company).upper(), str(nit), str(owe).upper(), str(cc)))
            doc.addtext("LA SUMA DE {0} (${1}).\n\n\nPOR CONCEPTO DE SERVICIO DE COMEDOR {2} {3} A {4} {5} DEL {6}".format(str(quantity).upper(), str(total), str(month).upper(), str(firstday), str(month).upper(), str(lastday), str(year)))
            doc.addtext("\n\n\n\nATENTAMENTE,\n\n\n\n\n\n\n{0}\nCC. {1}".format(str(owe).upper(), str(cc)))
            doc.save()

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
import ast
import operator
import tkinter as tk


def evaluar_expresion(expresion: str) -> float | int:
    """Evalúa de forma segura una expresión matemática básica."""
    operadoresPermitidos = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(nodo):
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return nodo.value
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in operadoresPermitidos:
            izq = _eval(nodo.left)
            der = _eval(nodo.right)
            if isinstance(nodo.op, ast.Div) and der == 0:
                raise ZeroDivisionError("División entre cero")
            return operadoresPermitidos[type(nodo.op)](izq, der)
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in operadoresPermitidos:
            return operadoresPermitidos[type(nodo.op)](_eval(nodo.operand))
        raise ValueError("Expresión inválida")

    arbol = ast.parse(expresion, mode="eval")
    resultado = _eval(arbol.body)
    if isinstance(resultado, float) and resultado.is_integer():
        return int(resultado)
    return round(resultado, 10) if isinstance(resultado, float) else resultado


class CalculadoraApp:
    """Calculadora básica con interfaz gráfica en Tkinter."""

    COLOR_FONDO = "#1e1e2e"
    COLOR_PANTALLA = "#181825"
    COLOR_TEXTO = "#cdd6f4"
    COLOR_SUBTEXTO = "#a6adc8"
    COLOR_BTN_NUM = "#313244"
    COLOR_BTN_NUM_HOVER = "#45475a"
    COLOR_BTN_OP = "#fab387"
    COLOR_BTN_OP_TEXTO = "#11111b"
    COLOR_BTN_ACCION = "#585b70"
    COLOR_BTN_IGUAL = "#a6e3a1"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("340x500")
        self.root.minsize(300, 440)
        self.root.configure(bg=self.COLOR_FONDO)

        self.expresion_actual = ""
        self.historial_texto = tk.StringVar(value="")
        self.pantalla_texto = tk.StringVar(value="0")
        self.reiniciar_al_escribir = False

        self._crear_interfaz()
        self._vincular_teclado()

    def _crear_interfaz(self) -> None:
        # Contenedor de pantalla
        frame_pantalla = tk.Frame(self.root, bg=self.COLOR_PANTALLA, padx=16, pady=16)
        frame_pantalla.pack(fill="both", padx=12, pady=(12, 6))

        lbl_historial = tk.Label(
            frame_pantalla,
            textvariable=self.historial_texto,
            font=("Segoe UI", 12),
            bg=self.COLOR_PANTALLA,
            fg=self.COLOR_SUBTEXTO,
            anchor="e",
        )
        lbl_historial.pack(fill="x")

        lbl_pantalla = tk.Label(
            frame_pantalla,
            textvariable=self.pantalla_texto,
            font=("Segoe UI Semibold", 32),
            bg=self.COLOR_PANTALLA,
            fg=self.COLOR_TEXTO,
            anchor="e",
        )
        lbl_pantalla.pack(fill="x", pady=(4, 0))

        # Contenedor de botones
        frame_botones = tk.Frame(self.root, bg=self.COLOR_FONDO)
        frame_botones.pack(fill="both", expand=True, padx=10, pady=6)

        for i in range(5):
            frame_botones.rowconfigure(i, weight=1)
        for j in range(4):
            frame_botones.columnconfigure(j, weight=1)

        botones = [
            ("C", 0, 0, self.COLOR_BTN_ACCION, self.COLOR_TEXTO),
            ("⌫", 0, 1, self.COLOR_BTN_ACCION, self.COLOR_TEXTO),
            ("%", 0, 2, self.COLOR_BTN_ACCION, self.COLOR_TEXTO),
            ("÷", 0, 3, self.COLOR_BTN_OP, self.COLOR_BTN_OP_TEXTO),
            ("7", 1, 0, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("8", 1, 1, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("9", 1, 2, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("×", 1, 3, self.COLOR_BTN_OP, self.COLOR_BTN_OP_TEXTO),
            ("4", 2, 0, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("5", 2, 1, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("6", 2, 2, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("-", 2, 3, self.COLOR_BTN_OP, self.COLOR_BTN_OP_TEXTO),
            ("1", 3, 0, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("2", 3, 1, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("3", 3, 2, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("+", 3, 3, self.COLOR_BTN_OP, self.COLOR_BTN_OP_TEXTO),
            ("±", 4, 0, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("0", 4, 1, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            (".", 4, 2, self.COLOR_BTN_NUM, self.COLOR_TEXTO),
            ("=", 4, 3, self.COLOR_BTN_IGUAL, self.COLOR_BTN_OP_TEXTO),
        ]

        for texto, fila, col, bg_color, fg_color in botones:
            btn = tk.Button(
                frame_botones,
                text=texto,
                font=("Segoe UI Semibold", 16),
                bg=bg_color,
                fg=fg_color,
                activebackground=self.COLOR_BTN_NUM_HOVER,
                activeforeground=fg_color,
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda t=texto: self.al_presionar_boton(t),
            )
            btn.grid(row=fila, column=col, sticky="nsew", padx=4, pady=4)

    def _vincular_teclado(self) -> None:
        self.root.bind("<Key>", self._al_presionar_tecla)

    def _al_presionar_tecla(self, evento: tk.Event) -> None:
        tecla = evento.keysym
        char = evento.char

        if char in "0123456789+-." and char != "":
            self.al_presionar_boton(char)
        elif char == "*":
            self.al_presionar_boton("×")
        elif char == "/":
            self.al_presionar_boton("÷")
        elif char == "%":
            self.al_presionar_boton("%")
        elif tecla in ("Return", "KP_Enter", "equal"):
            self.al_presionar_boton("=")
        elif tecla == "BackSpace":
            self.al_presionar_boton("⌫")
        elif tecla in ("Escape", "c", "C"):
            self.al_presionar_boton("C")

    def al_presionar_boton(self, valor: str) -> None:
        if valor == "C":
            self.expresion_actual = ""
            self.historial_texto.set("")
            self.pantalla_texto.set("0")
            self.reiniciar_al_escribir = False
            return

        if valor == "⌫":
            if self.reiniciar_al_escribir:
                self.al_presionar_boton("C")
                return
            self.expresion_actual = self.expresion_actual[:-1]
            self._actualizar_pantalla()
            return

        if valor == "=":
            self._calcular_resultado()
            return

        if valor == "%":
            self._aplicar_porcentaje()
            return

        if valor == "±":
            self._cambiar_signo()
            return

        mapa_op = {"×": "*", "÷": "/"}
        token = mapa_op.get(valor, valor)

        if self.reiniciar_al_escribir:
            if token in "0123456789.":
                self.expresion_actual = ""
            self.reiniciar_al_escribir = False

        if token in "+-*/":
            if not self.expresion_actual and token != "-":
                self.expresion_actual = "0"
            if self.expresion_actual and self.expresion_actual[-1] in "+-*/":
                self.expresion_actual = self.expresion_actual[:-1] + token
            else:
                self.expresion_actual += token
        elif token == ".":
            ultimo_numero = self._obtener_ultimo_numero()
            if "." not in ultimo_numero:
                if not ultimo_numero:
                    self.expresion_actual += "0."
                else:
                    self.expresion_actual += "."
        else:
            self.expresion_actual += token

        self._actualizar_pantalla()

    def _obtener_ultimo_numero(self) -> str:
        partes = (
            self.expresion_actual.replace("+", " ")
            .replace("-", " ")
            .replace("*", " ")
            .replace("/", " ")
            .split()
        )
        return partes[-1] if partes else ""

    def _aplicar_porcentaje(self) -> None:
        if not self.expresion_actual:
            return
        try:
            valor = evaluar_expresion(self.expresion_actual)
            porcentaje = evaluar_expresion(f"{valor} / 100")
            self.expresion_actual = str(porcentaje)
            self._actualizar_pantalla()
        except Exception:
            self.pantalla_texto.set("Error")
            self.reiniciar_al_escribir = True

    def _cambiar_signo(self) -> None:
        if not self.expresion_actual or self.expresion_actual == "0":
            return
        if self.expresion_actual.startswith("-"):
            self.expresion_actual = self.expresion_actual[1:]
        else:
            self.expresion_actual = "-" + self.expresion_actual
        self._actualizar_pantalla()

    def _calcular_resultado(self) -> None:
        if not self.expresion_actual:
            return
        expresion_visual = (
            self.expresion_actual.replace("*", " × ").replace("/", " ÷ ")
        )
        try:
            resultado = evaluar_expresion(self.expresion_actual)
            self.historial_texto.set(f"{expresion_visual} =")
            self.pantalla_texto.set(str(resultado))
            self.expresion_actual = str(resultado)
            self.reiniciar_al_escribir = True
        except ZeroDivisionError:
            self.historial_texto.set(f"{expresion_visual} =")
            self.pantalla_texto.set("No se puede ÷ 0")
            self.expresion_actual = ""
            self.reiniciar_al_escribir = True
        except Exception:
            self.pantalla_texto.set("Error")
            self.expresion_actual = ""
            self.reiniciar_al_escribir = True

    def _actualizar_pantalla(self) -> None:
        if not self.expresion_actual:
            self.pantalla_texto.set("0")
        else:
            visual = self.expresion_actual.replace("*", "×").replace("/", "÷")
            self.pantalla_texto.set(visual)


def main() -> None:
    root = tk.Tk()
    CalculadoraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

class Persona:
    def __init__(self, nombre, edad, peso_persona):
        self.nombre = nombre
        self.edad = edad
        self.peso_persona = peso_persona

    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Peso: {self.peso_persona}"


class Cabina:
    MAX_PERSONAS = 10
    MAX_PESO = 850.0

    def __init__(self, nro_cabina):
        self.nro_cabina = nro_cabina
        self.personas_abordo = []
        self.cantidad_cabinas = 0  

    def agregar_persona(self, persona):
        if len(self.personas_abordo) < Cabina.MAX_PERSONAS and sum(p.peso_persona for p in self.personas_abordo) + persona.peso_persona <= Cabina.MAX_PESO:
            self.personas_abordo.append(persona)
            return True
        else:
            print(f"No se puede agregar a {persona.nombre} a la cabina {self.nro_cabina} (Límite de peso o personas alcanzado).")
            return False

    def agregar_persona(self, persona):
        if len(self.personas_abordo) < Cabina.MAX_PERSONAS and sum(p.peso_persona for p in self.personas_abordo) + persona.peso_persona <= Cabina.MAX_PESO:
            self.personas_abordo.append(persona)
            return True
        else:
            print(f"No se puede agregar a {persona.nombre} a la cabina {self.nro_cabina} (Límite de peso o personas alcanzado).")
            return False

    def __str__(self):
        return f"Cabina nro: {self.nro_cabina}, Personas a bordo: {len(self.personas_abordo)}"

class Linea:
    def __init__(self, color):
        self.color = color
        self.cabinas = []

    def agregar_cabina(self, cabina):
        self.cabinas.append(cabina)

    def agregar_persona_fila(self, persona, cabina):
        if cabina in self.cabinas:
            cabina.agregar_persona(persona)
        else:
            print(f"La cabina no pertenece a esta línea.")

    def __str__(self):
        return f"Línea de color: {self.color}, número de cabinas: {len(self.cabinas)}"


class MiTeleferico:
    def __init__(self):
        self.lineas = []
        self.cantidad_ingresos = 0.0

    def agregar_linea(self, linea):
        self.lineas.append(linea)

    def calcular_ingreso_total(self):
        total = 0
        for linea in self.lineas:
            for cabina in linea.cabinas:
                for persona in cabina.personas_abordo:
                    if persona.edad < 25 or persona.edad > 60:
                        total += 1.5
                    else:
                        total += 3
        self.cantidad_ingresos = total
        return total

    def mostrar_linea_con_mas_ingreso_regular(self):
        linea_con_mas_ingreso = None
        max_ingreso_regular = 0

        for linea in self.lineas:
            ingreso_regular_linea = 0
            for cabina in linea.cabinas:
                for persona in cabina.personas_abordo:
                    if 25 <= persona.edad <= 60:
                        ingreso_regular_linea += 3

            if ingreso_regular_linea > max_ingreso_regular:
                max_ingreso_regular = ingreso_regular_linea
                linea_con_mas_ingreso = linea

        if linea_con_mas_ingreso:
            print(f"La línea con más ingreso regular es: {linea_con_mas_ingreso.color} con ingreso de: {max_ingreso_regular}")
        else:
            print("No hay líneas con ingresos regulares.")



teleferico = MiTeleferico()

linea_amarilla = Linea("Amarilla")
linea_roja = Linea("Roja")
teleferico.agregar_linea(linea_amarilla)
teleferico.agregar_linea(linea_roja)


cabina1 = Cabina(1)
cabina2 = Cabina(2)
linea_amarilla.agregar_cabina(cabina1)
linea_roja.agregar_cabina(cabina2)

persona1 = Persona("Juan", 30, 75)
persona2 = Persona("Maria", 20, 60)
persona3 = Persona("Pedro", 70, 70)
persona4 = Persona("Laura", 40, 65)


linea_amarilla.agregar_persona_fila(persona1, cabina1)
linea_amarilla.agregar_persona_fila(persona2, cabina1)
linea_roja.agregar_persona_fila(persona3, cabina2)
linea_roja.agregar_persona_fila(persona4, cabina2)


ingreso_total = teleferico.calcular_ingreso_total()
print(f"Ingreso total del teleférico: {ingreso_total}")


teleferico.mostrar_linea_con_mas_ingreso_regular()
import json


class consulta:
    def __init__(self, ci, nombrepaciente, apellidopaciente, idmed, dia, mes, anio):
        self.ci = ci
        self.nombrepaciente = nombrepaciente.strip()
        self.apellidopaciente = apellidopaciente.strip()
        self.idmed = idmed
        self.dia = dia
        self.mes = mes.lower().strip()
        self.anio = anio

    def to_dict(self):
        return {
            "ci": self.ci,
            "nombrepaciente": self.nombrepaciente,
            "apellidopaciente": self.apellidopaciente,
            "idmed": self.idmed,
            "dia": self.dia,
            "mes": self.mes,
            "anio": self.anio
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["ci"], data["nombrepaciente"], data["apellidopaciente"], data["idmed"], data["dia"], data["mes"], data["anio"])
        
    def __str__(self):
        return f"CI: {self.ci}, Paciente: {self.nombrepaciente} {self.apellidopaciente}, ID Médico: {self.idmed}, Fecha: {self.dia} de {self.mes} de {self.anio}"


class medico:
    def __init__(self, idmed, nombremed, apellidomed, aniosexperiencia):
        self.idmed = idmed
        self.nombremed = nombremed.strip()
        self.apellidomed = apellidomed.strip()
        self.aniosexperiencia = aniosexperiencia

    def to_dict(self):
        return {
            "idmed": self.idmed,
            "nombremed": self.nombremed,
            "apellidomed": self.apellidomed,
            "aniosexperiencia": self.aniosexperiencia
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["idmed"], data["nombremed"], data["apellidomed"], data["aniosexperiencia"])
        
    def __str__(self):
        return f"ID: {self.idmed}, Médico: {self.nombremed} {self.apellidomed}, Años Exp: {self.aniosexperiencia}"



class Persistencia:
    def __init__(self, archivo):
        self.archivo = archivo

    def _existe_y_no_vacio(self):
        
        try:
            with open(self.archivo, "r") as archivo:
               
                data = json.load(archivo)
                return bool(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def guardar(self, data_list, indent_val=5):
        with open(self.archivo, "w") as archivo:
            json.dump(data_list, archivo, indent=indent_val)
    
    def leer_medicos(self):
        if not self._existe_y_no_vacio():
            return []
            
        try:
            with open(self.archivo, "r") as archivo:
                data = json.load(archivo)
                return [medico.from_dict(d) for d in data]
        except json.JSONDecodeError:
            print(f"Advertencia: Archivo {self.archivo} mal formado. Devolviendo lista vacía.")
            return []

    def leer_consultas(self):
        if not self._existe_y_no_vacio():
            return []
            
        try:
            with open(self.archivo, "r") as archivo:
                data = json.load(archivo)
                return [consulta.from_dict(d) for d in data]
        except json.JSONDecodeError:
            print(f"Advertencia: Archivo {self.archivo} mal formado. Devolviendo lista vacía.")
            return []

    
    def agregar_medico(self, nuevo_medico):
        medicos = self.leer_medicos()
        if any(m.idmed == nuevo_medico.idmed for m in medicos):
            print(f"Error: Ya existe un médico con ID {nuevo_medico.idmed}.")
            return
        medicos.append(nuevo_medico)
        data = [m.to_dict() for m in medicos]
        self.guardar(data)
        print("Medico agregado con exito.")
    



    def eliminar_medico(self, nombremed, apellidomed):
        medicos = self.leer_medicos()
        
        medico_a_eliminar = next((m for m in medicos if m.nombremed.lower() == nombremed.lower() and m.apellidomed.lower() == apellidomed.lower()), None)
        
        if not medico_a_eliminar:
            return False, None 
            
        id_medico_eliminado = medico_a_eliminar.idmed
        
        medicos = [m for m in medicos if m.idmed != id_medico_eliminado]
        
        data = [m.to_dict() for m in medicos]
        self.guardar(data)
        return True, id_medico_eliminado 





    def agregar_consultas(self, nueva_consulta):
        consultas = self.leer_consultas()
        consultas.append(nueva_consulta)
        data = [c.to_dict() for c in consultas]
        self.guardar(data, indent_val=8)
        print("Consulta agregada con exito.")





    def eliminar_consultas_por_medico(self, id_medico):
        consultas = self.leer_consultas()
        
        consultas_a_mantener = [c for c in consultas if c.idmed != id_medico]
        consultas_eliminadas_count = len(consultas) - len(consultas_a_mantener)
        
        data = [c.to_dict() for c in consultas_a_mantener]
        self.guardar(data, indent_val=8)
        return consultas_eliminadas_count





    def actualizar_consulta_por_fecha(self, dia_original, mes_original, dia_nuevo, mes_nuevos):
        consultas = self.leer_consultas()
        consultas_actualizadas_count = 0
        
        mes_original = mes_original.lower().strip()
        mes_nuevo = mes_nuevo.lower().strip()

        for c in consultas:
            if c.dia == dia_original and c.mes == mes_original:
                c.dia = dia_nuevo
                c.mes = mes_nuevo
                consultas_actualizadas_count += 1
                
        if consultas_actualizadas_count > 0:
            data = [c.to_dict() for c in consultas]
            self.guardar(data, indent_val=8)
        
        return consultas_actualizadas_count






    def buscar_pacientes_por_fecha(self, dia, mes, anio):
        consultas = self.leer_consultas()
        mes = mes.lower().strip()
        pacientes = []
        
        for c in consultas:
            if c.dia == dia and c.mes == mes and c.anio == anio:
                pacientes.append(f"{c.nombrepaciente} {c.apellidopaciente} (CI: {c.ci})")
        
        return pacientes








def inicializar_archivos(pers_medico, pers_consulta):
  
    if not pers_medico._existe_y_no_vacio():
        medicos_iniciales = [
            medico(12344, "juan", "quispe", 6),
            medico(22034, "maria", "choque", 10),
            medico(12345, "guzman", "valeria", 14)
        ]
        data = [m.to_dict() for m in medicos_iniciales]
        pers_medico.guardar(data)
        print(f"-> Archivo '{pers_medico.archivo}' creado con 3 médicos por defecto.")

  
    if not pers_consulta._existe_y_no_vacio():
        consultas_iniciales = [
            consulta(918364,"juan","torrez", 12344,10,"enero",2014),
            consulta(10918050,"brayan","perez",22034,13,"febrero",2015),
            consulta(918362,"alverto","marquez", 12344,25,"diciembre",2014), 
            consulta(91833,"juan jose","torrez medrano", 12345,1,"enero",2015), 
            consulta(24564,"jorge","venavidez", 22034,15,"enero",2016),
            consulta(3345566,"julia","cortez", 12344,19,"mayo",2016),
            consulta(57693,"maria elena","fuceneco", 12345,20,"marzo",2017),
            consulta(1346743,"jaime","luque", 12345,28,"junio",2019),
            consulta(3029493,"mariano","aguilera",12345,20,"abril",2013)
        ]
        data = [c.to_dict() for c in consultas_iniciales]
        pers_consulta.guardar(data, indent_val=8)
        print(f"-> Archivo '{pers_consulta.archivo}' creado con 9 consultas .")




def main():
    persistencia_consultas = Persistencia("consulta.json")
    persistencia_medicos = Persistencia("medico.json")

    
    inicializar_archivos(persistencia_medicos, persistencia_consultas)

    while True:
        print("\n--- Menu Principal de Consultas Medicas ---")
        print("1. Agregar medico")
        print("2. Agregar consulta")
        print("3. Dar baja a medico (y sus consultas)")
        print("4. (Navidad/Ano Nuevo)")
        print("5. Mostrar pacientes atendidos en una fecha especifica")
        print("6. Salir")
        print("---------------------------------------------")
        opcion = input("Ingrese una opcion: ").strip()

        if opcion == "1":
            print("\n## Agregar Medico")
            try:
                idmed = int(input("Ingrese ID de medico: "))
                nombremed = input("Ingrese el nombre del medico nuevo: ")
                apellidomed = input("Ingrese el apellido del medico nuevo: ")
                aniosexperiencia = int(input("Ingrese los anos de experiencia: "))
                nuevo_medico = medico(idmed, nombremed, apellidomed, aniosexperiencia)
                persistencia_medicos.agregar_medico(nuevo_medico)
            except ValueError:
                print("Error: ID y anos de experiencia deben ser numeros.")

        elif opcion == "2":
            print("\n## Agregar Consulta")
            try:
                ci = int(input("Ingrese CI de paciente: "))
                nombrepaciente = input("Ingrese el nombre del paciente: ")
                apellidopaciente = input("Ingrese el apellido del paciente: ")
                idmed = int(input("Ingrese ID del medico designado: "))
                dia = int(input("Ingrese dia de consulta: "))
                mes = input("Ingrese el mes de consulta : ")
                anio = int(input("Ingrese el año de consulta: "))
                nueva_consulta = consulta(ci, nombrepaciente, apellidopaciente, idmed, dia, mes, anio)
                persistencia_consultas.agregar_consultas(nueva_consulta)
            except ValueError:
                print("Error: CI, ID del medico, dia y año deben ser numeros.")

        elif opcion == "3":
            print("\n## Dar Baja a Medico y Consultas")
            mednombre = input("Ingrese el nombre del medico a retirar: ")
            apmedico = input("Ingrese el apellido del medico a retirar: ")
            
           
            eliminado, id_medico = persistencia_medicos.eliminar_medico(mednombre, apmedico)
            
            if eliminado:
                print(f"Medico '{mednombre} {apmedico}' (ID: {id_medico}) dado de baja con exito.")
                
                
                consultas_eliminadas = persistencia_consultas.eliminar_consultas_por_medico(id_medico)
                print(f"Se eliminaron {consultas_eliminadas} consultas asociadas a ese medico.")
            else:
                print("No se encontro al medico con ese nombre y apellido.")

        elif opcion == "4":
            print("\n## Reagendar Dias Festivos")
            
           
            festivos = [
                (25, "diciembre", "Navidad"), 
                (1, "enero", "Ano Nuevo")
            ]
            
            consultas_actualizadas_total = 0
            
            for dia_orig, mes_orig, nombre_f in festivos:
              
                dia_nuevo = dia_orig + 1
                mes_nuevo = mes_orig
                anio_dummy = 0 

                
                actualizadas = persistencia_consultas.actualizar_consulta_por_fecha(dia_orig, mes_orig, anio_dummy, dia_nuevo, mes_nuevo, anio_dummy)
                
                if actualizadas > 0:
                    print(f"Se actualizaron {actualizadas} consultas del {nombre_f} ({dia_orig} de {mes_orig}).")
                    print(f"actualizadas para el {dia_nuevo} de {mes_nuevo} .")
                    consultas_actualizadas_total += actualizadas
            
            if consultas_actualizadas_total == 0:
                print("No se encontraron consultas en dias festivos (25 de Diciembre o 1 de Enero) para actualizar.")
                
        elif opcion == "5":
            print("\n## Pacientes Atendidos por Fecha")
            try:
                dia = int(input("Ingrese el dia: "))
                mes = input("Ingrese el mes: ")
                anio = int(input("Ingrese el año: "))
                
                pacientes = persistencia_consultas.buscar_pacientes_por_fecha(dia, mes, anio)
                
                print(f"\n--- Resultados para el {dia} de {mes} de {anio} ---")
                if pacientes:
                    print(f"Total de pacientes atendidos: *{len(pacientes)}*")
                    for p in pacientes:
                        print(f"  * {p}")
                else:
                    print("No se registraron consultas en esa fecha.")
                    
            except ValueError:
                print("Error: El dia y el año deben ser numeros.")

        elif opcion == "6":
            print("fin!")
            break
        else:
            print("Opcion incorrecta. Por favor, ingrese un numero del 1 al 6.")

if __name__ == "__main__":
  main()


import json
def grabar_consulta():
    consultas = [
        consulta(918364,"juan ","torrez", 12344,10,"enero",2014),
        consulta(10918050,"brayan","perez",22034,13,"febrero",2015),
        consulta(918362,"alverto ","marquez", 12344,25,"diciembre",2014),
        consulta(91833,"juan jose ","torrez medrano", 12345,1,"enero",2015),
        consulta(24564,"jorge ","venavidez", 22034,15,"enero",2016),
        consulta(3345566,"julia ","cortez", 12344,19,"mayo",2016),
        consulta(57693,"maria elena","fuceneco", 12345,20,"marzo",2017),
        consulta(1346743,"jaime ","luque", 12345,28,"junio",2019),
        consulta(3029493,"mariano","aguilera",12345,20,"abril",2013)
    ]
    data = [consulta.to_dict() for consulta in consultas]

    with open("consulta.json", "w") as archivo:
        json.dump(data, archivo, indent=8)

if __name__ == "__main__":
    grabar_consulta()

def grabar_medico():
    medicos = [
        medico(12344,"juan","quispe",6),
        medico(22034,"maria","choque",10),
        medico(12345,"guzman","valeria",14)
    ]
    data = [medico.to_dict() for medico in medicos]

    with open("medico.json","w") as archivo:
        json.dump(data, archivo, indent=5)
if __name__ == "__main__":
    grabar_medico()





def leer_consultas():
    try:
        with open("consulta.json", "r") as archivo:
            data = json.load(archivo)
            consultas = [consulta.from_dict(consultas) for consulta in data]
            for consulta in consultas:
                print(f"ci: {consulta.ci}")
                print(f"nombrepaciente: {consulta.nombrepaciente}")
                print(f"apellidopaciente: {consulta.apellidopaciente}")
                print(f"idmed: {consulta.idmed}")
                print(f"dia: {consulta.dia}")
                print(f"mes: {consulta.mes}")
                print(f"anio: {consulta.anio}")
                print("------------------------")
    except FileNotFoundError:
        print("El archivo consulta.json no existe.")

if __name__ == "__main__":
    leer_consultas()

def leer_medicos():
    try:
        with open ("medico.json","r") as archivo:
            data = json.load(archivo)
            medicos = [medico.from_dict(medicos) for medico in data]
            for medico in medicos:
                print(f"idmed: {medico.idmed}")
                print(f"nombremed: {medico.nombremed}")
                print(f"apellidomed: {medico.apellidomed}")
                print(f"aniosexperiencia: {medico.aniosexperiencia}")
                print("------------------------")
    except FileNotFoundError:
        print("El archivo medico.json no existe.")

if __name__ == "__main__":
    leer_medicos()    

class consulta:
    def __init__(self, ci, nombrepaciente, apellidopaciente,idmed,dia,mes,anio):
        self.ci = ci
        self.nombrepaciente = nombrepaciente
        self.apellidopaciente = apellidopaciente
        self.idmed = idmed
        self.dia = dia
        self.mes = mes
        self.anio = anio 

    def to_dict(self):
        return {
            "ci": self.ci,
            "nombrepaciente": self.nombrepaciente,
            "apellidopaciente": self.apellidopaciente,
            "idmed" : self.idmed,
            "dia" : self.dia,
            "mes" : self.mes,
            "anio" : self.anio
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["ci"], data["nombrepaciente"], data["apellidopaciente"],data["idmed"],data["dia"],data["mes"],data["anio"])
class medico:
    def __init__(self,idmed,nombremed,apellidomed,aniosexperiencia):
        self.idmed = idmed
        self.nombremed = nombremed
        self.apellidomed = apellidomed
        self.aniosexperiencia = aniosexperiencia

    def to_dict(self):
        return {
            "idmed" : self.idmed,
            "nombremed" : self.nombremed,
            "apellidomed" : self.apellidomed,
            "aniosexperiencia" : self.aniosexperiencia
        }    
    @classmethod
    def form_dict(cls,data):
        return cls(data["idmed"],data["nombremed"],data["apellidomed"],data["aniosexperiencia"])

class Persistencia:
    def __init__(self, archivo):
        self.archivo = archivo

    def guardar_consultas(self, consulta):
        data = [consulta.to_dict() for consulta in consulta]
        with open(self.archivo, "w") as archivo:
            json.dump(data, archivo, indent=8)

    def guardar_medicos(self,medico):
        data = [medico.to_dict() for medico in medico]
        with open(self.archivo, "w") as archivo:
            json.dump(data,archivo,indent=5)        

    def leer_consultas(self):
        try:
            with open(self.archivo, "r") as archivo:
                data = json.load(archivo)
                return [consulta.from_dict(consulta) for consulta in data]
        except FileNotFoundError:
            return []

    def leer_medicos(self):
        try:
             with open(self.archivo, "r") as archivo:
                data = json.load(archivo)
                return [medico.from_dict(medico) for medico in data]
        except FileNotFoundError:
            return []   

    def agregar_consultas(self, consulta):
        consultas = self.leer_consulta()
        consultas.append(consulta)
        self.guardar_consultas(consultas)

    def agregar_medicos(self,medico):
        medicos = self.leer_medico()
        medicos.append(medico)
        self.guardar_medicos(medicos)    

    def actualizar_consulta(self, ci, nueva_consulta):
        consulta = self.leer_consultas()
        for i, consulta in enumerate(consulta):
            if consulta.ci == ci:
                consulta[i] = nueva_consulta
                self.guardar_consulta(consulta)
                return True
        return False
    def eliminar_medico(self,nombremed,apellidomed):
        medicos = self.leer_medico()
        medicos = [medico for medico in medicos if medico.nombremed != nombremed and medico.apellidomed != apellidomed]
        self.guardar_medicos(medicos)

def main():
    persistencia = Persistencia("consulta.json")
    persistencia = Persistencia("medico.json")

    while True:
        print("1. agregar medico ")
        print("2. agregar consulta")
        print("3. dar baja medico")
        print("4. dias festivos")
        print("5. pacientes atendidos ")
        print("6. Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            idmed = int(input("ingrese id de medico: "))
            nombremed = input("Ingrese el nombre del medico nuevo: ")
            apellidomed = input("Ingrese el apellido del medico nuevo: ")
            aniosexperiencia = int(input("Ingrese los años de experiencia: "))
            medico = medico(idmed, nombremed, apellidomed,aniosexperiencia)
            persistencia.agregar_medico(medico)
        elif opcion == "2":
            ci = int(input("ingrese ci de paciente: "))
            nombrepaciente = input("Ingrese el nombre del paciente: ")
            apellidopaciente = input("Ingrese el apellido del paciente: ")
            dia = int(input("Ingrese dia de consulta: "))
            mes = input("ingrese el mes de consulta: ")
            anio = int(input("ingrese el año de consulta: "))
            consulta = consulta(ci, nombrepaciente, apellidopaciente,dia,mes,anio)
            persistencia.agregar_consultas(consulta)
        elif opcion == "3":
            mednombre = input("Ingrese el nombre de medico a retirar: ")
            apmedico = input("Ingrese el apellido de medico a retirar: ")
            if persistencia.eliminar_medico(mednombre, apmedico):
                print("medico dado de baja con éxito")
            else:
                print("No se encontró al medico")

        elif opcion == "4":
            navidad = 25
            dianuevo = 1
            mesnuevo = "enero"
            festividad = consulta(navidad, dianuevo, mesnuevo)
            if persistencia.actualizar_consulta(navidad,festividad):
                print("consulta actualizada")
            else:
                print("No se encontró fechas festivas")   


        elif opcion == "6":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()

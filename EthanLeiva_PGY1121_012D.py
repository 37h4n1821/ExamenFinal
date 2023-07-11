from datetime import datetime

now = datetime.now()
class Error_proporcional(Exception):
    "Error el valor de asistentes es inferior a 60"
    pass

def validar_rut(rut_a_validar:str,limite:int=9000000000000000,largo_min:int=3):
    """
Funcion que recibe como parametro obligatorio:
    -rut_a_validar en formato xx.xxx.xxx-x o xxxxxxxx-x o xxxxxxxxx
    Parametro opcionales:
    -limite para establecer el limite numerico de rut
    -largomin para establecer el largo minimo de un rut
    """
    conver={1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'K',11:'0'}
    rut_a_validar=rut_a_validar.replace("-","").replace(".","").replace(",","").upper()
    if len(rut_a_validar)<largo_min:
        return (False,f"No ingreso un rut de longitud valida: {largo_min} de largo minimo",None)
    run=rut_a_validar[:-1]
    div=rut_a_validar[-1]
    if (not run.isnumeric()) or (not div.isalnum()):
        return (False,"Valores ingresados invalidos",None)
    if int(run)>limite:
        return (False,f"Rut fuera del limite {limite}!",None)
    run2=[int(i) for i in run]
    i=0
    val=[2,3,4,5,6,7]
    suma=0
    for i3 in run2[::-1]:
        if i==len(val):
            i=0
        suma+=i3*val[i]
        i+=1
    val=11-suma%11
    if (div==conver[val]):
        rut=int(run)
        return (True,"Rut valido",rut)
    else:
        return (False,"Rut invaldio",None)


def calcular_proporcion(n:int)->int:
    for a in range(5,n//2):
        for h in range(10,n//5,2):
            if (a*h==n):
                return (h,a)
    return  None

class Concierto():
    def __init__(self,nombre:str,Asistentes:int,Precios=dict()) -> None:
        self.nombre=nombre
        self.Asistentes=Asistentes
        self.razon_proporcionAsientos=calcular_proporcion(Asistentes)
        self.ventas=[]
        if not self.razon_proporcionAsientos:
            raise Error_proporcional
        self.Asientos=[]
        actual=1
        for alto in range(self.razon_proporcionAsientos[0]):
            self.Asientos.append([])
            for ancho in range(self.razon_proporcionAsientos[1]):
                self.Asientos[-1].append({f"{actual:03d}":[None,None,None]}if actual <= self.Asistentes else {"___":[None,None,None]})
                actual+=1
        
        self.Precios=Precios

        for llave in self.Precios.keys():
            for valor in range(self.Precios[llave][1],self.Precios[llave][2]+1):
                for alto in range(self.razon_proporcionAsientos[0]):
                    for ancho in range(self.razon_proporcionAsientos[1]):
                        try:
                            if int(list(self.Asientos[alto][ancho].keys())[0]) == valor:
                                self.Asientos[alto][ancho][list(self.Asientos[alto][ancho].keys())[0]][1]=llave
                                self.Asientos[alto][ancho][list(self.Asientos[alto][ancho].keys())[0]][2]=self.Precios[llave][0]
                        except:
                            continue


    
    def imprimir(self)->None:
        print(f"\tPlano Concierto: {self.nombre}")
        for alto in range(self.razon_proporcionAsientos[0]):
            for ancho in range(self.razon_proporcionAsientos[1]):
                print(f"[{list(self.Asientos[alto][ancho].keys())[0]}] " if not self.Asientos[alto][ancho][list(self.Asientos[alto][ancho].keys())[0]][0] else "[ X ] ",end="")
            print()

    def check_asiento(self,asiento:str)->tuple:
        for alto in range(self.razon_proporcionAsientos[0]):
            for ancho in range(self.razon_proporcionAsientos[1]):
                if asiento in list(self.Asientos[alto][ancho].keys()) and not self.Asientos[alto][ancho][asiento][0]:
                    return (True,self.Asientos[alto][ancho][asiento][1],self.Asientos[alto][ancho][asiento][2])
        return (False,None,None)

    def comprar_asiento(self, asiento:str,rut:str)->bool:
        for alto in range(self.razon_proporcionAsientos[0]):
            for ancho in range(self.razon_proporcionAsientos[1]):
                if asiento in list(self.Asientos[alto][ancho].keys()) and not self.Asientos[alto][ancho][asiento][0]:
                    self.Asientos[alto][ancho][asiento][0]=rut
                    self.ventas.append(rut)
                    return True
        return False
    
    def anular_asiento(self,rut:str)->bool:
        for alto in range(self.razon_proporcionAsientos[0]):
            for ancho in range(self.razon_proporcionAsientos[1]):
                asiento=list(self.Asientos[alto][ancho].keys())[0]
                if self.Asientos[alto][ancho][asiento][0] and self.Asientos[alto][ancho][asiento][0]==rut:
                    self.Asientos[alto][ancho][asiento][0]=None
                    self.ventas.remove(rut)
                    return True
        return False
    
    def informacion_compradores(self)->dict:
        ventas_={}
        for i in self.Precios.keys():
            ventas_[i]=0
        
        for rut in self.ventas:
            for alto in range(self.razon_proporcionAsientos[0]):
                for ancho in range(self.razon_proporcionAsientos[1]):
                    asiento=list(self.Asientos[alto][ancho].keys())[0]
                    if self.Asientos[alto][ancho][asiento][0] and self.Asientos[alto][ancho][asiento][0]==rut:
                        ventas_[self.Asientos[alto][ancho][asiento][1]]+=1

        return (ventas_,self.Precios)
    
    def dev(self):
        print((self.Asientos))


def comprar_asiento(concierto:Concierto)->bool:
    while True:
        try:
            cant_entradas=int(input("Ingrese cantidad de asientos a comprar: "))
        except:
            print("Valor ingresado invalido!")
            continue
        if cant_entradas<1:
            print("cantidad ingresada nula o negativa!")
        elif cant_entradas>3:
            print("Cantidad de entradas excede el limite de ventas permitido, solo se pueden vender de 1 a 3 entradas")
        else:
            break
    concierto.imprimir()
    venta=[]
    for i in range(cant_entradas):
        print(f"Indique rut asistente N°{i+1}")
        while True:
            estado,mensaje,rut=validar_rut(input("Ingrese su rut: "))
            if estado:
                if not rut in concierto.ventas:
                    break
                else:
                    print("Este rut ya cuenta con una entrada vendida!")
            else:
                print(mensaje)
    
        while True:
            try:
                asiento=f"{int(input('Indique asiento a comprar: ')):03d}"
            except:
                print("Valor ingresado invalido!")
                continue
            estado,tipo,precio=concierto.check_asiento(asiento)
            if estado:
                break
            else:
                print("No está disponible")
        concierto.comprar_asiento(asiento=asiento,rut=rut)
        venta.append([rut,asiento,tipo,precio])
        concierto.imprimir()
    
    print("Información de venta:")
    total=0
    for i in venta:
        print(f"Rut:{i[0]} Asiento:{i[1]} Tipo:{i[2]} Precio:${i[3]}")
        total+=i[3]
    print(f"Total a pagar: ${total}")
    while True:
        try:
            conf=input('Confirmar compra Si No \n>')
        except:
            print("Valor ingresado invalido!")
            continue
        if conf=="Si" or conf =="No":
            break
        else:
            print("Opcion ingresada invalida")
    
    if conf=="Si":
        return True
    else:
        for i in venta:
            concierto.anular_asiento(i[0])
        return False


def listado_asistente(concierto:Concierto):
    c=1
    for asistente in sorted(concierto.ventas):
        print(f"{c}-{asistente}")
        c+=1

def ganancias_totales(concierto:Concierto):
    ventas=concierto.informacion_compradores()

    vent_t=0
    vent_t2=0
    print("Tipo      | Valor     | Cantidad | Total")
    for tipo in ventas[0].keys():
        vent_t+=ventas[0][tipo]
        vent_t2+=ventas[0][tipo]*ventas[1][tipo][0]

        if (ventas[0][tipo]==0):
            continue
        print(f"{str(tipo):10s}|${str(ventas[1][tipo][0]):10s}",end="")
        print(f"|{str(ventas[0][tipo]):10s}",end="")
        print(f"|${str(ventas[0][tipo]*ventas[1][tipo][0]):10s}",end="")
        
        print()
    print(f"Total\t\t      |{str(vent_t):10s}|${str(vent_t2):20s}")
    



concierto=Concierto("Michael Jam",100,{"Platinum":[120000,1,20],"Gold":[80000,21,50],"Silver":[50000,51,100]})

while True:
    try:
        op=int(input(f"Menú Concierto: {concierto.nombre}\n1)Comprar Entradas\n2)Mostrar ubicaciones disponibles\n3)Ver listado asistentes\n4)Mostrar Ganancias totales\n5)Salir\n>"))
    except:
        print("Valor ingresado invalido!")
        continue
        
    if (op==5):
        print("Hasta luego!\nMuchas gracias por utilizar Ethan's system compra\nDesarrollador: Ethan Leiva\nFecha de hoy:",now.strftime("%d/%m/%Y"))
        break
    elif (op==1):
        if comprar_asiento(concierto):
            print("Compra realizada con exito!")
        else:
            print("Compra no realizada")
    elif (op==2):
        concierto.imprimir()
    elif (op==3):
        listado_asistente(concierto=concierto)
    elif (op==4):
        ganancias_totales(concierto=concierto)
import pandas as pd, PyPDF2, re, os

#funciones
def extraer_archivos(dir_path):
    result = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            if(path.split(".")[-1] == "pdf"):
                result.append(dir_path + "/" + path)
    return result


def extraer_vistas(views_path, columna):
    views = []
    for path in os.listdir(views_path):
        if os.path.isfile(os.path.join(views_path, path)):
            if(path.split(".")[-1] == 'csv'):
                df = pd.read_csv(os.path.join(views_path, path), delimiter=';')
                views += list(df['VIEW_NAME'].values)
    return views



def extraer_vistas(views_path, columna):
    views = []
    for path in os.listdir(views_path):
        if os.path.isfile(os.path.join(views_path, path)):
            if(path.split(".")[-1] == 'csv'):
                df = pd.read_csv(os.path.join(views_path, path), delimiter=';')
                views += list(df['VIEW_NAME'].values)
    return views

def extraer_vistas_archivo(archivo):
    with open(archivo, "r") as file:
        return file.readlines()

#estas son solo para facilitar la lectura y quitarnos de close y tonterías.

def escribir(archivo, texto):
    with open(archivo, 'w+') as f:
        f.write(texto)


def añadir(archivo, texto):
    with open(archivo, 'a+') as f:
        f.write(texto)


# main


#recomendamos poner en directorio la ruta absoluta de la carpeta contenedora del main
directorio = '.'

directorio_pdf=directorio+'nuevos/'
directorio_vistas = directorio+'vistas/'
directorio_logs = directorio+'logs/'


columna='VIEW_NAME'
rutas = extraer_archivos(directorio_pdf)
views = extraer_vistas(directorio_vistas, 'VIEW_NAME')


# extra para una prueba
views = extraer_vistas_archivo(directorio_vistas+'hoja_nueva2.txt')
####

views = list(map(lambda x: x.rstrip(), views))




log_path = directorio_logs+"log.txt"
resultados = directorio_logs+"resultados.txt"
ya_acabado = directorio_logs+"acabados.txt"

for pdf in rutas:
    pdfObject=open(pdf, 'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfObject)
    pdfReader.strict = False
    for j, view in enumerate(views):
        i = 0
        encontrado = False
        while i < pdfReader.getNumPages() and encontrado == False:
            mensaje_exito = "Encontrada vista " + view + " en pagina " + str(i) + " de archivo " + pdf.split("/")[-1] + "\n"
            mensaje_fracaso = "\n"+"NO "+str(j)+" : "+view+" en "+pdf.split("/")[-1]+"\n"
            Text = pdfReader.getPage(i).extractText()
            ResSearch = re.search(view, Text)          
            if ResSearch != None:
                añadir(resultados, mensaje_exito)
                añadir(log_path, mensaje_exito) 
                print(mensaje_exito)
                encontrado = True
            i = i+1
        if (encontrado == False):
            añadir(log_path, mensaje_fracaso)
            print(mensaje_fracaso)
            
        




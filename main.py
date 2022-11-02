import pandas as pd, PyPDF2, re, os

#funciones
def extraer_archivos(dir_path):
    result = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            if(path.split(".")[-1] == "pdf"):
                result.append(dir_path + "/" + path)
    return result


#esta funcion busca extraer la lista de palabras a buscar como una lista. Ya como a cada uno
#le haga falta sacarlos. en nuestro caso era a partir de un dataframe sacado de un csv.


def extraer_vistas(views_path):
    df = pd.read_csv(views_path+'views_limpio.csv', delimiter=';')
    df2 = pd.read_csv(views_path+'mviews_limpio.csv', delimiter=';')

    views = list(df['VIEW_NAME'].values) + list(df2["VIEW_NAME"].values)
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


rutas = extraer_archivos(directorio_pdf)
views = extraer_vistas(directorio_vistas)


# extra para una prueba
views = extraer_vistas_archivo(directorio_vistas+'hoja_nueva.txt')
####

views = list(map(lambda x: x.rstrip(), views))

views.remove('')


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
            
        




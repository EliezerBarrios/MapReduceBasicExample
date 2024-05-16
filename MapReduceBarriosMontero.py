from functools import reduce

def descargar_contenido(url):

  import requests
  response = requests.get(url)
  if response.status_code == 200:
    return response.text
  else:
    raise Exception(f"Error al descargar la URL: {url}")

def eliminar_etiquetas_html(contenido):
    import re
    contenido_sin_etiquetas = re.sub(r"<[^>]+?(?: class=[\w']+|' id=[\w']+)?>", "", contenido)

    return contenido_sin_etiquetas

def eliminar_scripts_comentarios(contenido):

  import re
  return re.sub(r"<script[^>]*?>.*?</script>", "", contenido) + re.sub(r"", "", contenido)

def convertir_entidades_html(contenido):

  import html
  return html.unescape(contenido)

def eliminar_caracteres_especiales(contenido):

  import re
  return re.sub(r"[^\w\s]", "", contenido)

def normalizar_espacios_en_blanco(contenido):

  import re
  return re.sub(r"\s+", " ", contenido)

def procesar_contenido(contenido):

  contenido_sin_html = eliminar_etiquetas_html(contenido)
  contenido_sin_scripts_comentarios = eliminar_scripts_comentarios(contenido_sin_html)
  contenido_con_entidades_convertidas = convertir_entidades_html(contenido_sin_scripts_comentarios)
  contenido_sin_caracteres_especiales = eliminar_caracteres_especiales(contenido_con_entidades_convertidas)
  contenido_final = normalizar_espacios_en_blanco(contenido_sin_caracteres_especiales)
  return contenido_final

def reducer(contenido1, contenido2):
  # Crear un diccionario para almacenar el conteo de palabras
  conteo_palabras = {}

  # Procesar el contenido 1
  for palabra in contenido1.split():
    if palabra in conteo_palabras:
      conteo_palabras[palabra] += 1
    else:
      conteo_palabras[palabra] = 1

  # Procesar el contenido 2
  for palabra in contenido2.split():
    if palabra in conteo_palabras:
      conteo_palabras[palabra] += 1
    else:
      conteo_palabras[palabra] = 1

  # Generar el resultado formateado
  resultado = ""
  for palabra, conteo in conteo_palabras.items():
    resultado += f"{palabra}: {conteo}\n"

  return resultado


def main():
  """
  Función principal del programa.
  """
  # Leer las URLs del archivo txt
  with open("urls.txt", "r") as archivo:
    urls = archivo.readlines()

  contenido_procesado = list(map(procesar_contenido, map(descargar_contenido, urls)))

  contenido_final = reduce(reducer, contenido_procesado)

  print(contenido_final)

  # Guardar el contenido final en un archivo txt
  with open("resultado.txt", "w") as archivo_salida:
    archivo_salida.write(contenido_final)


if __name__ == "__main__":
  main()

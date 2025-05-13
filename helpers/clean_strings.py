import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup


def download_nltk_resource(resource_name, resource_path):
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(resource_name)

# Descargar recursos necesarios (solo si no están presentes)
download_nltk_resource('punkt_tab', 'tokenizers/punkt_tab')
download_nltk_resource('punkt', 'tokenizers/punkt')
download_nltk_resource('stopwords', 'corpora/stopwords')
download_nltk_resource('wordnet', 'corpora/wordnet')
download_nltk_resource('omw-1.4', 'corpora/omw-1.4')


def limpiar_texto(texto):
    """
    Realiza una limpieza profunda del texto para preparación en vectorización en modelos RAG.
    :param texto: Cadena de texto a limpiar.
    :param eliminar_numeros: Booleano para decidir si eliminar los números o no.
    :return: Texto limpio listo para vectorizar.
    """
    # 1. Eliminar etiquetas HTML si las hay
    try:
        texto = BeautifulSoup(texto, "html.parser").get_text()
    except Exception as e:
        print(e)

    # 3. Convertir a minúsculas
    texto = texto.lower()

    # 2. Normalizar caracteres Unicode (quita tildes, diacríticos, etc.)
    texto = ''.join((c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn'))

    # 4. Eliminar signos de puntuación
    texto = re.sub(r'[^\w\s]', ' ', texto)

    return texto


# Ejemplo de uso:
# texto_prueba = "<p>Esto es un ejemplo de texto con HTML, números 123 y palabras innecesarias.</p>"
# print(limpiar_texto(texto_prueba))

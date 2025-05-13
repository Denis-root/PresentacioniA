from pathlib import Path

def encontrar_txt(path_base):
    path = Path(path_base)
    for archivo in path.rglob("*.txt"):
        if archivo.is_file():
            yield archivo

def leer_txt(path_base):
    path = Path(path_base)
    for archivo in path.rglob("*.txt"):
        if archivo.is_file():
            with archivo.open("r", encoding="utf-8") as f:
                contenido = f.read()
                yield archivo, contenido
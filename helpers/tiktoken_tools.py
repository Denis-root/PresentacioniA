from icecream import ic
import tiktoken


def contar_tokens(cadena: str, modelo: str = "gpt-4o-mini") -> int:
    """
    Calcula y retorna el número de tokens para una cadena dada utilizando el modelo especificado.

    Args:
        cadena (str): El texto para calcular el número de tokens.
        modelo (str): El modelo a usar para el tokenizador (por defecto "gpt-4").

    Returns:
        int: El número de tokens en la cadena.
    """
    try:
        # Obtén el codificador basado en el modelo
        encoding = tiktoken.encoding_for_model(modelo)
        # Codifica la cadena y cuenta los tokens
        tokens = encoding.encode(cadena)
        return len(tokens)
    except KeyError:
        raise ValueError(f"Modelo '{modelo}' no soportado por tiktoken.")


# ic(contar_tokens('dime mamamona que tu quieres'))
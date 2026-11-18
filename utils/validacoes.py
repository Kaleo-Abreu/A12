def vazio(valor):
    """Indica se o valor é nulo ou está em branco."""
    return valor is None or str(valor).strip() == ""


def inteiro_convertido(valor):
    """Converte o valor em inteiro ou retorna None quando não for possível."""
    if vazio(valor):
        return None

    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def texto_valido(valor, minimo=1):
    """Indica se o texto preenchido possui o tamanho mínimo exigido."""
    if vazio(valor):
        return False

    return len(str(valor).strip()) >= minimo

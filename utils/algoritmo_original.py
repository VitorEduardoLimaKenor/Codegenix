

def maior_valor(lista):
    """Encontra o maior valor em uma lista."""
    if not lista:
        return None
    maior = lista[0]
    for valor in lista:
        if valor > maior:
            maior = valor
    return maior


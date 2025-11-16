def counting_sort(lista_de_dicionarios, id):
    if not lista_de_dicionarios:
        return []

    max = 0
    for item in lista_de_dicionarios:
        if item[id] > max:
            max = item[id]
    
    tamanho_lista = len(lista_de_dicionarios)
    count = [0] * (max + 1)
    lista_ordenada = []

    for i in range(tamanho_lista):
        elemento = lista_de_dicionarios[i]
        valor_chave = elemento[id]
        count[valor_chave] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    i = tamanho_lista - 1
    while i >= 0:
        elemento = lista_de_dicionarios[i]
        valor_chave = elemento[id]
        
        posicao_saida = count[valor_chave] - 1
        lista_ordenada[posicao_saida] = elemento
        count[valor_chave] -= 1
        i -= 1

    return lista_ordenada

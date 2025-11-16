import json
import os
from ordenacao import counting_sort

pedidos_ativos = []
pedidos_finalizados = []
todos_os_pedidos = []
itens = []

proximo_codigo_item = 1
proximo_codigo_pedido = 1

pedido_aguardando_aprovacao = []
pedido_aceito = []
pedido_fazendo = []
pedido_feito = []
pedido_esperando_entregador = []
pedido_saiu_entrega = []
pedido_entregue = []
pedido_rejeitado = []
pedido_cancelado = []

NOME_ARQUIVO = "dados_pedidos.json"

def salvar_dados():
    dados = {
        "itens": itens,
        "todos_os_pedidos": todos_os_pedidos,
        "proximo_codigo_item": proximo_codigo_item,
        "proximo_codigo_pedido": proximo_codigo_pedido
    }
    try:
        with open(NOME_ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar dados: {e}")

def carregar_dados():
    global itens, todos_os_pedidos, proximo_codigo_item, proximo_codigo_pedido
    global pedidos_ativos, pedidos_finalizados, pedido_aguardando_aprovacao
    global pedido_aceito, pedido_fazendo, pedido_feito, pedido_esperando_entregador
    global pedido_saiu_entrega, pedido_entregue, pedido_rejeitado, pedido_cancelado

    if not os.path.exists(NOME_ARQUIVO):
        print("Arquivo não encontrado")
        return

    try:
        with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
            if os.path.getsize(NOME_ARQUIVO) == 0:
                print("Arquivo de dados vazio")
                return
            dados = json.load(f)

        itens = dados.get('itens', [])
        todos_os_pedidos = dados.get('todos_os_pedidos', [])
        proximo_codigo_item = dados.get('proximo_codigo_item', 1)
        proximo_codigo_pedido = dados.get('proximo_codigo_pedido', 1)

        pedidos_ativos = []
        pedidos_finalizados = []
        pedido_aguardando_aprovacao = []
        pedido_aceito = []
        pedido_fazendo = []
        pedido_feito = []
        pedido_esperando_entregador = []
        pedido_saiu_entrega = []
        pedido_entregue = []
        pedido_rejeitado = []
        pedido_cancelado = []

        for pedido in todos_os_pedidos:
            status = pedido.get('status')
            if status == "AGUARDANDO APROVACAO":
                pedido_aguardando_aprovacao.append(pedido)
                pedidos_ativos.append(pedido)
            elif status == "ACEITO":
                pedido_aceito.append(pedido)
                pedidos_ativos.append(pedido)
            elif status == "FAZENDO":
                pedido_fazendo.append(pedido)
                pedidos_ativos.append(pedido)
            elif status == "FEITO":
                pedido_feito.append(pedido)
                pedidos_ativos.append(pedido)
            elif status == "ESPERANDO ENTREGADOR":
                pedido_esperando_entregador.append(pedido)
                pedidos_ativos.append(pedido)
            elif status == "SAIU PARA ENTREGA":
                pedido_saiu_entrega.append(pedido)
                pedidos_ativos.append(pedido)
            elif status == "ENTREGUE":
                pedido_entregue.append(pedido)
                pedidos_finalizados.append(pedido)
            elif status == "CANCELADO":
                pedido_cancelado.append(pedido)
                pedidos_finalizados.append(pedido)
            elif status == "REJEITADO":
                pedido_rejeitado.append(pedido)
                pedidos_finalizados.append(pedido)
        
        print("Dados carregados com sucesso.")

    except:
        print("Erro ao carregar dados")

def cadastrar_item():
    nome = input("Nome do item: ").strip()
    if not nome:
        print("Nome do item não pode estar vazio!")
        return None
    
    descricao = input("Descrição do item: ").strip()
    
    while True:
        try:
            preco = float(input("Preço do item: R$ "))
            if preco < 0:
                print("O preço não pode ser negativo!")
                continue
            break
        except ValueError:
            print("Por favor, insira um valor numérico válido!")
    
    while True:
        try:
            quantidade_estoque = int(input("Quantidade em estoque: "))
            if quantidade_estoque < 0:
                print("A quantidade não pode ser negativa!")
                continue
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido!")

    global proximo_codigo_item
    
    produto = {
        "codigo": proximo_codigo_item,
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "estoque": quantidade_estoque
    }
    
    itens.append(produto)
    proximo_codigo_item += 1
    
    print(f"\nItem '{produto['nome']}' cadastrado com sucesso!")
    print(f"Código atribuído: {produto['codigo']}")
    salvar_dados()
    return produto

def modificar_itens():
    if not itens:
        print("Nenhum item cadastrado no sistema.")
        return
    
    print("\n--- Itens Cadastrados ---")
    for item in itens:
        print(f"[{item['codigo']}] {item['nome']} - R$ {item['preco']:.2f} | Estoque: {item['estoque']} | {item['descricao']}")
    
    try:
        codigo = int(input("\nDigite o código do item que deseja modificar: "))
    except ValueError:
        print("Código inválido!")
        return
    
    item_encontrado = None
    for item in itens:
        if item['codigo'] == codigo:
            item_encontrado = item
            break
    
    if not item_encontrado:
        print("Item não encontrado!")
        return
    
    print(f"\nModificando: {item_encontrado['nome']}")
    
    novo_nome = input(f"Novo nome (atual: '{item_encontrado['nome']}'): ").strip()
    if novo_nome:
        item_encontrado['nome'] = novo_nome
    
    novo_preco = input(f"Novo preço (atual: R$ {item_encontrado['preco']:.2f}): ").strip()
    if novo_preco:
        try:
            preco_float = float(novo_preco)
            if preco_float >= 0:
                item_encontrado['preco'] = preco_float
            else:
                print("Preço não pode ser negativo. Valor mantido.")
        except ValueError:
            print("Preço inválido. Valor mantido.")
    
    nova_descricao = input(f"Nova descrição (atual: '{item_encontrado['descricao']}'): ").strip()
    if nova_descricao:
        item_encontrado['descricao'] = nova_descricao
    
    nova_quantidade = input(f"Nova quantidade (atual: {item_encontrado['estoque']}): ").strip()
    if nova_quantidade:
        try:
            quantidade_int = int(nova_quantidade)
            if quantidade_int >= 0:
                item_encontrado['estoque'] = quantidade_int
            else:
                print("Quantidade não pode ser negativa. Valor mantido.")
        except ValueError:
            print("Quantidade inválida. Valor mantido.")

    print(f"\nItem atualizado com sucesso!")
    salvar_dados()

def consultar_itens():
    if not itens:
        print("Nenhum item cadastrado no sistema.")
        return
    
    print("\n--- Catálogo de Itens ---")
    for item in itens:
        estoque_info = f"Estoque: {item['estoque']}" if item['estoque'] > 0 else "SEM ESTOQUE"
        print(f"[{item['codigo']}] {item['nome']} - R$ {item['preco']:.2f}")
        print(f"    Descrição: {item['descricao']}")
        print(f"    {estoque_info}")
        print("-" * 40)

def criar_pedido():
    if not itens:
        print("Não há itens cadastrados. Cadastre itens antes de criar pedidos.")
        return

    global proximo_codigo_pedido
    
    pedido_itens = []
    valor_total = 0.0
    
    print("\n--- Criar Novo Pedido ---")
    print("Itens disponíveis:")
    
    itens_disponiveis = [item for item in itens if item['estoque'] > 0]
    if not itens_disponiveis:
        print("Nenhum item disponível em estoque!")
        return
    
    for item in itens_disponiveis:
        print(f"[{item['codigo']}] {item['nome']} - R$ {item['preco']:.2f} (Estoque: {item['estoque']})")

    while True:
        entrada = input("\nDigite o código do item (ou 'fim' para finalizar): ").strip()
        
        if entrada.lower() == 'fim':
            break
            
        try:
            codigo = int(entrada)
        except ValueError:
            print("Código inválido!")
            continue
        
        item_escolhido = None
        for item in itens:
            if item['codigo'] == codigo:
                item_escolhido = item
                break
        
        if not item_escolhido:
            print("Item não encontrado!")
            continue
            
        if item_escolhido['estoque'] <= 0:
            print(f"Item '{item_escolhido['nome']}' está sem estoque!")
            continue
        
        while True:
            try:
                quantidade = int(input(f"Quantidade de '{item_escolhido['nome']}' (máx: {item_escolhido['estoque']}): "))
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero!")
                    continue
                elif quantidade > item_escolhido['estoque']:
                    print(f"Estoque insuficiente! Máximo disponível: {item_escolhido['estoque']}")
                    continue
                break
            except ValueError:
                print("Quantidade inválida!")
        
        subtotal = item_escolhido['preco'] * quantidade
        valor_total += subtotal
        
        item_pedido = {
            "codigo_produto": codigo,
            "nome_produto": item_escolhido['nome'],
            "quantidade": quantidade,
            "subtotal": subtotal
        }
        pedido_itens.append(item_pedido)
        
        item_escolhido['estoque'] -= quantidade
        
        print(f"Adicionado: {quantidade}x {item_escolhido['nome']} = R$ {subtotal:.2f}")

    if not pedido_itens:
        print("Pedido cancelado - nenhum item foi adicionado.")
        return

    valor_com_desconto = valor_total
    cupom_aplicado = ""
    
    cupom = input("\nCupom de desconto (DESCONTO10, DESCONTO20 ou deixe vazio): ").strip().upper()
    
    if cupom == "DESCONTO10":
        valor_com_desconto = valor_total * 0.9
        cupom_aplicado = cupom
        print("Cupom DESCONTO10 aplicado - 10% de desconto!")
    elif cupom == "DESCONTO20":
        valor_com_desconto = valor_total * 0.8
        cupom_aplicado = cupom
        print("Cupom DESCONTO20 aplicado - 20% de desconto!")
    elif cupom and cupom not in ["DESCONTO10", "DESCONTO20"]:
        print("Cupom inválido - pedido criado sem desconto.")

    pedido = {
        "codigo": proximo_codigo_pedido,
        "itens_do_pedido": pedido_itens,
        "valor_final": valor_com_desconto,
        "cupom": cupom_aplicado,
        "status": "AGUARDANDO APROVACAO"
    }
    
    pedidos_ativos.append(pedido)
    todos_os_pedidos.append(pedido)
    pedido_aguardando_aprovacao.append(pedido)
    proximo_codigo_pedido += 1
    
    print(f"Pedido #{pedido['codigo']} criado com sucesso!")
    print(f"Status: {pedido['status']}")
    if valor_total != valor_com_desconto:
        print(f"Valor original: R$ {valor_total:.2f}")
        print(f"Valor com desconto: R$ {valor_com_desconto:.2f}")
    else:
        print(f"Valor total: R$ {valor_com_desconto:.2f}")
    
    salvar_dados()

def imprimir_pedido(pedido):
    print(f"\n{'='*50}")
    print(f"PEDIDO #{pedido['codigo']:03d}")
    print(f"Status: {pedido['status']}")
    print(f"{'='*50}")
    
    print("ITENS:")
    for item in pedido['itens_do_pedido']:
        print(f"    • {item['quantidade']}x {item['nome_produto']} (Cód: {item['codigo_produto']}) - R$ {item['subtotal']:.2f}")
    
    if pedido['cupom']:
        print(f"\nCupom aplicado: {pedido['cupom']}")
    
    print(f"\nVALOR TOTAL: R$ {pedido['valor_final']:.2f}")
    print(f"{'='*50}")

def consultar_pedido():
    if not todos_os_pedidos:
        print("Nenhum pedido registrado no sistema.")
        return

    while True:
        print("\n--- Consultar Pedidos ---")
        print("(1) Ver todos os pedidos")
        print("(2) Filtrar por status")
        print("(0) Voltar ao menu principal")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "0":
            break
        elif opcao == "1":
            pedidos_ordenados = counting_sort(todos_os_pedidos, "codigo")
            print("\n--- TODOS OS PEDIDOS ---")

            for pedido in pedidos_ordenados:
                imprimir_pedido(pedido)
        elif opcao == "2":
            filtrar_pedidos_por_status()
        else:
            print("Opção inválida!")

def filtrar_pedidos_por_status():
    status_opcoes = {
        "1": "AGUARDANDO APROVACAO",
        "2": "ACEITO", 
        "3": "FAZENDO",
        "4": "FEITO",
        "5": "ESPERANDO ENTREGADOR",
        "6": "SAIU PARA ENTREGA",
        "7": "ENTREGUE",
        "8": "CANCELADO",
        "9": "REJEITADO"
    }
    
    print("\nFiltrar por status:")
    for num, status in status_opcoes.items():
        print(f"({num}) {status}")
    print("(0) Voltar")
    
    escolha = input("Escolha o status: ").strip()
    
    if escolha == "0":
        return
    
    if escolha not in status_opcoes:
        print("Opção inválida!")
        return
    
    status_escolhido = status_opcoes[escolha]
    pedidos_filtrados = [p for p in todos_os_pedidos if p['status'] == status_escolhido]
    
    if not pedidos_filtrados:
        print(f"\nNenhum pedido encontrado com status '{status_escolhido}'.")
    else:
        print(f"\n--- PEDIDOS: {status_escolhido} ---")
        for pedido in pedidos_filtrados:
            imprimir_pedido(pedido)

def gerenciar_status_pedido():
    while True:
        print("\n--- Processar Pedidos ---")
        print("O sistema processará sempre o pedido mais antigo de cada etapa.")
        print()
        
        status_count = {}
        for pedido in pedidos_ativos:
            status = pedido['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        print("Status atual dos pedidos ativos:")
        if not status_count:
            print("    Nenhum pedido ativo.")
        else:
            for status, count in status_count.items():
                print(f"    • {status}: {count} pedido(s)")
        print()
        
        print("(1) Aprovar/Rejeitar pedidos")
        print("(2) Iniciar preparo")
        print("(3) Finalizar preparo") 
        print("(4) Aguardar entregador")
        print("(5) Enviar para entrega")
        print("(6) Confirmar entrega")
        print("(7) Cancelar pedido")
        print("(0) Voltar ao menu")
        
        opcao = input("Escolha uma ação: ").strip()
        
        if opcao == "0":
            break
        elif opcao == "1":
            processar_aprovacao()
        elif opcao == "2":
            processar_inicio_preparo()
        elif opcao == "3":
            processar_fim_preparo()
        elif opcao == "4":
            processar_aguardar_entregador()
        elif opcao == "5":
            processar_envio_entrega()
        elif opcao == "6":
            processar_confirmacao_entrega()
        elif opcao == "7":
            cancelar_pedido()
        else:
            print("Opção inválida!")

def processar_aprovacao():
    try:
        pedido = pedido_aguardando_aprovacao.pop(0)
    except IndexError:
        print("Nenhum pedido aguardando aprovação.")
        return
    
    imprimir_pedido(pedido)
    
    while True:
        decisao = input("Aprovar (A) ou Rejeitar (R)? ").strip().upper()
        if decisao == "A":
            pedido['status'] = "ACEITO"
            pedido_aceito.append(pedido)
            print(f"Pedido #{pedido['codigo']} aprovado!")
            break
        elif decisao == "R":
            pedido['status'] = "REJEITADO"
            pedido_rejeitado.append(pedido)
            pedidos_ativos.remove(pedido)
            pedidos_finalizados.append(pedido)
            print(f"Pedido #{pedido['codigo']} rejeitado!")
            break
        else:
            print("Digite A para aprovar ou R para rejeitar.")
    salvar_dados()

def processar_inicio_preparo():
    try:
        pedido = pedido_aceito.pop(0)
    except IndexError:
        print("Nenhum pedido aceito para iniciar preparo.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Iniciar preparo deste pedido? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido['status'] = "FAZENDO"
        pedido_fazendo.append(pedido)
        print(f"Preparo do pedido #{pedido['codigo']} iniciado!")
    else:
        pedido_aceito.insert(0, pedido)
        print(f"Pedido #{pedido['codigo']} devolvido à fila de aceitos.")
    salvar_dados()

def processar_fim_preparo():
    try:
        pedido = pedido_fazendo.pop(0)
    except IndexError:
        print("Nenhum pedido em preparo.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Finalizar preparo deste pedido? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido['status'] = "FEITO"
        pedido_feito.append(pedido)
        print(f"Pedido #{pedido['codigo']} está pronto!")
    else:
        pedido_fazendo.insert(0, pedido)
        print(f"Pedido #{pedido['codigo']} devolvito à fila de preparo.")
    salvar_dados()

def processar_aguardar_entregador():
    try:
        pedido = pedido_feito.pop(0)
    except IndexError:
        print("Nenhum pedido pronto aguardando entregador.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Mover para aguardar entregador? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido['status'] = "ESPERANDO ENTREGADOR"
        pedido_esperando_entregador.append(pedido)
        print(f"Pedido #{pedido['codigo']} aguardando entregador!")
    else:
        pedido_feito.insert(0, pedido)
        print(f"Pedido #{pedido['codigo']} devolvido à fila de prontos.")
    salvar_dados()

def processar_envio_entrega():
    try:
        pedido = pedido_esperando_entregador.pop(0)
    except IndexError:
        print("Nenhum pedido aguardando entregador.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Enviar para entrega? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido['status'] = "SAIU PARA ENTREGA"
        pedido_saiu_entrega.append(pedido)
        print(f"Pedido #{pedido['codigo']} saiu para entrega!")
    else:
        pedido_esperando_entregador.insert(0, pedido)
        print(f"Pedido #{pedido['codigo']} devolvido à espera por entregador.")
    salvar_dados()

def processar_confirmacao_entrega():
    try:
        pedido = pedido_saiu_entrega.pop(0)
    except IndexError:
        print("Nenhum pedido em rota de entrega.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Confirmar entrega? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido['status'] = "ENTREGUE"
        pedido_entregue.append(pedido)
        pedidos_ativos.remove(pedido)
        pedidos_finalizados.append(pedido)
        print(f"Pedido #{pedido['codigo']} entregue com sucesso!")
    else:
        pedido_saiu_entrega.insert(0, pedido)
        print(f"Pedido #{pedido['codigo']} devolvido à rota de entrega.")
    salvar_dados()

def cancelar_pedido():
    if not pedidos_ativos:
        print("Nenhum pedido ativo para cancelar.")
        return
    
    print("Pedidos ativos (cancelamento permitido apenas para 'AGUARDANDO APROVACAO' ou 'ACEITO'):")
    for pedido in pedidos_ativos:
        print(f"    #{pedido['codigo']} - {pedido['status']} - R$ {pedido['valor_final']:.2f}")
    
    try:
        codigo = int(input("Digite o código do pedido para cancelar: "))
    except ValueError:
        print("Código inválido!")
        return
    
    pedido_encontrado = None
    for pedido in pedidos_ativos:
        if pedido['codigo'] == codigo:
            pedido_encontrado = pedido
            break
    
    if not pedido_encontrado:
        print("Pedido não encontrado!")
        return
    
    status_atual = pedido_encontrado['status']
    
    if status_atual not in ["AGUARDANDO APROVACAO", "ACEITO"]:
        print(f"\nEste pedido não pode ser cancelado.")
        print(f"Status atual: {status_atual}")
        print("Apenas pedidos com status 'AGUARDANDO APROVACAO' ou 'ACEITO' podem ser cancelados.")
        return

    for item_pedido in pedido_encontrado['itens_do_pedido']:
        codigo_item = item_pedido['codigo_produto']
        quantidade = item_pedido['quantidade']
        for item in itens:
            if item['codigo'] == codigo_item:
                item['estoque'] += quantidade
                break
    
    if status_atual == "AGUARDANDO APROVACAO" and pedido_encontrado in pedido_aguardando_aprovacao:
        pedido_aguardando_aprovacao.remove(pedido_encontrado)
    elif status_atual == "ACEITO" and pedido_encontrado in pedido_aceito:
        pedido_aceito.remove(pedido_encontrado)
    
    pedido_encontrado['status'] = "CANCELADO"
    pedido_cancelado.append(pedido_encontrado)
    pedidos_ativos.remove(pedido_encontrado)
    pedidos_finalizados.append(pedido_encontrado)
    
    print(f"\nPedido #{pedido_encontrado['codigo']} cancelado com sucesso!")
    print("Os itens foram devolvidos ao estoque.")
    salvar_dados()
    
def menu_principal():
    while True:
        print("\n" + "="*50)
        print("          SISTEMA DE PEDIDOS")
        print("="*50)
        print("(1) Cadastrar Item")
        print("(2) Modificar Item")
        print("(3) Consultar Itens")
        print("(4) Criar Pedido")
        print("(5) Processar Pedidos")
        print("(6) Consultar Pedidos")
        print("(0) Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_item()
        elif opcao == "2":
            modificar_itens()
        elif opcao == "3":
            consultar_itens()
        elif opcao == "4":
            criar_pedido()
        elif opcao == "5":
            gerenciar_status_pedido()
        elif opcao == "6":
            consultar_pedido()
        elif opcao == "0":
            print("Obrigado por usar o sistema! Dados salvos.")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    carregar_dados()
    menu_principal()
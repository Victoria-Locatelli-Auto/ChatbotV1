import sqlite3

def conectar():
    return sqlite3.connect('pizzaria.db')

def exibir_pizzas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cod, sabor, p, m, g FROM pizzas")
    pizzas = cursor.fetchall()
    print("\n🍕 Sabores de Pizza:")
    for cod, sabor, p, m, g in pizzas:
        print(f"{cod} - {sabor} | P: R${p:.2f}, M: R${m:.2f}, G: R${g:.2f}")
    conn.close()

def exibir_bordas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cod, sabor, p, m, g FROM bordas")
    bordas = cursor.fetchall()
    print("\n🍞 Bordas:")
    for cod, sabor, p, m, g in bordas:
        print(f"{cod} - {sabor} | P: R${p:.2f}, M: R${m:.2f}, G: R${g:.2f}")
    conn.close()

def exibir_bebidas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cod, nome, valor FROM bebidas")
    bebidas = cursor.fetchall()
    print("\n🥤 Bebidas:")
    for cod, nome, valor in bebidas:
        print(f"{cod} - {nome}: R${valor:.2f}")
    conn.close()

def calcular_entrega(bairro):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM enderecos WHERE bairro LIKE ?", (bairro,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def fazer_pedido():
    print("\n--- Fazer Pedido ---")

    # Perguntar tamanho
    tamanho = input("Escolha o tamanho da pizza (P/M/G): ").upper()
    if tamanho not in ["P", "M", "G"]:
        print("Tamanho inválido. Pedido cancelado.")
        return

    # Limite de sabores
    limite_sabores = 2 if tamanho in ["P", "M"] else 3
    print(f"\nVocê pode escolher até {limite_sabores} sabor(es).")

    exibir_pizzas()

    # Sabores selecionados
    sabores_selecionados = []
    for i in range(limite_sabores):
        cod_sabor = input(f"Digite o código do sabor {i+1} (ou Enter para parar): ").upper()
        if not cod_sabor:
            break
        sabores_selecionados.append(cod_sabor)

    if not sabores_selecionados:
        print("Nenhum sabor selecionado. Pedido cancelado.")
        return

    # Escolher borda
    exibir_bordas()
    borda = input("Digite o código da borda (ou Enter para nenhuma): ").upper() or None

    # Escolher bebida
    exibir_bebidas()
    bebida = input("Digite o código da bebida (ou Enter para nenhuma): ").upper() or None

    # Tipo de pedido
    tipo_pedido = input("O pedido será para entrega ou retirada? ").strip().lower()
    if tipo_pedido not in ["entrega", "retirada"]:
        print("Tipo de pedido inválido. Pedido cancelado.")
        return

    taxa = 0
    bairro = None
    endereco_completo = ""

    if tipo_pedido == "entrega":
        while True:
            bairro = input("Digite o bairro para entrega: ").strip().title()
            taxa = calcular_entrega(bairro)
            if taxa is not None:
                break
            print("⚠ Bairro não encontrado. Tente novamente.")

        endereco_completo = input("Digite o restante do endereço (rua, número, complemento): ").strip()

    # Conexão e cálculos
    conn = conectar()
    cursor = conn.cursor()

    preco_total_pizza = 0
    for cod in sabores_selecionados:
        cursor.execute(f"SELECT {tamanho} FROM pizzas WHERE cod = ?", (cod,))
        resultado = cursor.fetchone()
        if resultado:
            preco_total_pizza += resultado[0]
        else:
            print(f"Sabor {cod} não encontrado. Ignorado.")

    preco_pizza_final = preco_total_pizza / len(sabores_selecionados)

    preco_borda = 0
    if borda:
        cursor.execute(f"SELECT {tamanho} FROM bordas WHERE cod = ?", (borda,))
        resultado = cursor.fetchone()
        if resultado:
            preco_borda = resultado[0]

    preco_bebida = 0
    if bebida:
        cursor.execute("SELECT valor FROM bebidas WHERE cod = ?", (bebida,))
        resultado = cursor.fetchone()
        if resultado:
            preco_bebida = resultado[0]

    conn.close()

    total = preco_pizza_final + preco_borda + preco_bebida + taxa

    print("\n--- Resumo do Pedido ---")
    print(f"Tamanho: {tamanho}")
    print("Sabores selecionados:", ", ".join(sabores_selecionados))
    if borda:
        print(f"Borda: {borda}")
    if bebida:
        print(f"Bebida: {bebida}")
    print(f"Tipo de pedido: {tipo_pedido.capitalize()}")
    if tipo_pedido == "entrega":
        print(f"Bairro: {bairro}")
        print(f"Endereço: {endereco_completo}")
        print(f"Taxa de entrega: R${taxa:.2f}")
    print(f"Total do pedido: R${total:.2f}")
    print("Obrigado por seu pedido! 🍕")

def menu():
    while True:
        print("\n--- Chatbot da Pizzaria ---")
        print("1. Ver cardápio de pizzas")
        print("2. Ver bordas")
        print("3. Ver bebidas")
        print("4. Fazer pedido")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            exibir_pizzas()
        elif opcao == "2":
            exibir_bordas()
        elif opcao == "3":
            exibir_bebidas()
        elif opcao == "4":
            fazer_pedido()
        elif opcao == "5":
            print("Até logo! 👋")
            break
        else:
            print("Opção inválida!")

# Executar menu
menu()

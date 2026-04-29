import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from connect import connect_to_database

# =======================
# CONFIGURAÇÕES DE DESIGN
# =======================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COR_SIDEBAR, COR_TEXTO, COR_FUNDO = "#1E1E2F", "#FFFFFF", "#F5F5F5"
COR_BOTAO, COR_EDITAR, COR_EXCLUIR = "#FF6B00", "#4CAF50", "#F44336"
ORANGE, DARK, LIGHT_BG = "#ff6b00", "#0d1b2a", "#f5f6f8"

# =======================
# FUNÇÕES DE FORMATAÇÃO E MÁSCARAS
# =======================
def aplicar_mascara_cpf(event):
    texto = ''.join(filter(str.isdigit, event.widget.get()))
    novo = ""
    for i, char in enumerate(texto):
        if i == 3 or i == 6: novo += "."
        elif i == 9: novo += "-"
        novo += char
    event.widget.delete(0, "end")
    event.widget.insert(0, novo[:14])

def aplicar_mascara_tel(event):
    texto = ''.join(filter(str.isdigit, event.widget.get()))
    novo = ""
    for i, char in enumerate(texto):
        if i == 0: novo += "("
        elif i == 2: novo += ") "
        elif i == 7: novo += "-"
        novo += char
    event.widget.delete(0, "end")
    event.widget.insert(0, novo[:15])

def formatar_cpf(cpf):
    c = ''.join(filter(str.isdigit, str(cpf)))
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c) == 11 else c

def formatar_telefone(tel):
    t = ''.join(filter(str.isdigit, str(tel)))
    if len(t) == 11: return f"({t[:2]}) {t[2:7]}-{t[7:]}"
    elif len(t) == 10: return f"({t[:2]}) {t[2:6]}-{t[6:]}"
    return t


# =======================
# SISTEMA PRINCIPAL (GESTAO)
# =======================
def iniciar_sistema():
    global root, main_frame
    
    root = ctk.CTk()
    root.title("Gestão Pizzaloop")
    root.geometry("1200x800")
    root.attributes("-fullscreen", True)
    root.conn = connect_to_database()

    sidebar = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color=COR_SIDEBAR)
    sidebar.pack(side="left", fill="y")
    ctk.CTkLabel(sidebar, text="Pizzaloop", font=("Arial", 22, "bold"), text_color=COR_TEXTO).pack(pady=30)

    main_frame = ctk.CTkFrame(root, fg_color=COR_FUNDO)
    main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    ctk.CTkButton(sidebar, text="Dashboard", command=tela_dashboard).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Pedidos", command=tela_pedidos).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Clientes", command=tela_clientes).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Produtos", command=tela_produtos).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Sair", fg_color="#333", command=root.quit).pack(side="bottom", pady=20)

    tela_dashboard()
    root.mainloop()

def limpar_main():
    for widget in main_frame.winfo_children(): widget.destroy()

def tela_dashboard():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Dashboard Pizzaloop 🍕", font=("Arial", 30, "bold")).pack(pady=50)

# =======================
# TELA DE CLIENTES
# =======================

def tela_clientes():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gerenciar Clientes 👥", font=("Arial", 24, "bold")).pack(pady=20)
    def abrir_form(dados=None):
        f = ctk.CTkToplevel(root); f.geometry("400x480"); f.attributes("-topmost", True)
        en_n = ctk.CTkEntry(f, placeholder_text="Nome", width=300); en_n.pack(pady=10)
        en_t = ctk.CTkEntry(f, placeholder_text="(00) 00000-0000", width=300); en_t.pack(pady=10)
        en_t.bind("<KeyRelease>", aplicar_mascara_tel)
        en_c = ctk.CTkEntry(f, placeholder_text="000.000.000-00", width=300); en_c.pack(pady=10)
        en_c.bind("<KeyRelease>", aplicar_mascara_cpf)
        if dados:
            en_n.insert(0, dados['nome']); en_t.insert(0, formatar_telefone(dados['telefone'])); en_c.insert(0, formatar_cpf(dados['cpf']))
        def salvar():
            n, t, c = en_n.get(), ''.join(filter(str.isdigit, en_t.get())), ''.join(filter(str.isdigit, en_c.get()))
            if len(c) != 11: messagebox.showerror("Erro", "CPF Inválido"); return
            try:
                cur = root.conn.cursor()
                if dados: cur.execute("UPDATE cliente SET nome=%s, telefone=%s, cpf=%s WHERE id_cliente=%s", (n, t, c, dados['id_cliente']))
                else: cur.execute("INSERT INTO cliente (nome, telefone, cep, endereco, cpf) VALUES (%s,%s,'0','0',%s)", (n, t, c))
                root.conn.commit(); cur.close(); f.destroy(); tela_clientes()
            except Exception as e: messagebox.showerror("Erro", str(e))
        ctk.CTkButton(f, text="Salvar", fg_color=COR_BOTAO, command=salvar).pack(pady=20)
    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=COR_BOTAO, command=lambda: abrir_form()).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent"); scroll.pack(fill="both", expand=True)
    cursor = root.conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente ORDER BY nome ASC")
    for c in cursor.fetchall():
        card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10); card.pack(fill="x", pady=5, padx=10)
        ctk.CTkLabel(card, text=f"{c['nome']}\nCPF: {formatar_cpf(c['cpf'])}", font=("Arial", 13, "bold"), justify="left").pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(card, text=f"📞 {formatar_telefone(c['telefone'])}", font=("Arial", 12), text_color="gray").pack(side="left", padx=30)
        ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=lambda i=c['id_cliente']: excluir_item(i, "cliente")).pack(side="right", padx=10)
        ctk.CTkButton(card, text="Editar", fg_color=COR_EDITAR, width=60, command=lambda d=c: abrir_form(d)).pack(side="right", padx=5)
    cursor.close()      

# =======================
# TELA DE PRODUTOS
# =======================

def tela_produtos():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Produtos 🍕", font=("Arial", 24, "bold")).pack(pady=20)
    def abrir_form(dados=None):
        f = ctk.CTkToplevel(root); f.geometry("400x400"); f.attributes("-topmost", True)
        en_n = ctk.CTkEntry(f, placeholder_text="Nome", width=300); en_n.pack(pady=10)
        en_p = ctk.CTkEntry(f, placeholder_text="Preço", width=300); en_p.pack(pady=10)
        if dados: en_n.insert(0, dados['nome_produto']); en_p.insert(0, str(dados['preco']))
        def salvar():
            try:
                cur = root.conn.cursor(); n, p = en_n.get(), float(en_p.get().replace(",", "."))
                if dados: cur.execute("UPDATE produtos SET nome_produto=%s, preco=%s WHERE id_produto=%s", (n, p, dados['id_produto']))
                else: cur.execute("INSERT INTO produtos (nome_produto, preco, categoria) VALUES (%s,%s,'Pizza')", (n, p))
                root.conn.commit(); cur.close(); f.destroy(); tela_produtos()
            except Exception as e: messagebox.showerror("Erro", str(e))
        ctk.CTkButton(f, text="Salvar", fg_color=COR_BOTAO, command=salvar).pack(pady=20)
    ctk.CTkButton(main_frame, text="+ Novo Produto", fg_color=COR_BOTAO, command=lambda: abrir_form()).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent"); scroll.pack(fill="both", expand=True)
    cursor = root.conn.cursor(dictionary=True); cursor.execute("SELECT * FROM produtos")
    for p in cursor.fetchall():
        card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10); card.pack(fill="x", pady=5, padx=10)
        ctk.CTkLabel(card, text=f"{p['nome_produto']}", font=("Arial", 13, "bold")).pack(side="left", padx=15)
        ctk.CTkLabel(card, text=f"R$ {p['preco']:.2f}", font=("Arial", 12)).pack(side="left", padx=20)
        ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=lambda i=p['id_produto']: excluir_item(i, "produtos")).pack(side="right", padx=10)
        ctk.CTkButton(card, text="Editar", fg_color=COR_EDITAR, width=60, command=lambda d=p: abrir_form(d)).pack(side="right", padx=5)
    cursor.close()  

# =======================
# TELA DE PEDIDOS
# =======================

def tela_pedidos():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Pedidos 📋", font=("Arial", 24, "bold")).pack(pady=20)
    def abrir_form(dados=None):
        f = ctk.CTkToplevel(root); f.geometry("450x600"); f.attributes("-topmost", True)
        f.title("Editar Pedido" if dados else "Novo Pedido")
        
        cur = root.conn.cursor()
        cur.execute("SELECT id_cliente, nome FROM cliente"); dict_cli = {n: i for i, n in cur.fetchall()}
        cur.execute("SELECT id_produto, nome_produto, preco FROM produtos"); dict_prod = {n: (i, p) for i, n, p in cur.fetchall()}; cur.close()

        # IDENTIFICAÇÃO DOS CAMPOS NO FORMULÁRIO (COMO ESTAVA ANTES)
        ctk.CTkLabel(f, text="Nome do Cliente:").pack(pady=(10, 0))
        cb_cli = ctk.CTkComboBox(f, values=list(dict_cli.keys()), width=300); cb_cli.pack(pady=5)

        ctk.CTkLabel(f, text="Item (Produto):").pack(pady=(10, 0))
        cb_prod = ctk.CTkComboBox(f, values=list(dict_prod.keys()), width=300); cb_prod.pack(pady=5)

        ctk.CTkLabel(f, text="Quantidade:").pack(pady=(10, 0))
        en_qtd = ctk.CTkEntry(f, width=300); en_qtd.insert(0, "1"); en_qtd.pack(pady=5)

        ctk.CTkLabel(f, text="Status do Pedido:").pack(pady=(10, 0))
        cb_st = ctk.CTkComboBox(f, values=['Em preparo', 'Saiu para entrega', 'Entregue'], width=300); cb_st.pack(pady=5)

        if dados:
            cb_cli.set(dados['nome_cliente']); cb_prod.set(dados['nome_produto'])
            en_qtd.delete(0, 'end'); en_qtd.insert(0, str(dados['quantidade'])); cb_st.set(dados['status_pedido'])
        
        def salvar():
            try:
                id_c, (id_p, pr), qtd, st = dict_cli[cb_cli.get()], dict_prod[cb_prod.get()], int(en_qtd.get()), cb_st.get()
                total, c = (float(pr) * qtd), root.conn.cursor()
                if dados:
                    c.execute("UPDATE pedidos SET id_cliente=%s, valor_total=%s, status_pedido=%s WHERE id_pedidos=%s", (id_c, total, st, dados['id_pedidos']))
                    c.execute("UPDATE itens_pedidos SET id_produto=%s, quantidade=%s WHERE id_pedido=%s", (id_p, qtd, dados['id_pedidos']))
                else:
                    c.execute("INSERT INTO pedidos (id_cliente, valor_total, status_pedido, data_hora) VALUES (%s,%s,%s,NOW())", (id_c, total, st))
                    c.execute("INSERT INTO itens_pedidos (id_pedido, id_produto, quantidade) VALUES (%s,%s,%s)", (c.lastrowid, id_p, qtd))
                root.conn.commit(); c.close(); f.destroy(); tela_pedidos()
            except: messagebox.showerror("Erro", "Verifique as opções!")
        
        ctk.CTkButton(f, text="Salvar", fg_color=COR_BOTAO, command=salvar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Pedido", fg_color=COR_BOTAO, command=lambda: abrir_form()).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent"); scroll.pack(fill="both", expand=True)
    cursor = root.conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.nome as nome_cliente, pr.nome_produto, i.quantidade, DATE_FORMAT(p.data_hora, '%d/%m %H:%i') as dt 
        FROM pedidos p JOIN cliente c ON p.id_cliente = c.id_cliente 
        JOIN itens_pedidos i ON p.id_pedidos = i.id_pedido JOIN produtos pr ON i.id_produto = pr.id_produto 
        ORDER BY p.id_pedidos DESC""")
    for p in cursor.fetchall():
        card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10); card.pack(fill="x", pady=5, padx=10)
        
        # Na tela de listagem continua limpo como você pediu antes (sem o texto "Produto:")
        info = f"ID: #{p['id_pedidos']} | Cliente: {p['nome_cliente']}\n{p['nome_produto']} (Qtd: {p['quantidade']})"
        
        ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"), justify="left").pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(card, text=f"Data: {p['dt']}", font=("Arial", 11), text_color="gray").pack(side="left", padx=30)
        ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=lambda i=p['id_pedidos']: excluir_item(i, "pedidos")).pack(side="right", padx=10)
        ctk.CTkButton(card, text="Editar", fg_color=COR_EDITAR, width=60, command=lambda d=p: abrir_form(d)).pack(side="right", padx=5)
        ctk.CTkLabel(card, text=f"{p['status_pedido']} | R$ {p['valor_total']:.2f}", font=("Arial", 12, "bold"), text_color="#2E7D32").pack(side="right", padx=15)
    cursor.close()


def excluir_item(id_item, tabela):
    if messagebox.askyesno("Confirmar", f"Excluir item?"):
        try:
            cursor = root.conn.cursor(); mapa = {"produtos": "id_produto", "cliente": "id_cliente", "pedidos": "id_pedidos"}
            cursor.execute(f"DELETE FROM {tabela} WHERE {mapa[tabela]} = %s", (id_item,))
            root.conn.commit(); cursor.close()
            globals()[f"tela_{tabela}"]()
        except: messagebox.showerror("Erro", "Remova vínculos no banco primeiro.")

# =======================
# LOGIN E INICIALIZAÇÃO
# =======================
def fazer_login():
    e, s = email_entry.get().strip(), password_entry.get().strip()
    try:
        conn = connect_to_database(); cursor = conn.cursor()
        cursor.execute("SELECT senha FROM login WHERE email=%s", (e,))
        res = cursor.fetchone()
        if res and res[0] == s: login_win.destroy(); iniciar_sistema()
        else: messagebox.showerror("Erro", "E-mail ou senha inválidos.")
        cursor.close(); conn.close()
    except Exception as err: messagebox.showerror("Erro", str(err))

def abrir_cadastro():
    login_win.withdraw()
    cad = ctk.CTkToplevel(login_win); cad.geometry("400x500"); cad.title("Criar Conta")
    email_cadastro = ctk.CTkEntry(cad, placeholder_text="Email", width=300); email_cadastro.pack(pady=20)
    senha_cadastro = ctk.CTkEntry(cad, placeholder_text="Senha", show="*", width=300); senha_cadastro.pack(pady=10)
    def salvar():
        try:
            conn = connect_to_database(); cursor = conn.cursor()
            cursor.execute("INSERT INTO login (email, senha) VALUES (%s, %s)", (email_cadastro.get(), senha_cadastro.get()))
            conn.commit(); cad.destroy(); login_win.deiconify()
        except: messagebox.showerror("Erro", "E-mail já existe!")
    ctk.CTkButton(cad, text="Cadastrar", fg_color=ORANGE, command=salvar).pack(pady=20)
    cad.protocol("WM_DELETE_WINDOW", lambda: (cad.destroy(), login_win.deiconify()))

login_win = ctk.CTk()
login_win.title("Login - Pizzaloop"); login_win.geometry("1200x600")
left_f = ctk.CTkFrame(login_win, width=350, fg_color=DARK, corner_radius=0); left_f.pack(side="left", fill="y")
ctk.CTkLabel(left_f, text="🍕 Pizzaloop", font=("Arial", 24, "bold"), text_color="white").place(relx=0.5, rely=0.4, anchor="center")
right_f = ctk.CTkFrame(login_win, fg_color=LIGHT_BG, corner_radius=0); right_f.pack(side="right", fill="both", expand=True)
card = ctk.CTkFrame(right_f, width=350, height=400, corner_radius=15, fg_color="white"); card.place(relx=0.5, rely=0.5, anchor="center")
email_entry = ctk.CTkEntry(card, placeholder_text="Email", width=260); email_entry.pack(pady=(50, 10))
password_entry = ctk.CTkEntry(card, placeholder_text="Senha", show="*", width=260); password_entry.pack(pady=10)
ctk.CTkButton(card, text="Entrar", fg_color=ORANGE, command=fazer_login).pack(pady=20)
footer = ctk.CTkLabel(card, text="Criar conta", cursor="hand2", text_color="gray"); footer.pack(); footer.bind("<Button-1>", lambda e: abrir_cadastro())

login_win.mainloop()

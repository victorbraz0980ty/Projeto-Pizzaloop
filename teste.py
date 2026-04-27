from tkinter import messagebox
import customtkinter as ctk
from connect import connect_to_database

# Configurações de Design ORIGINAIS
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COR_SIDEBAR, COR_TEXTO, COR_FUNDO = "#1E1E2F", "#FFFFFF", "#F5F5F5"
COR_BOTAO, COR_EDITAR, COR_EXCLUIR = "#FF6B00", "#4CAF50", "#F44336"

root = ctk.CTk()
root.title("Gestão Pizzaloop - Sistema Completo")
root.geometry("1200x800")
root.attributes("-fullscreen", True)

# Conexão com o banco
root.conn = connect_to_database()

# --- FUNÇÕES DE NAVEGAÇÃO ---
def limpar_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

def tela_dashboard():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Dashboard Pizzaloop 🍕", font=("Arial", 30, "bold")).pack(pady=50)
    ctk.CTkLabel(main_frame, text="Selecione uma opção no menu lateral.", font=("Arial", 16)).pack()

# =======================
# GESTÃO DE CLIENTES (CONECTADO)
# =======================
def tela_clientes():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gerenciar Clientes 👥", font=("Arial", 24, "bold")).pack(pady=20)
    
    def salvar_cliente():
        form = ctk.CTkToplevel(root); form.geometry("400x400"); form.attributes("-topmost", True)
        n = ctk.CTkEntry(form, placeholder_text="Nome", width=300); n.pack(pady=10)
        t = ctk.CTkEntry(form, placeholder_text="Telefone", width=300); t.pack(pady=10)
        c = ctk.CTkEntry(form, placeholder_text="CPF", width=300); c.pack(pady=10)

        def confirmar():
            try:
                cursor = root.conn.cursor()
                sql = "INSERT INTO cliente (nome, telefone, cep, endereco, cpf) VALUES (%s, %s, '00000', 'Endereço', %s)"
                cursor.execute(sql, (n.get(), t.get(), c.get()))
                root.conn.commit()
                messagebox.showinfo("Sucesso", "Cliente salvo!")
                form.destroy(); tela_clientes()
            except Exception as e: messagebox.showerror("Erro", str(e))
        ctk.CTkButton(form, text="Salvar", fg_color=COR_BOTAO, command=confirmar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=COR_BOTAO, command=salvar_cliente).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    try:
        cursor = root.conn.cursor()
        cursor.execute("SELECT id_cliente, nome, telefone FROM cliente")
        for (id_c, nome, tel) in cursor.fetchall():
            card = ctk.CTkFrame(scroll, fg_color="white")
            card.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(card, text=f"{nome} | {tel}", font=("Arial", 14, "bold")).pack(side="left", padx=15)
            ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=lambda i=id_c: excluir_item(i, "cliente")).pack(side="right", padx=10)
    except: pass

# =======================
# GESTÃO DE PRODUTOS (CONECTADO)
# =======================
def tela_produtos():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gestão de Produtos 🍕", font=("Arial", 24, "bold")).pack(pady=20)
    
    def salvar_produto():
        form = ctk.CTkToplevel(root); form.geometry("400x400"); form.attributes("-topmost", True)
        n = ctk.CTkEntry(form, placeholder_text="Nome", width=300); n.pack(pady=10)
        p = ctk.CTkEntry(form, placeholder_text="Preço", width=300); p.pack(pady=10)

        def confirmar():
            try:
                cursor = root.conn.cursor()
                sql = "INSERT INTO produtos (nome_produto, preco, categoria) VALUES (%s, %s, 'Pizza')"
                cursor.execute(sql, (n.get(), float(p.get().replace(",", "."))))
                root.conn.commit()
                form.destroy(); tela_produtos()
            except Exception as e: messagebox.showerror("Erro", str(e))
        ctk.CTkButton(form, text="Salvar", fg_color=COR_BOTAO, command=confirmar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Produto", fg_color=COR_BOTAO, command=salvar_produto).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    try:
        cursor = root.conn.cursor()
        cursor.execute("SELECT id_produto, nome_produto, preco FROM produtos")
        for (id_p, nome, preco) in cursor.fetchall():
            card = ctk.CTkFrame(scroll, fg_color="white")
            card.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(card, text=f"{nome} | R$ {preco:.2f}", font=("Arial", 14, "bold")).pack(side="left", padx=15)
            ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=lambda i=id_p: excluir_item(i, "produtos")).pack(side="right", padx=10)
    except: pass

def excluir_item(id_item, tabela):
    if messagebox.askyesno("Confirmar", "Deseja excluir?"):
        cursor = root.conn.cursor()
        coluna = "id_produto" if tabela == "produtos" else "id_cliente"
        cursor.execute(f"DELETE FROM {tabela} WHERE {coluna} = %s", (id_item,))
        root.conn.commit()
        if tabela == "produtos": tela_produtos()
        else: tela_clientes()

# --- SIDEBAR COM TODOS OS BOTÕES DO DESIGN ANTIGO ---
sidebar = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color=COR_SIDEBAR)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="Pizzaloop", font=("Arial", 22, "bold"), text_color=COR_TEXTO).pack(pady=30)

# Botões Restaurados
ctk.CTkButton(sidebar, text="Dashboard", command=tela_dashboard).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Pedidos", command=lambda: (limpar_main(), ctk.CTkLabel(main_frame, text="Tela de Pedidos", font=("Arial", 24)).pack(pady=50))).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Clientes", command=tela_clientes).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Produtos", command=tela_produtos).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Cardápio", command=lambda: (limpar_main(), ctk.CTkLabel(main_frame, text="Tela de Cardápio", font=("Arial", 24)).pack(pady=50))).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Relatórios", command=lambda: (limpar_main(), ctk.CTkLabel(main_frame, text="Tela de Relatórios", font=("Arial", 24)).pack(pady=50))).pack(pady=15, padx=20)

ctk.CTkButton(sidebar, text="Sair", fg_color="#333", command=root.quit).pack(side="bottom", pady=20)

main_frame = ctk.CTkFrame(root)
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Início
if root.conn:
    tela_dashboard()
    root.mainloop()
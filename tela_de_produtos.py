from tkinter import messagebox
import customtkinter as ctk
from connect import connect_to_database
# Certifique-se de que esses arquivos de conexão existam ou use o connect_to_database para tudo
from connect import connect_to_database as connect_login_db 
from connect import connect_to_database as connect_cliente_db 

# Configurações iniciais
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COR_SIDEBAR, COR_TEXTO, COR_FUNDO = "#1E1E2F", "#FFFFFF", "#F5F5F5"
COR_BOTAO, COR_EDITAR, COR_EXCLUIR = "#FF6B00", "#4CAF50", "#F44336"

root = ctk.CTk()
root.title("Pizza Loop - Sistema Integrado")
root.geometry("1200x800")
root.attributes("-fullscreen", True)

# Conectar ao banco
root.conn = connect_to_database()

# =======================
# NAVEGAÇÃO E TELAS
# =======================

def limpar_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

def tela_dashboard():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Bem-vindo ao Dashboard! 🍕", font=("Arial", 30, "bold")).pack(pady=40)
    ctk.CTkLabel(main_frame, text="Selecione uma opção na barra lateral para começar.", font=("Arial", 16)).pack()

# --- FUNÇÃO DE CLIENTES (INTEGRADA DO SEU OUTRO CÓDIGO) ---
def tela_clientes():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gerenciar Clientes 🍕", font=("Arial", 24, "bold")).pack(pady=20)
    
    # Botão Novo Cliente
    def abrir_form_novo_cliente():
        form = ctk.CTkToplevel(root)
        form.geometry("400x400")
        form.title("Novo Cliente")
        form.attributes("-topmost", True)

        entry_nome = ctk.CTkEntry(form, placeholder_text="Nome", width=300)
        entry_nome.pack(pady=10)
        entry_tel = ctk.CTkEntry(form, placeholder_text="Telefone", width=300)
        entry_tel.pack(pady=10)
        entry_cpf = ctk.CTkEntry(form, placeholder_text="CPF", width=300)
        entry_cpf.pack(pady=10)

        def salvar():
            con = connect_cliente_db()
            if con:
                try:
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO cliente (nome, telefone, cpf, cep, endereco) VALUES (%s, %s, %s, '00000', 'Rua')", 
                                   (entry_nome.get(), entry_tel.get(), entry_cpf.get()))
                    con.commit()
                    messagebox.showinfo("Sucesso", "Cliente cadastrado!")
                    form.destroy()
                    tela_clientes()
                except Exception as e: messagebox.showerror("Erro", str(e))
                finally: con.close()

        ctk.CTkButton(form, text="Salvar", fg_color=COR_BOTAO, command=salvar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=COR_BOTAO, command=abrir_form_novo_cliente).pack(pady=10)

    # Lista de Clientes
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    con = connect_cliente_db()
    if con:
        try:
            cursor = con.cursor()
            cursor.execute("SELECT nome, telefone, cpf FROM cliente")
            for (nome, tel, cpf) in cursor.fetchall():
                card = ctk.CTkFrame(scroll, fg_color="white")
                card.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(card, text=f"{nome} | {tel}", font=("Arial", 14, "bold")).pack(side="left", padx=15)
                # Botão Excluir Cliente
                ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, 
                             command=lambda c=cpf: excluir_c(c)).pack(side="right", padx=10)
            cursor.close()
        finally: con.close()

def excluir_c(cpf):
    if messagebox.askyesno("Confirmar", "Excluir cliente?"):
        con = connect_cliente_db()
        cursor = con.cursor()
        cursor.execute("DELETE FROM cliente WHERE cpf = %s", (cpf,))
        con.commit()
        con.close()
        tela_clientes()

# =======================
# INTERFACE PRINCIPAL
# =======================

sidebar = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color=COR_SIDEBAR)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="Pizzaloop", font=("Arial", 22, "bold"), text_color=COR_TEXTO).pack(pady=30)

# BOTÕES DA SIDEBAR (Agora com as funções ligadas)
ctk.CTkButton(sidebar, text="Dashboard", command=tela_dashboard).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Clientes", command=tela_clientes).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Produtos").pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Cardápio").pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Relatórios").pack(pady=15, padx=20)

ctk.CTkButton(sidebar, text="Sair", fg_color="#333", command=root.quit).pack(side="bottom", pady=20)

main_frame = ctk.CTkFrame(root)
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Início
tela_dashboard()
root.mainloop()
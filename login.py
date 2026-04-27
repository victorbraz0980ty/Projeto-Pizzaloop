import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

DB_NAME = "pizzaloop"



def criar_banco_e_tabela():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        email VARCHAR(30) UNIQUE NOT NULL,
        senha VARCHAR(45) NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=DB_NAME
    )

criar_banco_e_tabela()
conn = conectar()


cursor = conn.cursor()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Login - Pizzaloop")
app.geometry("1200x600")
app.resizable(False, False)

ORANGE = "#ff6b00"
DARK = "#0d1b2a"
LIGHT_BG = "#f5f6f8"

left_frame = ctk.CTkFrame(app, width=350, fg_color=DARK, corner_radius=0)
left_frame.pack(side="left", fill="y")

logo_label = ctk.CTkLabel(left_frame, text="🍕 Pizzaloop", font=("Arial", 24, "bold"), text_color="white")
logo_label.place(relx=0.5, rely=0.4, anchor="center")

subtitle_label = ctk.CTkLabel(left_frame, text="Painel Administrativo", font=("Arial", 14), text_color="#cbd5e1")
subtitle_label.place(relx=0.5, rely=0.48, anchor="center")

right_frame = ctk.CTkFrame(app, fg_color=LIGHT_BG, corner_radius=0)
right_frame.pack(side="right", fill="both", expand=True)

card = ctk.CTkFrame(right_frame, width=350, height=380, corner_radius=15, fg_color="white")
card.place(relx=0.5, rely=0.5, anchor="center")

title = ctk.CTkLabel(card, text="Bem-vindo 👋", font=("Arial", 22, "bold"), text_color="#1f2937")
title.pack(pady=(30, 5))

subtitle = ctk.CTkLabel(card, text="Faça login para acessar", font=("Arial", 13), text_color="#6b7280")
subtitle.pack(pady=(0, 20))

email_entry = ctk.CTkEntry(card, placeholder_text="Email", width=260, height=40, corner_radius=8)
email_entry.pack(pady=10)

password_entry = ctk.CTkEntry(card, placeholder_text="Senha", show="*", width=260, height=40, corner_radius=8)
password_entry.pack(pady=10)

options_frame = ctk.CTkFrame(card, fg_color="transparent")
options_frame.pack(fill="x", padx=40, pady=10)

remember = ctk.CTkCheckBox(options_frame, text="Lembrar")
remember.pack(side="left")

forgot = ctk.CTkLabel(options_frame, text="Esqueceu a senha?", text_color=ORANGE, cursor="hand2")
forgot.pack(side="right")

def fazer_login():
    email = email_entry.get().strip()
    senha = password_entry.get().strip()

    if not email or not senha:
        messagebox.showerror("Erro", "Preencha email e senha.")
        return

    cursor.execute("SELECT nome FROM login WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        messagebox.showinfo("Login", f"Bem-vindo, {usuario[0]}!")
    else:
        resposta = messagebox.askyesno("Conta não encontrada", "Você ainda não tem conta. Deseja criar agora?")
        if resposta:
            abrir_cadastro()

def abrir_cadastro():
    app.withdraw()

    cadastro_win = ctk.CTkToplevel(app)
    cadastro_win.title("Criar Conta - Pizzaloop")
    cadastro_win.geometry("1200x600")
    cadastro_win.resizable(False, False)

    def fechar_cadastro():
        cadastro_win.destroy()
        app.deiconify()

    cadastro_win.protocol("WM_DELETE_WINDOW", fechar_cadastro)

    frame = ctk.CTkFrame(cadastro_win, fg_color="white", corner_radius=10)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    title = ctk.CTkLabel(frame, text="Criar Conta 🍕", font=("Arial", 20, "bold"), text_color="#1f2937")
    title.pack(pady=(10, 20))

    nome_entry = ctk.CTkEntry(frame, placeholder_text="Nome completo", width=300, height=40)
    nome_entry.pack(pady=10)

    email_entry_cad = ctk.CTkEntry(frame, placeholder_text="Email", width=300, height=40)
    email_entry_cad.pack(pady=10)

    senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300, height=40)
    senha_entry.pack(pady=10)

    confirmar_senha_entry = ctk.CTkEntry(frame, placeholder_text="Confirmar senha", show="*", width=300, height=40)
    confirmar_senha_entry.pack(pady=10)

    def salvar_usuario():
        nome = nome_entry.get().strip()
        email = email_entry_cad.get().strip()
        senha = senha_entry.get().strip()
        confirmar = confirmar_senha_entry.get().strip()


        if not nome or not email or not senha or not confirmar:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem, reveja o que foi digitado!")
            return

        try:
            cursor.execute(
                "INSERT INTO login (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha)
            )
            print(nome, email, senha)
            conn.commit()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            cadastro_win.destroy()
            app.deiconify()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Erro", "Esse email já está cadastrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro no banco de dados: {err}")

    cadastrar_button = ctk.CTkButton(
        frame,
        text="Cadastrar",
        fg_color=ORANGE,
        hover_color="#e65c00",
        width=300,
        height=40,
        corner_radius=8,
        command=salvar_usuario
    )
    cadastrar_button.pack(pady=20)

login_button = ctk.CTkButton(
    card,
    text="Entrar",
    fg_color=ORANGE,
    hover_color="#e65c00",
    width=260,
    height=40,
    corner_radius=8,
    command=fazer_login
)
login_button.pack(pady=20)

footer = ctk.CTkLabel(
    card,
    text="Não tem conta? Criar agora",
    text_color="#6b7280",
    font=("Arial", 12),
    cursor="hand2"
)
footer.pack(pady=(10, 20))
footer.bind("<Button-1>", lambda e: abrir_cadastro())

app.mainloop()
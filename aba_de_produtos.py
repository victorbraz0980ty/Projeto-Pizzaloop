# GESTÃO DE PRODUTOS (CONECTADO)
# =======================
def tela_produtos():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gestão de Produtos 🍕", font=("Arial", 24, "bold")).pack(pady=20)
    
    def salvar_novo_produto():
        form = ctk.CTkToplevel(root)
        form.geometry("400x400")
        form.attributes("-topmost", True)
        
        ent_nome = ctk.CTkEntry(form, placeholder_text="Nome", width=300); ent_nome.pack(pady=10)
        ent_preco = ctk.CTkEntry(form, placeholder_text="Preço", width=300); ent_preco.pack(pady=10)

        def confirmar():
            try:
                cursor = root.conn.cursor()
                sql = "INSERT INTO produtos (nome_produto, preco, categoria) VALUES (%s, %s, 'Pizza')"
                cursor.execute(sql, (ent_nome.get(), float(ent_preco.get().replace(",", "."))))
                root.conn.commit()
                cursor.close()
                messagebox.showinfo("Sucesso", "Produto cadastrado!")
                form.destroy()
                tela_produtos()
            except Exception as e: messagebox.showerror("Erro", str(e))

        ctk.CTkButton(form, text="Salvar", fg_color=COR_BOTAO, command=confirmar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Produto", fg_color=COR_BOTAO, command=salvar_novo_produto).pack(pady=10)

    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    try:
        cursor = root.conn.cursor()
        cursor.execute("SELECT id_produto, nome_produto, preco FROM produtos")
        for (id_p, nome, preco) in cursor.fetchall():
            card = ctk.CTkFrame(scroll, fg_color="white")
            card.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(card, text=f"{nome} | R$ {preco:.2f}", font=("Arial", 14, "bold")).pack(side="left", padx=15)
            
            def excluir_p(id_prod=id_p):
                if messagebox.askyesno("Excluir", "Deseja remover?"):
                    cur = root.conn.cursor()
                    cur.execute("DELETE FROM produtos WHERE id_produto = %s", (id_prod,))
                    root.conn.commit()
                    tela_produtos()

            ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=excluir_p).pack(side="right", padx=10)
        cursor.close()
    except: pass

# --- SIDEBAR ORIGINAL ---
sidebar = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color=COR_SIDEBAR)
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="Pizzaloop", font=("Arial", 22, "bold"), text_color=COR_TEXTO).pack(pady=30)

ctk.CTkButton(sidebar, text="Clientes", command=tela_clientes).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Produtos", command=tela_produtos).pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Sair", fg_color="#333", command=root.quit).pack(side="bottom", pady=20)

main_frame = ctk.CTkFrame(root)
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Iniciar
if root.conn:
    tela_dashboard = lambda: (limpar_main(), ctk.CTkLabel(main_frame, text="Dashboard", font=("Arial", 30)).pack(pady=50))
    tela_dashboard()
    root.mainloop()
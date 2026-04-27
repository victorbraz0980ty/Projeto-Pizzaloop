# GESTÃO DE CLIENTES (CONECTADO)
# =======================
def tela_clientes():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gestão de Clientes 👥", font=("Arial", 24, "bold")).pack(pady=20)
    
    def salvar_novo_cliente():
        form = ctk.CTkToplevel(root)
        form.geometry("400x400")
        form.attributes("-topmost", True)
        
        ent_nome = ctk.CTkEntry(form, placeholder_text="Nome", width=300); ent_nome.pack(pady=10)
        ent_tel = ctk.CTkEntry(form, placeholder_text="Telefone", width=300); ent_tel.pack(pady=10)
        ent_cpf = ctk.CTkEntry(form, placeholder_text="CPF", width=300); ent_cpf.pack(pady=10)

        def confirmar():
            try:
                cursor = root.conn.cursor()
                # SQL usando seus nomes originais: id_cliente, nome, telefone, cep, endereco, cpf
                sql = "INSERT INTO cliente (nome, telefone, cep, endereco, cpf) VALUES (%s, %s, '00000', 'Endereço', %s)"
                cursor.execute(sql, (ent_nome.get(), ent_tel.get(), ent_cpf.get()))
                root.conn.commit() # SALVA NO WORKBENCH
                cursor.close()
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")
                form.destroy()
                tela_clientes()
            except Exception as e: messagebox.showerror("Erro", str(e))

        ctk.CTkButton(form, text="Salvar", fg_color=COR_BOTAO, command=confirmar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=COR_BOTAO, command=salvar_novo_cliente).pack(pady=10)

    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    try:
        cursor = root.conn.cursor()
        cursor.execute("SELECT id_cliente, nome, telefone FROM cliente")
        for (id_c, nome, tel) in cursor.fetchall():
            card = ctk.CTkFrame(scroll, fg_color="white")
            card.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(card, text=f"{nome} | {tel}", font=("Arial", 14, "bold")).pack(side="left", padx=15)
            
            def excluir(id_cli=id_c):
                if messagebox.askyesno("Excluir", "Deseja remover?"):
                    cur = root.conn.cursor()
                    cur.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cli,))
                    root.conn.commit()
                    tela_clientes()

            ctk.CTkButton(card, text="Excluir", fg_color=COR_EXCLUIR, width=60, command=excluir).pack(side="right", padx=10)
        cursor.close()
    except: pass
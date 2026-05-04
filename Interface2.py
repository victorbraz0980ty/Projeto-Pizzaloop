import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ========================
# PALETA DE CORES
# ========================
ORANGE     = "#ff6b00"
ORANGE_L   = "#fff3ea"
SIDEBAR    = "#0f172a"
SIDEBAR_H  = "#1e293b"
BG         = "#f1f5f9"
CARD       = "#ffffff"
CARD_BRD   = "#e2e8f0"
BLUE       = "#2563eb"
BLUE_L     = "#eff6ff"
GREEN      = "#16a34a"
GREEN_L    = "#f0fdf4"
PURPLE     = "#7c3aed"
PURPLE_L   = "#f5f3ff"
RED        = "#dc2626"
RED_L      = "#fef2f2"
GRAY       = "#64748b"
DARK       = "#0f172a"
TEXT       = "#1e293b"
TEXT_S     = "#64748b"

# ========================
# APP PRINCIPAL
# ========================
app = ctk.CTk()
app.geometry("1280x780")
app.title("Pizza Loop – Sistema de Gestão")
app.resizable(True, True)

# ========================
# SIDEBAR
# ========================
sidebar = ctk.CTkFrame(app, width=230, fg_color=SIDEBAR, corner_radius=0)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Logo
logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
logo_frame.pack(pady=(28, 10), padx=20, fill="x")
ctk.CTkLabel(logo_frame, text="🍕", font=("Arial", 28)).pack(side="left")
ctk.CTkLabel(logo_frame, text="Pizza Loop🍕",
             font=("Arial", 18, "bold"), text_color="white").pack(side="left", padx=8)

ctk.CTkFrame(sidebar, height=1, fg_color="#1e293b").pack(fill="x", padx=20, pady=(0, 10))

# ========================
# FRAME PRINCIPAL
# ========================
main_frame = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
main_frame.pack(side="left", fill="both", expand=True)

def limpar_main():
    for w in main_frame.winfo_children():
        w.destroy()

# ========================
# HELPERS DE UI
# ========================
def card(parent, **kw):
    defaults = dict(fg_color=CARD, corner_radius=12,
                    border_width=1, border_color=CARD_BRD)
    defaults.update(kw)
    return ctk.CTkFrame(parent, **defaults)

def badge(parent, text, bg, fg):
    f = ctk.CTkFrame(parent, fg_color=bg, corner_radius=6)
    ctk.CTkLabel(f, text=text, font=("Arial", 11, "bold"),
                 text_color=fg).pack(padx=8, pady=2)
    return f

def section_title(parent, text):
    ctk.CTkLabel(parent, text=text, font=("Arial", 22, "bold"),
                 text_color=DARK).pack(anchor="w", padx=30, pady=(22, 6))

def divider(parent):
    ctk.CTkFrame(parent, height=1, fg_color=CARD_BRD).pack(fill="x", padx=30, pady=4)

# ========================
# TELA: DASHBOARD
# ========================
def tela_dashboard():
    limpar_main()
    section_title(main_frame, "Painel de Controle")
    divider(main_frame)

    # ── Métricas ──────────────────────────────────────
    metrics_row = ctk.CTkFrame(main_frame, fg_color="transparent")
    metrics_row.pack(fill="x", padx=30, pady=(10, 0))

    metrics = [
        ("Vendas Hoje",       "R$ 1.250,50", ORANGE,  ORANGE_L,  "↑ 12% vs ontem"),
        ("Pedidos",           "15",          BLUE,    BLUE_L,    "3 em andamento"),
        ("Ticket Médio",      "R$ 83,37",    GREEN,   GREEN_L,   "↑ 5% esta semana"),
        ("Clientes Ativos",   "120",         PURPLE,  PURPLE_L,  "8 novos hoje"),
    ]
    for titulo, valor, cor, bg, sub in metrics:
        c = ctk.CTkFrame(metrics_row, fg_color=CARD, corner_radius=12,
                         border_width=1, border_color=CARD_BRD, width=260, height=110)
        c.pack(side="left", padx=(0, 12), expand=True)
        c.pack_propagate(False)
        ctk.CTkLabel(c, text=titulo, font=("Arial", 12), text_color=TEXT_S).place(x=16, y=14)
        ctk.CTkLabel(c, text=valor,  font=("Arial", 24, "bold"), text_color=cor).place(x=16, y=36)
        ctk.CTkLabel(c, text=sub,    font=("Arial", 11), text_color=TEXT_S).place(x=16, y=78)
        acc = ctk.CTkFrame(c, width=4, fg_color=cor, corner_radius=2, height=80)
        acc.place(x=0, y=16)

    # ── Linha do meio ─────────────────────────────────
    mid = ctk.CTkFrame(main_frame, fg_color="transparent")
    mid.pack(fill="both", expand=True, padx=30, pady=12)

    # Pedidos recentes
    p_card = card(mid)
    p_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    ctk.CTkLabel(p_card, text="Pedidos Recentes",
                 font=("Arial", 14, "bold"), text_color=DARK).pack(anchor="w", padx=16, pady=(14, 4))

    pedidos = [
        (101, "João Silva",     75.50,  "Entregue",    GREEN,  GREEN_L),
        (102, "Maria Santos",   45.00,  "Em preparo",  ORANGE, ORANGE_L),
        (103, "Pedro Oliveira", 120.00, "Saiu p/ entrega", BLUE, BLUE_L),
        (104, "Ana Costa",      88.00,  "Aguardando",  GRAY,  "#f1f5f9"),
    ]
    for pid, nome, val, status, cor, bg in pedidos:
        row = ctk.CTkFrame(p_card, fg_color="#f8fafc", corner_radius=8)
        row.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(row, text=f"#{pid}", font=("Arial", 12, "bold"),
                     text_color=ORANGE).pack(side="left", padx=(10, 6), pady=8)
        ctk.CTkLabel(row, text=nome, font=("Arial", 12),
                     text_color=TEXT).pack(side="left")
        b = ctk.CTkFrame(row, fg_color=bg, corner_radius=6)
        b.pack(side="right", padx=10, pady=8)
        ctk.CTkLabel(b, text=status, font=("Arial", 10, "bold"),
                     text_color=cor).pack(padx=8, pady=2)
        ctk.CTkLabel(row, text=f"R$ {val:.2f}", font=("Arial", 12, "bold"),
                     text_color=DARK).pack(side="right", padx=8)

    # Mais vendidas
    v_card = card(mid)
    v_card.pack(side="left", fill="both", expand=True, padx=(10, 0))
    ctk.CTkLabel(v_card, text="Mais Vendidas",
                 font=("Arial", 14, "bold"), text_color=DARK).pack(anchor="w", padx=16, pady=(14, 4))

    pizzas = [
        ("Calabresa Especial", 25, ORANGE),
        ("Portuguesa",         18, BLUE),
        ("Margherita",         15, GREEN),
        ("Frango c/ Catupiry", 12, PURPLE),
    ]
    for i, (nome, qtd, cor) in enumerate(pizzas, 1):
        row = ctk.CTkFrame(v_card, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=6)
        rank = ctk.CTkFrame(row, fg_color=cor, corner_radius=6, width=28, height=28)
        rank.pack(side="left", padx=(0, 10))
        rank.pack_propagate(False)
        ctk.CTkLabel(rank, text=str(i), font=("Arial", 12, "bold"),
                     text_color="white").pack(expand=True)
        ctk.CTkLabel(row, text=nome, font=("Arial", 12),
                     text_color=TEXT).pack(side="left")
        ctk.CTkLabel(row, text=f"{qtd} un.", font=("Arial", 12, "bold"),
                     text_color=cor).pack(side="right")
        bar_bg = ctk.CTkFrame(v_card, height=5, fg_color="#e2e8f0", corner_radius=3)
        bar_bg.pack(fill="x", padx=16, pady=(0, 2))
        pct = qtd / 25
        bar_fill = ctk.CTkFrame(v_card, height=5, fg_color=cor, corner_radius=3,
                                width=int(pct * 240))
        bar_fill.place_configure()

    # ── Pagamentos ────────────────────────────────────
    pay_card = card(main_frame)
    pay_card.pack(fill="x", padx=30, pady=(0, 20))
    ctk.CTkLabel(pay_card, text="Métodos de Pagamento",
                 font=("Arial", 14, "bold"), text_color=DARK).pack(anchor="w", padx=16, pady=(14, 6))

    metodos = [("PIX", 0.50, GREEN), ("Cartão de Crédito", 0.30, BLUE), ("Dinheiro", 0.20, ORANGE)]
    for nome, pct, cor in metodos:
        r = ctk.CTkFrame(pay_card, fg_color="transparent")
        r.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(r, text=f"{nome}  {int(pct*100)}%", font=("Arial", 12),
                     text_color=TEXT).pack(side="left")
        pb = ctk.CTkProgressBar(r, height=8, corner_radius=4, progress_color=cor,
                                fg_color="#e2e8f0")
        pb.pack(side="right", fill="x", expand=True, padx=(20, 0))
        pb.set(pct)

# ========================
# TELA: PEDIDOS
# ========================
def tela_pedidos():
    limpar_main()
    section_title(main_frame, "Gestão de Pedidos")
    divider(main_frame)

    # Filtros
    filt = ctk.CTkFrame(main_frame, fg_color="transparent")
    filt.pack(fill="x", padx=30, pady=(10, 0))

    for label, cor, bg in [("Todos", DARK, "#e2e8f0"), ("Em Preparo", ORANGE, ORANGE_L),
                            ("Saiu p/ Entrega", BLUE, BLUE_L), ("Entregue", GREEN, GREEN_L),
                            ("Cancelado", RED, RED_L)]:
        b = ctk.CTkButton(filt, text=label, fg_color=bg, text_color=cor,
                          hover_color=CARD_BRD, corner_radius=8, width=130, height=32,
                          font=("Arial", 12, "bold"), border_width=0)
        b.pack(side="left", padx=(0, 8))

    # Tabela de pedidos
    t_card = card(main_frame)
    t_card.pack(fill="both", expand=True, padx=30, pady=14)

    headers = ["Pedido", "Cliente", "Itens", "Total", "Status", "Hora", "Ação"]
    header_row = ctk.CTkFrame(t_card, fg_color="#f8fafc", corner_radius=8)
    header_row.pack(fill="x", padx=12, pady=(10, 4))
    widths = [70, 180, 200, 90, 130, 80, 80]
    for h, w in zip(headers, widths):
        ctk.CTkLabel(header_row, text=h, font=("Arial", 11, "bold"),
                     text_color=TEXT_S, width=w, anchor="w").pack(side="left", padx=6, pady=8)

    pedidos = [
        (105, "Lucas Mendes",    "2x Calabresa",        112.00, "Em preparo",       "14:32", ORANGE, ORANGE_L),
        (104, "Ana Costa",       "1x Margherita",         45.00, "Aguardando",       "14:18", GRAY,   "#f1f5f9"),
        (103, "Pedro Oliveira",  "3x Portuguesa",        135.00, "Saiu p/ entrega",  "13:55", BLUE,   BLUE_L),
        (102, "Maria Santos",    "1x Frango+Cat",         55.00, "Entregue",         "13:10", GREEN,  GREEN_L),
        (101, "João Silva",      "2x Calabresa+1xRefri",  75.50, "Entregue",         "12:47", GREEN,  GREEN_L),
    ]
    for pid, cli, itens, total, status, hora, cor, bg in pedidos:
        row = ctk.CTkFrame(t_card, fg_color=CARD, corner_radius=8,
                           border_width=1, border_color=CARD_BRD)
        row.pack(fill="x", padx=12, pady=3)
        data = [f"#{pid}", cli, itens, f"R$ {total:.2f}", "", hora, ""]
        for val, w in zip(data, widths[:-2]):
            ctk.CTkLabel(row, text=val, font=("Arial", 12), text_color=TEXT,
                         width=w, anchor="w").pack(side="left", padx=6, pady=10)
        b = ctk.CTkFrame(row, fg_color=bg, corner_radius=6)
        b.pack(side="left", padx=6, pady=10)
        ctk.CTkLabel(b, text=status, font=("Arial", 10, "bold"),
                     text_color=cor).pack(padx=8, pady=3)
        ctk.CTkButton(row, text="Ver", width=60, height=28, corner_radius=6,
                      fg_color=ORANGE_L, text_color=ORANGE,
                      hover_color=CARD_BRD, font=("Arial", 11, "bold"),
                      border_width=0).pack(side="left", padx=10)

    # Botão novo pedido
    ctk.CTkButton(main_frame, text="+ Novo Pedido", fg_color=ORANGE,
                  hover_color="#e55f00", text_color="white",
                  font=("Arial", 13, "bold"), corner_radius=10,
                  width=160, height=40).pack(anchor="e", padx=30, pady=(0, 16))

# ========================
# TELA: CARDÁPIO
# ========================
def tela_cardapio():
    limpar_main()
    section_title(main_frame, "Cardápio")
    divider(main_frame)

    # Categorias
    cat_row = ctk.CTkFrame(main_frame, fg_color="transparent")
    cat_row.pack(fill="x", padx=30, pady=(10, 0))
    for cat, ativo in [("Todas", True), ("Tradicionais", False), ("Especiais", False),
                       ("Veganas", False), ("Bebidas", False)]:
        fg  = ORANGE if ativo else "#e2e8f0"
        txt = "white" if ativo else TEXT_S
        ctk.CTkButton(cat_row, text=cat, fg_color=fg, text_color=txt,
                      hover_color=ORANGE_L, corner_radius=20, width=110, height=32,
                      font=("Arial", 12), border_width=0).pack(side="left", padx=(0, 8))

    # Grade de pizzas
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=30, pady=14)

    pizzas = [
        ("Calabresa Especial",  "Molho, mozzarella, calabresa, cebola",  42.90, "Tradicional", True),
        ("Portuguesa",          "Presunto, ovo, azeitona, cebola",        44.90, "Tradicional", True),
        ("Margherita",          "Molho, mozzarella, tomate, manjericão",  39.90, "Tradicional", False),
        ("Frango c/ Catupiry",  "Frango desfiado, catupiry, milho",       46.90, "Especial",    True),
        ("Vegana Verde",        "Abobrinha, pimentão, tomate seco",       43.90, "Vegana",      False),
        ("Quatro Queijos",      "Mozzarella, parmesão, provolone, gorgonzola", 49.90, "Especial", True),
    ]

    cols = 3
    for i, (nome, desc, preco, cat, ativo) in enumerate(pizzas):
        r, c = divmod(i, cols)
        p_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=14,
                              border_width=1, border_color=CARD_BRD, width=310, height=170)
        p_card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
        p_card.pack_propagate(False)
        scroll.grid_columnconfigure(c, weight=1)

        top = ctk.CTkFrame(p_card, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(14, 2))
        ctk.CTkLabel(top, text=nome, font=("Arial", 13, "bold"),
                     text_color=DARK).pack(side="left")
        cat_badge = ctk.CTkFrame(top, fg_color=PURPLE_L, corner_radius=6)
        cat_badge.pack(side="right")
        ctk.CTkLabel(cat_badge, text=cat, font=("Arial", 10, "bold"),
                     text_color=PURPLE).pack(padx=6, pady=2)

        ctk.CTkLabel(p_card, text=desc, font=("Arial", 11), text_color=TEXT_S,
                     wraplength=260, justify="left").pack(anchor="w", padx=14, pady=4)

        bot = ctk.CTkFrame(p_card, fg_color="transparent")
        bot.pack(fill="x", padx=14, pady=(6, 12))
        ctk.CTkLabel(bot, text=f"R$ {preco:.2f}", font=("Arial", 16, "bold"),
                     text_color=ORANGE).pack(side="left")
        sw_color = GREEN if ativo else GRAY
        sw_text  = "● Ativo" if ativo else "○ Inativo"
        ctk.CTkLabel(bot, text=sw_text, font=("Arial", 11, "bold"),
                     text_color=sw_color).pack(side="right")
        ctk.CTkButton(bot, text="Editar", width=70, height=28, corner_radius=6,
                      fg_color=BLUE_L, text_color=BLUE,
                      hover_color=CARD_BRD, font=("Arial", 11), border_width=0).pack(side="right", padx=8)

    ctk.CTkButton(main_frame, text="+ Adicionar Pizza", fg_color=ORANGE,
                  hover_color="#e55f00", text_color="white",
                  font=("Arial", 13, "bold"), corner_radius=10,
                  width=180, height=40).pack(anchor="e", padx=30, pady=(0, 16))

# ========================
# TELA: CLIENTES
# ========================
def tela_clientes():
    limpar_main()
    section_title(main_frame, "Gestão de Clientes")
    divider(main_frame)

    # Busca
    search_row = ctk.CTkFrame(main_frame, fg_color="transparent")
    search_row.pack(fill="x", padx=30, pady=(10, 0))
    ctk.CTkEntry(search_row, placeholder_text="🔍  Buscar cliente...",
                 width=300, height=36, corner_radius=8,
                 fg_color=CARD, border_color=CARD_BRD).pack(side="left")
    ctk.CTkButton(search_row, text="Filtrar", fg_color=BLUE, text_color="white",
                  hover_color="#1d4ed8", corner_radius=8, width=90, height=36,
                  font=("Arial", 12)).pack(side="left", padx=10)

    # Cards de clientes
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=30, pady=14)

    clientes = [
        ("João Silva",      "joao@email.com",   "(11) 99999-0001", 12, 745.00,  "Ouro",    "#f59e0b", "#fffbeb"),
        ("Maria Santos",    "maria@email.com",  "(11) 99999-0002",  8, 380.00,  "Prata",   GRAY,      "#f8fafc"),
        ("Pedro Oliveira",  "pedro@email.com",  "(11) 99999-0003", 20, 1240.00, "Diamante", BLUE,     BLUE_L),
        ("Ana Costa",       "ana@email.com",    "(11) 99999-0004",  3, 135.00,  "Bronze",  "#b45309", "#fffbeb"),
        ("Lucas Mendes",    "lucas@email.com",  "(11) 99999-0005", 15, 870.00,  "Ouro",    "#f59e0b", "#fffbeb"),
    ]

    for nome, email, tel, pedidos, gasto, nivel, cor, bg in clientes:
        c = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=12,
                         border_width=1, border_color=CARD_BRD)
        c.pack(fill="x", pady=5)

        # Avatar inicial
        ini = nome[0]
        av = ctk.CTkFrame(c, fg_color=bg, corner_radius=24, width=48, height=48)
        av.pack(side="left", padx=14, pady=14)
        av.pack_propagate(False)
        ctk.CTkLabel(av, text=ini, font=("Arial", 18, "bold"),
                     text_color=cor).pack(expand=True)

        info = ctk.CTkFrame(c, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=14)
        ctk.CTkLabel(info, text=nome, font=("Arial", 13, "bold"),
                     text_color=DARK).pack(anchor="w")
        ctk.CTkLabel(info, text=f"{email}  ·  {tel}",
                     font=("Arial", 11), text_color=TEXT_S).pack(anchor="w")

        stats = ctk.CTkFrame(c, fg_color="transparent")
        stats.pack(side="right", padx=20, pady=14)
        ctk.CTkLabel(stats, text=f"{pedidos} pedidos",
                     font=("Arial", 11), text_color=TEXT_S).pack(anchor="e")
        ctk.CTkLabel(stats, text=f"R$ {gasto:.2f}",
                     font=("Arial", 13, "bold"), text_color=DARK).pack(anchor="e")
        nb = ctk.CTkFrame(stats, fg_color=bg, corner_radius=6)
        nb.pack(anchor="e", pady=4)
        ctk.CTkLabel(nb, text=nivel, font=("Arial", 10, "bold"),
                     text_color=cor).pack(padx=8, pady=2)

    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=ORANGE,
                  hover_color="#e55f00", text_color="white",
                  font=("Arial", 13, "bold"), corner_radius=10,
                  width=160, height=40).pack(anchor="e", padx=30, pady=(0, 16))

# ========================
# TELA: RELATÓRIOS
# ========================
def exportar_pdf():
    try:
        doc = SimpleDocTemplate("relatorio_pizza_loop.pdf")
        styles = getSampleStyleSheet()

        conteudo = []

        conteudo.append(Paragraph("Relatório - Pizza Loop", styles['Title']))
        conteudo.append(Spacer(1, 12))

        conteudo.append(Paragraph("Faturamento: R$ 8.754,30", styles['Normal']))
        conteudo.append(Paragraph("Total de Pedidos: 94", styles['Normal']))
        conteudo.append(Paragraph("Ticket Médio: R$ 93,13", styles['Normal']))
        conteudo.append(Paragraph("Cancelamentos: 3", styles['Normal']))

        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph("Relatório gerado automaticamente pelo sistema.", styles['Italic']))

        doc.build(conteudo)

        print("PDF gerado com sucesso!")

    except Exception as e:
        print("Erro ao gerar PDF:", e)

def tela_relatorios():
    limpar_main()
    section_title(main_frame, "Relatórios e Análises")
    divider(main_frame)

    # Período
    per_row = ctk.CTkFrame(main_frame, fg_color="transparent")
    per_row.pack(fill="x", padx=30, pady=(10, 0))
    for p, ativo in [("Hoje", True), ("7 dias", False), ("30 dias", False), ("Mês atual", False)]:
        fg  = ORANGE if ativo else "#e2e8f0"
        txt = "white" if ativo else TEXT_S
        ctk.CTkButton(per_row, text=p, fg_color=fg, text_color=txt,
                      hover_color=ORANGE_L, corner_radius=8, width=100, height=32,
                      font=("Arial", 12), border_width=0).pack(side="left", padx=(0, 6))

    # KPIs
    kpi_row = ctk.CTkFrame(main_frame, fg_color="transparent")
    kpi_row.pack(fill="x", padx=30, pady=14)
    kpis = [
        ("Faturamento",   "R$ 8.754,30", ORANGE, ORANGE_L, "↑ 18% vs período anterior"),
        ("Total Pedidos", "94",          BLUE,   BLUE_L,   "Média: 13,4/dia"),
        ("Ticket Médio",  "R$ 93,13",    GREEN,  GREEN_L,  "↑ 7% vs período anterior"),
        ("Cancelamentos", "3",           RED,    RED_L,    "Taxa: 3,2%"),
    ]
    for titulo, valor, cor, bg, sub in kpis:
        kc = ctk.CTkFrame(kpi_row, fg_color=CARD, corner_radius=12,
                          border_width=2, border_color=bg, width=260, height=110)
        kc.pack(side="left", padx=(0, 12), expand=True)
        kc.pack_propagate(False)
        ctk.CTkLabel(kc, text=titulo, font=("Arial", 11), text_color=TEXT_S).place(x=14, y=12)
        ctk.CTkLabel(kc, text=valor,  font=("Arial", 24, "bold"), text_color=cor).place(x=14, y=34)
        ctk.CTkLabel(kc, text=sub,    font=("Arial", 10), text_color=TEXT_S).place(x=14, y=76)

    # Linha meio
    mid = ctk.CTkFrame(main_frame, fg_color="transparent")
    mid.pack(fill="both", expand=True, padx=30, pady=(0, 14))

    # Vendas por dia
    ven_card = card(mid)
    ven_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    ctk.CTkLabel(ven_card, text="Vendas por Dia",
                 font=("Arial", 13, "bold"), text_color=DARK).pack(anchor="w", padx=14, pady=(12, 6))

    dias = [("Seg", 820), ("Ter", 1100), ("Qua", 950), ("Qui", 1350),
            ("Sex", 1800), ("Sáb", 2100), ("Dom", 1600)]
    bar_area = ctk.CTkFrame(ven_card, fg_color="transparent")
    bar_area.pack(fill="both", expand=True, padx=14, pady=6)
    max_val = max(v for _, v in dias)
    for dia, val in dias:
        col = ctk.CTkFrame(bar_area, fg_color="transparent")
        col.pack(side="left", expand=True, fill="both")
        ctk.CTkLabel(col, text=f"R${val//100}", font=("Arial", 8),
                     text_color=TEXT_S).pack()
        h = int((val / max_val) * 100)
        bar = ctk.CTkFrame(col, fg_color=ORANGE, corner_radius=4, height=h, width=22)
        bar.pack(pady=(0, 4))
        ctk.CTkLabel(col, text=dia, font=("Arial", 10), text_color=TEXT_S).pack()

    # Top itens
    top_card = card(mid)
    top_card.pack(side="left", fill="both", expand=True, padx=(10, 0))
    ctk.CTkLabel(top_card, text="Top Itens Vendidos",
                 font=("Arial", 13, "bold"), text_color=DARK).pack(anchor="w", padx=14, pady=(12, 6))

    tops = [
        ("Calabresa Especial",  48, ORANGE),
        ("Portuguesa",          35, BLUE),
        ("Margherita",          30, GREEN),
        ("Frango c/ Cat.",      24, PURPLE),
        ("Quatro Queijos",      18, "#f59e0b"),
    ]
    for nome, qtd, cor in tops:
        r = ctk.CTkFrame(top_card, fg_color="transparent")
        r.pack(fill="x", padx=14, pady=5)
        ctk.CTkLabel(r, text=nome, font=("Arial", 12), text_color=TEXT).pack(side="left")
        ctk.CTkLabel(r, text=f"{qtd}", font=("Arial", 12, "bold"), text_color=cor).pack(side="right")
        pct = qtd / 48
        bg_bar = ctk.CTkFrame(top_card, fg_color="#e2e8f0", corner_radius=3, height=5)
        bg_bar.pack(fill="x", padx=14, pady=(0, 2))
        fill_bar = ctk.CTkFrame(bg_bar, fg_color=cor, corner_radius=3,
                                height=5, width=int(pct * 280))
        fill_bar.place(x=0, y=0)

    # Exportar
    exp_row = ctk.CTkFrame(main_frame, fg_color="transparent")
    exp_row.pack(anchor="e", padx=30, pady=(0, 16))
    ctk.CTkButton(exp_row, text="Exportar PDF", fg_color="#C0504E",
                  text_color=DARK, hover_color=CARD_BRD, corner_radius=8,
                  font=("Arial", 12), border_width=0, width=130, height=36).pack(side="left", padx=6)
 

# ========================
# SIDEBAR: BOTÕES
# ========================
menu_items = [
    ("🏠  Dashboard",   tela_dashboard),
    ("📝  Pedidos",     tela_pedidos),
    ("🍕  Cardápio",    tela_cardapio),
    ("📊  Relatórios",  tela_relatorios),
    ("👥  Clientes",    tela_clientes),
]

active_btn = None

def menu_btn(text, command):
    def on_click():
        global active_btn
        if active_btn:
            active_btn.configure(fg_color="transparent")
        btn.configure(fg_color=SIDEBAR_H)
        active_btn = btn
        command()
    btn = ctk.CTkButton(sidebar, text=text, anchor="w",
                        fg_color="transparent", hover_color=SIDEBAR_H,
                        text_color="white", font=("Arial", 13),
                        height=42, corner_radius=8, border_width=0,
                        command=on_click)
    btn.pack(fill="x", padx=14, pady=3)
    return btn

buttons = [menu_btn(t, c) for t, c in menu_items]

# Separador + Sair
ctk.CTkFrame(sidebar, height=1, fg_color="#1e293b").pack(fill="x", padx=20, pady=10, side="bottom")
ctk.CTkButton(sidebar, text="🚪  Sair", fg_color="transparent",
              hover_color="#7f1d1d", text_color="#94a3b8",
              font=("Arial", 13), height=40, corner_radius=8,
              border_width=0, anchor="w", command=app.quit).pack(
                  fill="x", padx=14, pady=(0, 16), side="bottom")

# Ativar dashboard inicial
buttons[0].configure(fg_color=SIDEBAR_H)
active_btn = buttons[0]
tela_dashboard()

app.mainloop()

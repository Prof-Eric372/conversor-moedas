import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk  # Pillow para redimensionar as bandeiras

# ------------ CONFIGURAÇÃO DAS MOEDAS ------------
MOEDAS = {
    "USD": "flags/united-states-of-america.png",
    "EUR": "flags/european.png",
    "BRL": "flags/brazil-.png",
    "GBP": "flags/united-kingdom.png",
    "JPY": "flags/japan.png"
}

historico = []
tema_atual = "light"

# ------------ FUNÇÕES DO APP ------------

def alternar_tema():
    """Alterna entre tema claro e escuro"""
    global tema_atual
    tema_atual = "dark" if tema_atual == "light" else "light"
    aplicar_estilo()

def aplicar_estilo():
    """Aplica cores conforme o tema"""
    cor_bg = "#2E2E2E" if tema_atual == "dark" else "#f4f4f4"
    cor_fg = "#FFFFFF" if tema_atual == "dark" else "#333333"
    janela.configure(bg=cor_bg)

    for widget in janela.winfo_children():
        try:
            widget.configure(bg=cor_bg, fg=cor_fg)
        except:
            pass

    lista_historico.configure(
        bg="#3a3a3a" if tema_atual == "dark" else "white",
        fg=cor_fg
    )

def converter():
    """Realiza a conversão de moedas usando a API"""
    try:
        valor = float(entrada_valor.get())
        de = combo_de.get()
        para = combo_para.get()

        if de == para:
            messagebox.showwarning("Aviso", "Escolha moedas diferentes.")
            return

        url = f"https://api.exchangerate-api.com/v4/latest/{de}"
        resposta = requests.get(url)
        dados = resposta.json()

        if "rates" not in dados:
            raise Exception("Erro na resposta da API.")

        taxa = dados["rates"].get(para)
        if taxa is None:
            raise Exception("Moeda destino inválida.")

        convertido = round(valor * taxa, 2)
        resultado_var.set(f"{valor} {de} = {convertido} {para}")
        historico.append(f"{valor} {de} → {convertido} {para}")
        atualizar_historico()

    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na conversão: {e}")

def atualizar_historico():
    """Atualiza a lista de histórico"""
    lista_historico.delete(0, tk.END)
    for item in reversed(historico[-5:]):  # Últimas 5 conversões
        lista_historico.insert(tk.END, item)

def atualizar_bandeiras(event=None):
    """Atualiza as bandeiras ao mudar as seleções"""
    cod_de = combo_de.get()
    cod_para = combo_para.get()
    label_flag_de.configure(image=flags.get(cod_de))
    label_flag_para.configure(image=flags.get(cod_para))

# ------------ INTERFACE GRÁFICA ------------

janela = tk.Tk()
janela.title("💱 Conversor de Moedas")
janela.geometry("480x560")
janela.resizable(False, False)

# 🔽 Carrega e redimensiona as bandeiras com Pillow (favicon style: 16x16)
flags = {}
for code, path in MOEDAS.items():
    img = Image.open(path).resize((16, 16), Image.Resampling.LANCZOS)
    flags[code] = ImageTk.PhotoImage(img)

# Título
tk.Label(janela, text="Conversor de Moedas", font=("Segoe UI", 16, "bold")).pack(pady=(15, 5))

# Botão de tema
btn_tema = tk.Button(janela, text="Alternar Tema 🌓", command=alternar_tema, relief="groove")
btn_tema.pack()

# Entrada do valor
tk.Label(janela, text="Valor:").pack(pady=(20, 5))
entrada_valor = tk.Entry(janela, font=("Segoe UI", 12), justify="center", width=20)
entrada_valor.pack()

# Frame das moedas (com bandeira + combo lado a lado)
frame_moedas = tk.Frame(janela)
frame_moedas.pack(pady=20)

# Moeda de origem
frame_origem = tk.Frame(frame_moedas)
frame_origem.grid(row=0, column=0, padx=20)

label_flag_de = tk.Label(frame_origem, image=flags["USD"])
label_flag_de.pack()
combo_de = ttk.Combobox(frame_origem, values=list(MOEDAS.keys()), width=10, state="readonly", justify="center")
combo_de.current(0)
combo_de.pack()

# Moeda de destino
frame_destino = tk.Frame(frame_moedas)
frame_destino.grid(row=0, column=1, padx=20)

label_flag_para = tk.Label(frame_destino, image=flags["EUR"])
label_flag_para.pack()
combo_para = ttk.Combobox(frame_destino, values=list(MOEDAS.keys()), width=10, state="readonly", justify="center")
combo_para.current(1)
combo_para.pack()

# Atualiza bandeiras ao trocar seleção
combo_de.bind("<<ComboboxSelected>>", atualizar_bandeiras)
combo_para.bind("<<ComboboxSelected>>", atualizar_bandeiras)

# Botão de converter
tk.Button(janela, text="Converter", command=converter,
          bg="#1e90ff", fg="white", font=("Segoe UI", 11, "bold"),
          width=20, relief="ridge").pack(pady=10)

# Resultado da conversão
resultado_var = tk.StringVar()
tk.Label(janela, textvariable=resultado_var,
         font=("Segoe UI", 14, "bold"), fg="green").pack(pady=10)

# Histórico
tk.Label(janela, text="Histórico de Conversões:", font=("Segoe UI", 12, "bold")).pack(pady=(15, 5))
lista_historico = tk.Listbox(janela, height=6, width=50, bd=1, relief="sunken", highlightthickness=1)
lista_historico.pack(padx=10, pady=(0, 20))

# Estilo inicial (tema claro)
aplicar_estilo()

# Inicia o app
janela.mainloop()

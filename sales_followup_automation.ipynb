import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import re
import os
from datetime import datetime

print("=====================================================")
print("  🚀 PIPELINE DE DADOS - Desenvolvido por Eduardo Maia  ")
print("=====================================================\n")

# =====================================================
# 0. AUTENTICAÇÃO ÚNICA (SESSÃO GLOBAL)
# =====================================================
EMPRESA_SESSION = input("Cole o valor de 'empresa-session': ").strip()
XSRF_TOKEN = input("Cole o valor de 'XSRF-TOKEN': ").strip()

session = requests.Session()
session.cookies.update({"XSRF-TOKEN": XSRF_TOKEN, "empresa-session": EMPRESA_SESSION})
HEADERS_GLOBAIS = {
    "Accept": "application/json, text/html, application/xhtml+xml, */*",
    "Content-Type": "application/json",
    "Origin": "https://admin.empresa.com.br",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# =====================================================
# FASE 1: VARREDURA DE CLIENTES NOVOS (DELTA SYNC)
# =====================================================
print("\n[1/4] INICIANDO FASE 1: BUSCANDO CLIENTES NOVOS...")
URL_CLIENTES = "https://admin.empresa.com.br/users"
headers_f1 = HEADERS_GLOBAIS.copy()
headers_f1["Referer"] = URL_CLIENTES

ids_conhecidos = set()
df_antigo_clientes = pd.DataFrame()

if os.path.exists("clientes_finais_limpos.csv"):
    df_antigo_clientes = pd.read_csv("clientes_finais_limpos.csv", sep=";", dtype=str)
    if "ID_INTERNO_SISTEMA" in df_antigo_clientes.columns:
        ids_conhecidos = set(df_antigo_clientes["ID_INTERNO_SISTEMA"].dropna().str.strip().tolist())
        print(f" 📦 Freio Mágico pronto: {len(ids_conhecidos)} clientes reconhecidos no disco.")
else:
    print(" ⚠️ Base de clientes não encontrada. Varredura completa iniciada.")

resposta_f1 = session.get(URL_CLIENTES, headers=headers_f1)
if resposta_f1.status_code == 200:
    soup = BeautifulSoup(resposta_f1.text, "html.parser")
    meta_token = soup.find("meta", attrs={"name": "csrf-token"})
    TOKEN_DINAMICO = meta_token["content"] if meta_token else None

    ponteiro = soup.find("table")
    while ponteiro and not ponteiro.has_attr("wire:snapshot"): ponteiro = ponteiro.parent
    SNAPSHOT_INICIAL = ponteiro["wire:snapshot"] if ponteiro else None

    if TOKEN_DINAMICO and SNAPSHOT_INICIAL:
        headers_f1["X-CSRF-TOKEN"] = TOKEN_DINAMICO
        headers_f1["X-XSRF-TOKEN"] = unquote(XSRF_TOKEN)

        payload = {"_token": TOKEN_DINAMICO, "components": [{"snapshot": SNAPSHOT_INICIAL, "updates": {}, "calls": []}]}
        resp_post = session.post("https://admin.empresa.com.br/livewire/update", json=payload, headers=headers_f1)

        if resp_post.status_code == 200:
            snapshot_atual = resp_post.json()["components"][0]["snapshot"]
            html_dinamico = resp_post.json()["components"][0]["effects"]["html"]

            historico = []
            pagina = 1

            while True:
                print(f" ➔ Lendo página {pagina} de Clientes...", end=" ")
                soup_dinamico = BeautifulSoup(html_dinamico, "html.parser")
                tabela = soup_dinamico.find("table")
                novos_na_pagina = 0

                if tabela:
                    colunas = [th.get_text(strip=True) for th in tabela.find_all("th")]
                    for tr in tabela.find_all("tr"):
                        if tr.find("th"): continue
                        celulas = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
                        if len(celulas) == len(colunas):
                            linha = dict(zip(colunas, celulas))
                            link = tr.find("a", href=True)
                            if link and "/users/" in link["href"]:
                                id_cliente = str(link["href"].split("/")[-1]).strip()
                                linha["ID_INTERNO_SISTEMA"] = id_cliente
                                if id_cliente not in ids_conhecidos:
                                    historico.append(linha)
                                    novos_na_pagina += 1

                print(f"({novos_na_pagina} novos)")
                if len(ids_conhecidos) > 0 and novos_na_pagina == 0:
                    print(" 🏁 [DELTA] Histórico alcançado. Parando Fase 1.")
                    break

                btn_prox = soup_dinamico.find(lambda tag: tag.has_attr('wire:click') and 'nextPage' in tag['wire:click'])
                if not btn_prox or btn_prox.has_attr('disabled'): break

                pagina += 1
                payload_prox = {"_token": TOKEN_DINAMICO, "components": [{"snapshot": snapshot_atual, "updates": {}, "calls": [{"path": "", "method": "nextPage", "params": ["page"]}]}]}
                resp_post = session.post("https://admin.empresa.com.br/livewire/update", json=payload_prox, headers=headers_f1)
                snapshot_atual = resp_post.json()["components"][0]["snapshot"]
                html_dinamico = resp_post.json()["components"][0]["effects"]["html"]
                time.sleep(0.4)

            if historico:
                df_novos = pd.DataFrame(historico)
                df_consolidado = pd.concat([df_novos, df_antigo_clientes], ignore_index=True).drop_duplicates(subset=["ID_INTERNO_SISTEMA"], keep="first")
                df_consolidado.to_csv("clientes_finais_limpos.csv", sep=";", encoding="utf-8-sig", index=False)
                print(f" 💾 Salvo! {len(df_novos)} novos clientes adicionados.")
            else:
                print(" ℹ️ Nenhum cliente novo na base.")

# =====================================================
# FASE 1.5: GATILHO VIP (ATUALIZAÇÃO DE PEDIDOS GLOBAIS)
# =====================================================
print("\n[2/4] INICIANDO FASE 1.5: BUSCANDO RECOMPRAS (VIPs)...")
URL_PEDIDOS = "https://admin.empresa.com.br/orders"
headers_f15 = HEADERS_GLOBAIS.copy()
headers_f15["Referer"] = URL_PEDIDOS

ids_pedidos_conhecidos = set()
df_pedidos_antigos = pd.DataFrame()

if os.path.exists("pedidos_finais_limpos.csv"):
    df_pedidos_antigos = pd.read_csv("pedidos_finais_limpos.csv", sep=";", dtype=str)
    coluna_id = next((c for c in ["ID_INTERNO_SISTEMA", "ID_PEDIDO_SISTEMA", "ID_PEDIDO", "ID"] if c in df_pedidos_antigos.columns), None)

    if coluna_id:
        ids_pedidos_conhecidos = set(df_pedidos_antigos[coluna_id].dropna().astype(str).str.strip().tolist())
        print(f" 📦 Freio Mágico de Pedidos pronto: {len(ids_pedidos_conhecidos)} pedidos reconhecidos no disco.")

df_perfis_para_match = pd.DataFrame()
if os.path.exists("perfil_clientes_profundo.csv"):
    df_perfis_para_match = pd.read_csv("perfil_clientes_profundo.csv", sep=";", low_memory=False)

fila_vip = []
resposta_f15 = session.get(URL_PEDIDOS, headers=headers_f15)

if resposta_f15.status_code == 200:
    soup = BeautifulSoup(resposta_f15.text, "html.parser")
    meta_token = soup.find("meta", attrs={"name": "csrf-token"})
    TOKEN_DINAMICO = meta_token["content"] if meta_token else None

    ponteiro = soup.find("table")
    while ponteiro and not ponteiro.has_attr("wire:snapshot"): ponteiro = ponteiro.parent
    SNAPSHOT_INICIAL = ponteiro["wire:snapshot"] if ponteiro else None

    if TOKEN_DINAMICO and SNAPSHOT_INICIAL:
        headers_f15["X-CSRF-TOKEN"] = TOKEN_DINAMICO
        headers_f15["X-XSRF-TOKEN"] = unquote(XSRF_TOKEN)

        payload = {"_token": TOKEN_DINAMICO, "components": [{"snapshot": SNAPSHOT_INICIAL, "updates": {}, "calls": []}]}
        resp_post = session.post("https://admin.empresa.com.br/livewire/update", json=payload, headers=headers_f15)

        if resp_post.status_code == 200:
            snapshot_atual = resp_post.json()["components"][0]["snapshot"]
            html_dinamico = resp_post.json()["components"][0]["effects"]["html"]

            historico_pedidos = []
            nomes_recentes = set()
            pagina = 1

            while True:
                print(f" ➔ Lendo página {pagina} de Pedidos...", end=" ")
                soup_dinamico = BeautifulSoup(html_dinamico, "html.parser")
                tabela = soup_dinamico.find("table")
                novos_na_pagina = 0

                if tabela:
                    colunas = [th.get_text(strip=True) for th in tabela.find_all("th")]
                    for tr in tabela.find_all("tr"):
                        if tr.find("th"): continue
                        celulas = [td.get_text(" ", strip=True) for td in tr.find_all("td")]

                        if len(celulas) > 0:
                            qtd_minima = min(len(colunas), len(celulas))
                            linha = dict(zip(colunas[:qtd_minima], celulas[:qtd_minima]))
                            
                            id_pedido = None
                            for lnk in tr.find_all("a", href=True):
                                if "/orders/" in lnk["href"]:
                                    id_pedido = str(lnk["href"].split("/")[-1]).strip()
                                    break
                            if not id_pedido and "ID" in linha and linha["ID"]:
                                id_pedido = str(linha["ID"]).strip()

                            if id_pedido:
                                linha["ID_INTERNO_SISTEMA"] = id_pedido
                                if id_pedido not in ids_pedidos_conhecidos:
                                    historico_pedidos.append(linha)
                                    novos_na_pagina += 1
                                    if linha.get("CLIENTE"):
                                        nomes_recentes.add(re.split(r'\(|\n', linha["CLIENTE"])[0].strip())

                print(f"({novos_na_pagina} novos)")
                if len(ids_pedidos_conhecidos) > 0 and novos_na_pagina == 0:
                    print(" 🏁 [DELTA] Histórico alcançado. Parando Fase 1.5.")
                    break

                btn_prox = soup_dinamico.find(lambda tag: tag.has_attr('wire:click') and 'nextPage' in tag['wire:click'])
                if not btn_prox or btn_prox.has_attr('disabled'): break

                pagina += 1
                payload_prox = {"_token": TOKEN_DINAMICO, "components": [{"snapshot": snapshot_atual, "updates": {}, "calls": [{"path": "", "method": "nextPage", "params": ["page"]}]}]}
                resp_post = session.post("https://admin.empresa.com.br/livewire/update", json=payload_prox, headers=headers_f15)
                snapshot_atual = resp_post.json()["components"][0]["snapshot"]
                html_dinamico = resp_post.json()["components"][0]["effects"]["html"]
                time.sleep(0.4)

            if historico_pedidos:
                df_novos = pd.DataFrame(historico_pedidos)
                colunas_limpas = [c for c in df_novos.columns if "CONTROLE_SISTEMA" not in c]
                df_novos = df_novos[colunas_limpas]
                if "ID_INTERNO_SISTEMA" in df_novos.columns: df_novos["ID_INTERNO_SISTEMA"] = df_novos["ID_INTERNO_SISTEMA"].astype(str)

                df_pedidos_consolidado = pd.concat([df_novos, df_pedidos_antigos], ignore_index=True)
                coluna_desduplicar = "ID_INTERNO_SISTEMA" if "ID_INTERNO_SISTEMA" in df_pedidos_consolidado.columns else "ID"
                df_pedidos_consolidado = df_pedidos_consolidado.drop_duplicates(subset=[coluna_desduplicar], keep="first")

                df_pedidos_consolidado.to_csv("pedidos_finais_limpos.csv", sep=";", encoding="utf-8-sig", index=False)
                print(f" 💾 Salvo! {len(df_novos)} pedidos novos adicionados.")
            else:
                print(" ℹ️ Nenhum pedido novo pra salvar.")

            if nomes_recentes and not df_perfis_para_match.empty:
                df_perfis_para_match['NOME_UPPER'] = df_perfis_para_match['NOME'].astype(str).str.upper().str.strip()
                fila_vip = df_perfis_para_match[df_perfis_para_match['NOME_UPPER'].isin([n.upper() for n in nomes_recentes])]['ID_INTERNO_SISTEMA'].tolist()
                print(f" 🚀 Fila VIP: {len(fila_vip)} clientes antigos fizeram recompras!")

# =====================================================
# FASE 2: DEFINIÇÃO DA FILA E RASPAGEM DE PERFIS
# =====================================================
print("\n[3/4] INICIANDO FASE 2: EXTRAÇÃO PROFUNDA DE PERFIS E PEDIDOS...")

if not os.path.exists("clientes_finais_limpos.csv"):
    print(" ❌ ERRO FATAL: O arquivo 'clientes_finais_limpos.csv' não foi gerado.")
    import sys
    sys.exit()

df_lista_consolidada = pd.read_csv("clientes_finais_limpos.csv", sep=";")
ids_totais_alvo = df_lista_consolidada["ID_INTERNO_SISTEMA"].dropna().astype(int).unique()

perfis_consolidados = []
todos_pedidos = []
ids_ja_processados = set()

if os.path.exists("perfil_clientes_profundo.csv"):
    df_perfis_antigos = pd.read_csv("perfil_clientes_profundo.csv", sep=";", low_memory=False)
    df_perfis_antigos["ID_INTERNO_SISTEMA"] = df_perfis_antigos["ID_INTERNO_SISTEMA"].astype(int)
    ids_ja_processados = set(df_perfis_antigos["ID_INTERNO_SISTEMA"].tolist())
    perfis_consolidados = df_perfis_antigos.to_dict('records')

if os.path.exists("pedidos_clientes.csv"):
    df_ped_relacionais = pd.read_csv("pedidos_clientes.csv", sep=";", dtype=str)
    todos_pedidos = df_ped_relacionais.to_dict('records')

ids_novos = [int(uid) for uid in ids_totais_alvo if int(uid) not in ids_ja_processados]

fila_vip = fila_vip if 'fila_vip' in locals() else []
if fila_vip:
    perfis_consolidados = [p for p in perfis_consolidados if int(p.get('ID_INTERNO_SISTEMA', 0)) not in fila_vip]
    todos_pedidos = [p for p in todos_pedidos if str(p.get('ID_CLIENTE', 0)) not in [str(v) for v in fila_vip]]

ids_para_processar = list(set(ids_novos + fila_vip))
print(f" 🎯 Alvo: {len(ids_novos)} novos + {len(fila_vip)} recompras = {len(ids_para_processar)} perfis a raspar.")

for i, user_id in enumerate(ids_para_processar, 1):
    url_perfil = f"https://admin.empresa.com.br/users/{user_id}"
    print(f" ➔ [{i}/{len(ids_para_processar)}] Minerando perfil {user_id}...", end=" ")

    sucesso = False
    tentativas = 0

    while tentativas < 3 and not sucesso:
        try:
            resp = session.get(url_perfil, headers=HEADERS_GLOBAIS, timeout=15)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                
                nome_tag = soup.find('h2')
                nome_cliente = nome_tag.get_text(strip=True) if nome_tag else "Nome_Nao_Encontrado"

                email, telefone, doc_cpf = "", "", ""
                if nome_tag and nome_tag.parent:
                    for span in nome_tag.parent.find_all('span'):
                        texto = span.get_text(strip=True)
                        if '@' in texto and '.' in texto: email = texto
                        elif re.search(r'\(\d{2}\)\s?\d{4,5}-\d{4}', texto): telefone = texto
                        elif re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto): doc_cpf = texto

                qtd_pedidos, qtd_anamneses = 0, 0
                for t in soup.find_all('table'):
                    if 'PEDIDO' in t.text.upper():
                        qtd_pedidos = max(0, len(t.find_all('tr')) - 1)
                        break

                texto_pagina = soup.get_text(separator=' ')
                match_anamnese = re.search(r'(\d+)\s*questionário\(s\)\s*preenchido\(s\)', texto_pagina, re.IGNORECASE)
                if match_anamnese:
                    qtd_anamneses = int(match_anamnese.group(1))

                # --- 🎯 MÁGICA NOVA: CAPTURAR DATA DA ANAMNESE MAIS RECENTE ---
                data_ultima_anamnese = ""
                aba_anamneses = soup.find(id='infolist.anamneses::tab')
                if aba_anamneses:
                    spans_data = aba_anamneses.find_all('span', class_=re.compile(r'text-gray-700'))
                    datas_encontradas = [span.get_text(strip=True) for span in spans_data if re.match(r'^\d{2}/\d{2}/\d{4}$', span.get_text(strip=True))]

                    if datas_encontradas:
                        # Ordena e garante que a data puxada é matematicamente a última (mais nova)
                        datas_obj = [datetime.strptime(d, "%d/%m/%Y") for d in datas_encontradas]
                        data_ultima_anamnese = max(datas_obj).strftime("%d/%m/%Y")

                perfil_data = {
                    "ID_INTERNO_SISTEMA": user_id,
                    "NOME": nome_cliente,
                    "EMAIL_BRUTO": email,
                    "TELEFONE_BRUTO": telefone,
                    "DOCUMENTO_BRUTO": doc_cpf,
                    "LINK_PERFIL": url_perfil,
                    "QTD_PEDIDOS": qtd_pedidos,
                    "QTD_ANAMNESES": qtd_anamneses,
                    "DATA_ULTIMA_ANAMNESE": data_ultima_anamnese
                }
                perfis_consolidados.append(perfil_data)

                # --- 2. MINERAÇÃO DA TABELA RELACIONAL DE PEDIDOS ---
                pedidos_tab = soup.find(id='infolist.pedidos::tab')
                if pedidos_tab:
                    tabela_p = pedidos_tab.find('table')
                    if tabela_p and tabela_p.find('tbody'):
                        for tr in tabela_p.find('tbody').find_all('tr'):
                            tds = tr.find_all('td')
                            if len(tds) >= 8:
                                produtos_list = [div.get_text(strip=True).replace('•', '').strip() for div in tds[4].find_all('div') if div.get_text(strip=True)]

                                todos_pedidos.append({
                                    "ID_CLIENTE": user_id,
                                    "ID_PEDIDO": tds[0].get_text(strip=True),
                                    "DATA": tds[1].get_text(strip=True),
                                    "ASSINATURA": tds[2].get_text(strip=True),
                                    "ANAMNESE": tds[3].get_text(strip=True),
                                    "PRODUTOS": " | ".join(produtos_list),
                                    "VALOR": tds[5].get_text(strip=True),
                                    "FATURA": tds[6].get_text(strip=True),
                                    "STATUS": tds[7].get_text(strip=True)
                                })

                print("✅")
                sucesso = True

            elif resp.status_code == 404:
                print(f"⚠️ Perfil {user_id} não encontrado (404). Pulando...")
                sucesso = True

            else:
                raise Exception(f"Status HTTP {resp.status_code}")

        except Exception as e:
            tentativas += 1
            time.sleep(3)
            if tentativas == 3:
                print(f"❌ Falha após 3 tentativas: {e}")
                with open("erros_raspagem.log", "a") as f:
                    f.write(f"{user_id}\n")

    if i % 50 == 0:
        pd.DataFrame(perfis_consolidados).to_csv("perfil_clientes_profundo.csv", sep=";", index=False, encoding="utf-8-sig")
        if todos_pedidos:
            pd.DataFrame(todos_pedidos).to_csv("pedidos_clientes.csv", sep=";", index=False, encoding="utf-8-sig")
        print(f"\n 💾 [BACKUP AUTOMÁTICO] Progresso salvo no perfil {i}...")

pd.DataFrame(perfis_consolidados).to_csv("perfil_clientes_profundo.csv", sep=";", index=False, encoding="utf-8-sig")
if todos_pedidos:
    pd.DataFrame(todos_pedidos).to_csv("pedidos_clientes.csv", sep=";", index=False, encoding="utf-8-sig")

# =====================================================
# FASE 3: LIMPEZA E GERAÇÃO DE RELATÓRIOS (CRM & FOLLOW-UP)
# =====================================================
print("\n[4/4] INICIANDO FASE 3: LIMPEZA E EXPORTAÇÃO EXCEL...")

if os.path.exists("perfil_clientes_profundo.csv") and os.path.exists("clientes_finais_limpos.csv"):
    df_perfis = pd.read_csv("perfil_clientes_profundo.csv", sep=";", low_memory=False)
    df_clientes = pd.read_csv("clientes_finais_limpos.csv", sep=";", dtype=str)

    df_pedidos_relacionais = pd.DataFrame()
    if os.path.exists("pedidos_clientes.csv"):
        df_pedidos_relacionais = pd.read_csv("pedidos_clientes.csv", sep=";", dtype=str)

    def extrair_texto_nome(texto):
        if pd.isna(texto): return texto
        partes = texto.split("Nome da Razão Social ")
        return partes[1].strip() if len(partes) > 1 else partes[0].strip()

    coluna_nome = next((c for c in df_clientes.columns if c.upper().strip() in ["NOME", "NOME_CLIENTE", "CLIENTE", "NOME COMPLETO"]), None)
    if not coluna_nome: coluna_nome = next((c for c in df_clientes.columns if "NOME" in c.upper() or "CLIENTE" in c.upper()), None)

    if coluna_nome: df_clientes['NOME_LIMPO'] = df_clientes[coluna_nome].apply(extrair_texto_nome)
    else: df_clientes['NOME_LIMPO'] = "Sem Nome no Cadastro"

    colunas_para_puxar = ['ID_INTERNO_SISTEMA', 'NOME_LIMPO']
    mapa_colunas_data = {}

    for col_meta in ['CRIADO EM', 'ATUALIZADO EM', 'ACESSADO EM']:
        match_col = [c for c in df_clientes.columns if c.upper().strip() == col_meta]
        if match_col:
            colunas_para_puxar.append(match_col[0])
            mapa_colunas_data[match_col[0]] = col_meta

    df_perfis['ID_INTERNO_SISTEMA'] = df_perfis['ID_INTERNO_SISTEMA'].astype(str).str.strip()
    df_clientes['ID_INTERNO_SISTEMA'] = df_clientes['ID_INTERNO_SISTEMA'].astype(str).str.strip()

    df_final = pd.merge(df_perfis, df_clientes[colunas_para_puxar], on='ID_INTERNO_SISTEMA', how='left')
    df_final.rename(columns=mapa_colunas_data, inplace=True)

    df_final['NOME_CLIENTE'] = df_final['NOME_LIMPO'].fillna(df_final['NOME'])
    if 'EMAIL_BRUTO' in df_final.columns: df_final['EMAIL'] = df_final['EMAIL_BRUTO'].astype(str).str.replace('Copiar', '').str.strip()
    if 'TELEFONE_BRUTO' in df_final.columns: df_final['TELEFONE'] = df_final['TELEFONE_BRUTO'].astype(str).str.replace('Copiar', '').str.strip()
    if 'DOCUMENTO_BRUTO' in df_final.columns: df_final['CPF_CNPJ'] = df_final['DOCUMENTO_BRUTO'].astype(str).str.replace('Copiar', '').str.strip()

    colunas_saida_excel = ['ID_INTERNO_SISTEMA', 'NOME_CLIENTE', 'EMAIL', 'TELEFONE', 'CPF_CNPJ',
                           'QTD_PEDIDOS', 'QTD_ANAMNESES', 'DATA_ULTIMA_ANAMNESE', 'CRIADO EM', 'ATUALIZADO EM', 'ACESSADO EM', 'LINK_PERFIL']

    df_base_geral = df_final[[col for col in colunas_saida_excel if col in df_final.columns]].copy()
    df_base_geral.to_excel("dados_finais_limpos.xlsx", index=False)
    print(" 🎉 Planilha mestre 'dados_finais_limpos.xlsx' gerada (Base Completa para IA/Análises).")

    if not df_pedidos_relacionais.empty:
        df_pedidos_relacionais['ID_CLIENTE'] = df_pedidos_relacionais['ID_CLIENTE'].astype(str).str.strip()
        df_ped_agg = df_pedidos_relacionais.groupby('ID_CLIENTE').agg(
            DATA_DO_ULTIMO_ENVIO=('DATA', 'first'),
            HAS_ASSINATURA=('ASSINATURA', lambda x: any(pd.notna(v) and str(v).strip() not in ['', '-', '—'] for v in x)),
            ASSINATURA_ID=('ASSINATURA', lambda x: next((str(v) for v in x if pd.notna(v) and str(v).strip() not in ['', '-', '—']), ''))
        ).reset_index()
        df_leads = pd.merge(df_base_geral, df_ped_agg, left_on='ID_INTERNO_SISTEMA', right_on='ID_CLIENTE', how='left')
    else:
        df_leads = df_base_geral.copy()
        df_leads['DATA_DO_ULTIMO_ENVIO'] = ''
        df_leads['HAS_ASSINATURA'] = False
        df_leads['ASSINATURA_ID'] = ''

    df_leads['HAS_ASSINATURA'] = df_leads['HAS_ASSINATURA'].fillna(False)
    df_leads['QTD_PEDIDOS'] = pd.to_numeric(df_leads['QTD_PEDIDOS'], errors='coerce').fillna(0)
    df_leads['QTD_ANAMNESES'] = pd.to_numeric(df_leads['QTD_ANAMNESES'], errors='coerce').fillna(0)

    df_leads['NOME CADASTRO'] = df_leads['NOME_CLIENTE']
    df_leads['EMAIL DO CLIENTE'] = df_leads.get('EMAIL', '')
    df_leads['TEL CONTATO'] = df_leads.get('TELEFONE', '')
    df_leads['ASSINATURA'] = df_leads.get('ASSINATURA_ID', '')
    df_leads['DATA DO CADASTRO'] = df_leads.get('CRIADO EM', '')
    df_leads['DATA DA ANAMNESE'] = df_leads.get('DATA_ULTIMA_ANAMNESE', '')

    # --- FUNÇÃO AUXILIAR PARA GERAR AS 6 ABAS ---
    def exportar_planilha_comercial(df_dados, nome_arquivo):
        colunas_simples_cad = ['NOME CADASTRO', 'EMAIL DO CLIENTE', 'TEL CONTATO', 'DATA DO CADASTRO']
        colunas_simples_anam = ['NOME CADASTRO', 'EMAIL DO CLIENTE', 'TEL CONTATO', 'DATA DA ANAMNESE']
        colunas_com_data = ['NOME CADASTRO', 'EMAIL DO CLIENTE', 'TEL CONTATO', 'DATA_DO_ULTIMO_ENVIO']
        colunas_com_assinatura = ['NOME CADASTRO', 'EMAIL DO CLIENTE', 'TEL CONTATO', 'DATA_DO_ULTIMO_ENVIO', 'ASSINATURA']

        df_1 = df_dados[(df_dados['QTD_PEDIDOS'] == 0) & (df_dados['QTD_ANAMNESES'] == 0)][colunas_simples_cad]
        df_2 = df_dados[(df_dados['QTD_PEDIDOS'] == 0) & (df_dados['QTD_ANAMNESES'] > 0)][colunas_simples_anam]
        df_3 = df_dados[(df_dados['QTD_PEDIDOS'] == 1) & (~df_dados['HAS_ASSINATURA'])][colunas_com_data]
        df_4 = df_dados[(df_dados['QTD_PEDIDOS'] > 1)  & (~df_dados['HAS_ASSINATURA'])][colunas_com_data]
        df_5 = df_dados[(df_dados['QTD_PEDIDOS'] == 1) & (df_dados['HAS_ASSINATURA'])][colunas_com_assinatura]
        df_6 = df_dados[(df_dados['QTD_PEDIDOS'] > 1)  & (df_dados['HAS_ASSINATURA'])][colunas_com_assinatura]

        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            df_1.to_excel(writer, sheet_name='SOMENTE CADASTRO', index=False)
            df_2.to_excel(writer, sheet_name='C ANAMNESE, S PEDIDO', index=False)
            df_3.to_excel(writer, sheet_name='1 PEDIDO AVULSO', index=False)
            df_4.to_excel(writer, sheet_name='MULTIPAS PEDIDOS AVUL', index=False)
            df_5.to_excel(writer, sheet_name='ASS. CANCELADA APÓS 1', index=False)
            df_6.to_excel(writer, sheet_name='SEM RENOVAÇÃO DE ASS.', index=False)

        print(f" 🎯 SUCESSO! Relatório '{nome_arquivo}' gerado com {len(df_dados)} leads ativos.")

    # ==============================================
    # GERAÇÃO DAS DUAS PLANILHAS COMERCIAIS
    # ==============================================
    print(" ⚙️ Construindo abas do relatório COMPLETO (Todo o Histórico)...")
    exportar_planilha_comercial(df_leads, 'Leads_FollowUp_Completo.xlsx')

    print(" ⚙️ Construindo abas do relatório DIÁRIO (Apenas o Delta de hoje)...")
    if 'ids_para_processar' in locals() and len(ids_para_processar) > 0:
        ids_hoje_str = [str(uid) for uid in ids_para_processar]
        df_leads_diario = df_leads[df_leads['ID_INTERNO_SISTEMA'].isin(ids_hoje_str)].copy()
        exportar_planilha_comercial(df_leads_diario, 'Leads_FollowUp_Diario.xlsx')
    else:
        print(" ℹ️ Não houve delta (novos leads ou VIPs) nesta execução. Gerando planilha diária vazia por segurança.")
        df_leads_diario = df_leads.head(0).copy()
        exportar_planilha_comercial(df_leads_diario, 'Leads_FollowUp_Diario.xlsx')

else:
    print(" ⚠️ Erro: Arquivos CSV não encontrados na pasta para gerar os relatórios.")

# =====================================================
# 5. RESUMO EXECUTIVO (REPORT PARA O COMERCIAL)
# =====================================================
total_clientes = len(pd.read_csv("clientes_finais_limpos.csv", sep=";"))
total_pedidos = len(pd.read_csv("pedidos_clientes.csv", sep=";"))
total_anamneses = pd.read_csv("perfil_clientes_profundo.csv", sep=";")['QTD_ANAMNESES'].sum()

delta_clientes = len(historico) if 'historico' in locals() else 0
delta_pedidos = len(historico_pedidos) if 'historico_pedidos' in locals() else 0
delta_anamneses = delta_clientes

print("\n\n=====================================================")
print("Bom dia! Segue o resumo do scraper de hoje, focado no comportamento dos novos usuários integrados à base:\n")
print(f"👤 Tabela Perfil Clientes : {total_clientes} registros acumulados (📈 +{delta_clientes} adicionados agora)")
print(f"📦 Tabela Pedidos Clientes: {total_pedidos} registros acumulados (📈 +{delta_pedidos} adicionados agora)")
print(f"📋 Tabela Anamneses       : {total_anamneses} registros acumulados (📈 +{delta_anamneses} adicionadas agora)")
print("\n💡 Contexto: Os dados extraídos refletem o Upsert da rodada, englobando tanto os novos cadastros quanto a atualização completa do histórico de clientes antigos que realizaram recompras.")
print("=====================================================")

# CRM Data Pipeline & Sales Intelligence Automation 🚀
**Desenvolvido por:** Eduardo Maia

## 📌 Sobre o Projeto
Este repositório contém um pipeline completo de Extração, Transformação e Carga (ETL) e Web Scraping, desenvolvido inteiramente em Python. O projeto nasceu da necessidade prática de eliminar tarefas manuais e resolver um gargalo comercial crítico: a falta de visibilidade diária sobre o comportamento de compra e retenção de clientes.

O script automatiza a coleta de dados de um sistema de CRM web, processa essas informações e gera relatórios segmentados. O resultado é uma ferramenta de inteligência de vendas (Sales Intelligence) que entrega dados "frescos" e acionáveis todos os dias, permitindo que as equipes comerciais foquem exclusivamente no relacionamento e na conversão.

Este projeto é um reflexo prático da aplicação de conceitos de Análise e Desenvolvimento de Sistemas para arquitetar soluções que geram impacto e otimização de processos no mundo corporativo.

## ⚙️ Arquitetura e Soluções Técnicas
O código foi estruturado para ser resiliente e de alta performance, lidando com milhares de registros de forma otimizada.

* **Autenticação e Sessão:** Gerenciamento seguro de requisições HTTP, contornando proteções dinâmicas com envio de *cookies*, *headers* personalizados e tokens CSRF (`requests`).
* **Sincronização Inteligente (Delta Sync):** Criação de uma lógica de "freio mágico" que compara os dados em disco com o servidor. O scraper identifica o histórico local e faz o *fetch* apenas de novos cadastros e recompras, reduzindo o tempo de execução e o custo computacional.
* **Web Scraping Profundo:** Extração assíncrona de dados não estruturados de páginas HTML complexas, transformando tabelas e *spans* em dados limpos de contato e comportamento (`BeautifulSoup4`).
* **Tratamento de Dados (Transform):** Limpeza, desduplicação e cruzamento de bases relacionais (Perfis vs. Pedidos) utilizando dataframes (`pandas`).
* **Automação de Relatórios (Load):** Exportação final para planilhas `.xlsx` categorizadas automaticamente em 6 diferentes estágios de funil (ex: leads sem pedido, recompras avulsas, assinaturas), entregando o dado pronto para consumo gerencial.

## 🛠️ Stack Tecnológico
* **Linguagem:** Python 3
* **Engenharia de Dados & Manipulação:** `pandas`
* **Coleta de Dados (Scraping):** `beautifulsoup4`, `requests`
* **Manipulação de Arquivos e Expressões Regulares:** `os`, `re`, `datetime`

## 🚀 Como Executar

### Pré-requisitos
```
pip install pandas requests beautifulsoup4 openpyxl
```

## Instalação e Uso

Clone este repositório:
1. Clone este repositório
```
git clone [https://github.com/SEU-USUARIO/nome-do-repositorio.git](https://github.com/am-eduardo/sales-intelligence-automator.git)][(https://github.com/SEU-USUARIO/nome-do-repositorio.git](https://github.com/am-eduardo/sales-intelligence-automator.git)
```
2. Inicie o script ```pipeline_master.py``` (ou execute a célula via Jupyter Notebook).
3. O sistema solicitará os tokens de sessão ativos (```session``` e ```XSRF-TOKEN```).
4. O pipeline executará automaticamente o fluxo de sincronização Delta e a raspagem profunda, salvando o progresso em backups ```.csv``` a cada 50 perfis processados.
5. Ao final, os arquivos ```Leads_FollowUp_Completo.xlsx``` e ```Leads_FollowUp_Diario.xlsx``` estarão disponíveis no diretório raiz.

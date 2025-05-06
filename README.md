# 📦 nfe_averis

Aplicação em Python com Streamlit para tratamento de Notas Fiscais em trânsito, baseada na integração de planilhas Averis e planilhas de emissão por fazenda.

## ✅ Funcionalidades

- Upload de planilha Averis (`averis.xlsx`)
- Upload de múltiplas planilhas de emissão por fazenda
- Filtro por ano **2025** e mês selecionado pelo usuário
- Identificação de status por NF: `em trânsito`, `Cancelada`, etc.
- Tratamento especial para notas do estado de MG
- Download da planilha tratada

## 🚀 Como rodar o projeto

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/nfe_averis.git
cd nfe_averis

# Crie e ative o ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app/main.py


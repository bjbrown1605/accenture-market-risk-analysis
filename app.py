import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# -----------------------------------------------------------------------------
# Configuração da Página do Dashboard
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Risco de Mercado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Funções de Cálculo (Reutilizando a lógica do notebook)
# -----------------------------------------------------------------------------

# Usamos o cache do Streamlit para não baixar os mesmos dados repetidamente
@st.cache_data
def get_data(tickers, start_date, end_date):
    """Busca os dados de fechamento do Yahoo Finance."""
    return yf.download(tickers, start=start_date, end=end_date)['Close'].dropna()

def calculate_returns(prices):
    """Calcula os retornos logarítmicos."""
    return np.log(prices / prices.shift(1)).dropna()

def calculate_risk_metrics(returns):
    """Calcula Volatilidade, VaR e Correlação."""
    volatilidade_anualizada = returns.std() * np.sqrt(252)
    
    confianca = 0.95
    media_retornos = returns.mean()
    desvio_padrao_retornos = returns.std()
    z_score = norm.ppf(1 - confianca)
    var_parametrico = -(media_retornos + z_score * desvio_padrao_retornos)
    
    correlacao = returns.corr()
    
    return volatilidade_anualizada, var_parametrico, correlacao

# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar) para Inputs do Usuário
# -----------------------------------------------------------------------------
st.sidebar.header('Parâmetros de Análise')

# Tickers para análise, com os 4 ativos como padrão
default_tickers = ['PETR4.SA', 'ITUB4.SA', 'MGLU3.SA', '^BVSP']
tickers_input = st.sidebar.text_input('Tickers (separados por vírgula)', ','.join(default_tickers))
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]

# Seleção de datas
end_date = datetime.date.today()
start_date_default = end_date - pd.DateOffset(months=6)
start_date = st.sidebar.date_input('Data de Início', start_date_default)
end_date = st.sidebar.date_input('Data de Fim', end_date)

# Botão para executar a análise
if st.sidebar.button('Executar Análise'):
    
    # -----------------------------------------------------------------------------
    # Lógica Principal e Exibição do Dashboard
    # -----------------------------------------------------------------------------
    
    # Mapa de cores padronizado
    color_map = {
        'PETR4.SA': 'green',
        'ITUB4.SA': 'orange',
        'MGLU3.SA': 'purple',
        '^BVSP': 'blue'
    }

    # Carregar e processar os dados
    try:
        precos = get_data(tickers, start_date, end_date)
        retornos = calculate_returns(precos)
        volatilidade, var, correlacao = calculate_risk_metrics(retornos)

        st.title('📊 Dashboard de Análise de Risco de Mercado')
        st.markdown(f"Analisando **{', '.join(tickers)}** de {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}")

        # --- 3.1. Resumo dos Indicadores ---
        st.header('Resumo dos Indicadores')
        
        cols = st.columns(len(tickers))
        for i, ticker in enumerate(tickers):
            with cols[i]:
                st.metric(label=f"Volatilidade Anualizada ({ticker})", value=f"{volatilidade[ticker]:.2%}")
                st.metric(label=f"VaR Diário 95% ({ticker})", value=f"{var[ticker]:.2%}")
        
        # --- 3.2. Análise de Desempenho ---
        st.header('Análise de Desempenho')
        
        # Gráfico de Preços com Eixo Duplo (BOA PRÁTICA)
        fig_precos = make_subplots(specs=[[{"secondary_y": True}]])
        # Adiciona as ações no eixo primário
        for ticker in tickers:
            if ticker != '^BVSP':
                fig_precos.add_trace(go.Scatter(x=precos.index, y=precos[ticker], name=f'{ticker} (R$)', line=dict(color=color_map.get(ticker))), secondary_y=False)
        # Adiciona o Ibovespa no eixo secundário
        fig_precos.add_trace(go.Scatter(x=precos.index, y=precos['^BVSP'], name='^BVSP (Pontos)', line=dict(color=color_map.get('^BVSP'))), secondary_y=True)
        fig_precos.update_layout(title_text='Série Histórica de Preços')
        fig_precos.update_yaxes(title_text='Preço Ações (R$)', secondary_y=False)
        fig_precos.update_yaxes(title_text='Pontuação ^BVSP', secondary_y=True)
        st.plotly_chart(fig_precos, use_container_width=True)

        # Gráfico de Preços Normalizados
        precos_normalizados = (precos / precos.iloc[0]) * 100
        fig_precos_normalizados = px.line(precos_normalizados, title='Desempenho Comparativo (Base 100)', color_discrete_map=color_map)
        st.plotly_chart(fig_precos_normalizados, use_container_width=True)

        # --- 3.3. Análise de Risco ---
        st.header('Análise de Risco')
        
        # Volatilidade Móvel
        vol_movel = retornos.rolling(window=21).std() * np.sqrt(252)
        fig_vol_movel = px.line(vol_movel, title='Volatilidade Móvel Anualizada (21 dias)', color_discrete_map=color_map)
        st.plotly_chart(fig_vol_movel, use_container_width=True)
        
        # Drawdown
        retorno_acumulado = (1 + retornos).cumprod()
        pico_anterior = retorno_acumulado.cummax()
        drawdown = (retorno_acumulado - pico_anterior) / pico_anterior
        fig_drawdown = go.Figure()
        for ticker in drawdown.columns:
            fig_drawdown.add_trace(go.Scatter(x=drawdown.index, y=drawdown[ticker], fill='tozeroy', mode='lines', name=ticker, line=dict(color=color_map.get(ticker))))
        fig_drawdown.update_layout(title='Drawdown dos Ativos', yaxis_title='Queda Percentual desde o Pico')
        st.plotly_chart(fig_drawdown, use_container_width=True)

        # --- 3.4. Análise Estatística ---
        st.header('Análise Estatística')
        
        col1, col2 = st.columns(2)
        with col1:
            # Heatmap de Correlação
            fig_heatmap = px.imshow(correlacao, text_auto=True, title='Heatmap de Correlação', aspect="auto")
            st.plotly_chart(fig_heatmap, use_container_width=True)
        with col2:
            # Histograma de Retornos
            retornos_melted = retornos.melt(var_name='Ticker', value_name='Retorno Diário')
            fig_hist = px.histogram(retornos_melted, x='Retorno Diário', color='Ticker', marginal='box', color_discrete_map=color_map, title='Distribuição dos Retornos Diários')
            st.plotly_chart(fig_hist, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao analisar os tickers: {e}")
        st.warning("Por favor, verifique se os tickers estão corretos e existem no Yahoo Finance (ex: PETR4.SA, ^BVSP).")

else:
    st.info('Por favor, configure os parâmetros na barra lateral e clique em "Executar Análise".')

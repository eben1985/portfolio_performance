import pandas as pd
import streamlit as st
import yfinance as yf
import numpy as np


st.header('Portfolio Performance for ETFs')
st.write("Created by: Eben Opperman for the Australian Institute of Business (AIB)")
st.info('Please use sidebar to enter ticker symbol. If sidebar is not showing expand it by using the ">" in the left top corner.')
st.divider()

with st.sidebar:
    st.header("Please insert ETF info:")
    st.divider()
    ticker = st.text_input("Insert ticker (Please only insert ETF ticker symbols)")
    ticker = ticker.capitalize()
    history_range = st.selectbox("Please select period of data (y = year):", ['1y','2y','3y','5y','10y'])

    rfr = st.number_input("Insert risk-free rate (%):")
    mr = st.number_input("Insert market return (%):")

    st.divider()
    st.markdown('''This application shows the data of a EFT in combination with a chart. 
    When scrolling down the data can be see with calculation of the **Sharp measure**, **Treynor** and **Jensens alpha**.
    Some explination and the formula is also given at the end.
    ''')
    st.divider()

    

if mr > 0:
    try:
        ticker  = yf.Ticker(ticker)
        quote_type = ticker.info["quoteType"]
        if quote_type == 'ETF':
            pass
        else:
            st.error("NOT A ETF SELECTED")
        # data1 = ticker.info
        # df1 = pd.DataFrame([data1])
        # st.dataframe(df1.T)
    except:
        st.error("Not an EFT symbol on Yahoo Finance")

    try:
        long_name = ticker.info["longName"]
        bus_sum = ticker.info["longBusinessSummary"]
        category = ticker.info["category"]
        beta3Year = ticker.info["beta3Year"]
        regularMarketPreviousClose = ticker.info["regularMarketPreviousClose"]
        regularMarketOpen = ticker.info["regularMarketOpen"]
        change = round(regularMarketOpen - regularMarketPreviousClose,2)
        change_perc = round(change/regularMarketPreviousClose*100,2)

        st.subheader(long_name)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            regularMarketOpen = round(regularMarketOpen,2)
            st.metric('Open Price:   ', regularMarketOpen, change)
        with col2:
            regularMarketPreviousClose = round(regularMarketPreviousClose,2)
            st.metric('Previous close:   ', regularMarketPreviousClose)
        with col3:
            st.metric('Change:   ', change, f'{change_perc} %')
        with col4:
            st.metric('Beta: ', beta3Year)
        st.write(bus_sum)
        st.divider()

        df_close = ticker.history(period=history_range,interval='1mo', actions=False)['Close']
        df_more = ticker.history(period=history_range,interval='1mo', actions=False)
        st.line_chart(df_close)
        st.divider()
        st.dataframe(df_more)

        df_more['Monthly_return'] = (((df_more['Close'] - df_more['Close'].shift(1)) / df_more['Close'].shift(1)))
        df_more.drop(df_more.index[-1], inplace=True)
        st.subheader('Basic Metrics')
        coll1, coll2, coll3 = st.columns(3)
        with coll1:
            er = ((df_more['Monthly_return'].mean())*100).round(2)
            st.metric('(Er) %', er)
        with coll2:
            var_s = df_more['Monthly_return'].var(ddof=1).round(6)
            st.metric('Variance (σ2)', var_s)
        with coll3:
            stdev = ((df_more['Monthly_return'].std(ddof=1)).round(4))*100
            st.metric('Standard deviation (σ) %', stdev)
        st.divider()
        

    except:
        st.error("Yahoo Finance seems to have trouble retrieving some of the information. Please try another ticker.")
    


    st.subheader("Porfolio Performance Metrics")
    rfrm = rfr/12
    print(rfrm)
    mrm = mr/12
    print(mrm)

    sharp_m = ((er-rfrm)/stdev).round(5)
    # print('___')
    # print(er)
    # print(rfrm)
    # print(beta3Year)
    # print(sharp_m)
    # print('___')
    treynor_m = (((er - rfrm)/100)/(beta3Year)).round(5) 

    jensen_m = ((er-(rfrm+(beta3Year*(mrm-rfrm))))/100).round(5)


    colll1, colll2, colll3 = st.columns(3)
    with colll1:
        st.metric('Sharp measure', sharp_m)
    with colll2:
        st.metric('Treynor measure', treynor_m)
    with colll3:
        st.metric('Jensens measure', jensen_m)

    st.subheader("Explanations")
    with st.expander("Sharp Measure"):
        st.latex(r'''\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p} ''')
        st.write("""
        The Sharpe measure is the simplest to use due to its measurement of the return generated over the risk-free asset per unit of risk absorbed by the investor. Thus, the Sharpe measure may be thought of as being independent of any ‘market’ portfolio, allowing a quick comparison to be made between any two portfolios.
        The Sharpe measure is also widely accepted in the industry. The slope measure is based on the portfolio risk premium and the total risk of the portfolio as measured by the standard deviation.
        """)


    with st.expander("Treynor Measure"):
        st.latex(r'''\text{Treynor Ratio} = \frac{R_p - R_f}{\beta_p}''')
        st.write("""The Treynor measure is a risk-adjusted performance metric that evaluates the performance of an investment 
        portfolio relative to its systematic risk, which is represented by the portfolio's beta. 
        It is calculated by dividing the excess return of the portfolio over the risk-free rate by the portfolio's beta. 
        The measure provides an indication of the portfolio manager's ability to generate returns in relation to the market 
        risk taken. A higher Treynor ratio indicates better performance, with the assumption that the portfolio's systematic 
        risk is accurately measured by its beta. However, the measure does not take into account unsystematic risk or 
        the possibility of negative returns.
    """)

    with st.expander("Jensens Measure"):
        st.latex(r'''\text{Jensen's Alpha} = R_p - (R_f + \beta_p(R_m - R_f))
    ''')
        st.write("""Jensen's alpha, also known as the Jensen performance index or excess return, 
        is a risk-adjusted performance metric that measures the excess return of an investment portfolio above the 
        return predicted by the Capital Asset Pricing Model (CAPM) based on the portfolio's beta and the market risk premium. 
        It evaluates the portfolio manager's ability to generate returns in excess of what would be expected given its risk 
        exposure to the market. A positive Jensen's alpha indicates that the portfolio has outperformed its expected return 
        based on its systematic risk, while a negative alpha suggests underperformance. The measure is widely used in portfolio 
        performance evaluation and can help investors identify skilled portfolio managers who are capable of generating alpha.
    """)
st.divider()
st.write("All Rights Reserved © Eben Opperman v0.1 (20 April 2023)")










import streamlit as st
import matplotlib.pyplot as plt
# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Ecocalcolatore - Impatto Ambientale Personale",
    page_icon="🌱",
    layout="wide",
)

# 2. BENCHMARK E COEFFICIENTI DI RIFERIMENTO (Italia)
BENCHMARK = {
    "acqua_giorno_media" : 200,        # Litri/giorno (media Italia 174-220 l)
    "luce_anno_media": 1200,           # KWh/anno (media single)
    "gas_anno_medio": 350,             # Sm3/anno (media single)
    "cibo_sprecato_sett_medio": 555.8, # g/Settimana (~29 kg/anno pro capite)
    "co2_per_kwh": 0.28,               # kg CO2e per kWh elettrico
    "co2_per_sm3": 2.0,                # kg CO2e per Sm3 gas metano
    "co2_per_kg_cibo": 2.5,            # kg CO2e per kg cibo sprecato
    "acqua_per_kg_cibo": 1000,         # Litri di acqua virtuale sprecata per cibo
    "biocapacita_sostenibile_gha": 1.6, # Ettari globali sostenibili per persona
    "impronta_media_italia_gha": 3.8   # Ettari globali medi in Italia (~2.3 pianeti)
}

# 3. INTESTAZIONE APP
st.title("🌱 EcoCalcolatore Spreco & Impatto Ambientale")
st.markdown("""
Analizza i tuoi consumi personali domestici, quantifica lo spreco alimentare e scopri la tua **imporonta ecologica**.)
Utilizza i cursori a sinistra per inserire i tuoi dati e sperimenta con il simulatore **What-if**.
""")

st.divider()

# 4. SIDEBAR - INPUT UTENTE
st.sidebar.header("💮 I tuoi consumi quotidiani")

acqua_giorno = st.sidebar.slider(
    "Acqua potabile diretta (Litri/giorno)",
    min_value=50, max_value=500, value=200, step=10,
    help="Media nazionale in Italia: ~ L/giorno pro capite"
)

luce_kwh = st.sidebar.slider(
    "Consumo elettrico (KWh/anno)",
    min_value=0, max_value=5000, value=1200, step=50,
    help="Media single in Italia: 1.000 - 1400 kWh/anno"
)

gas_sm3 = st.sidebar.slider(
    "Consumo di gas metano (Sm³/anno)",
    min_value=0, max_value=2000, value=350, step=25,
    help="Media per single in Italia: 1.000 - 1.400 Sm³/anno"
)

cibo_g_sett = st.sidebar.slider(
    "Cibo sprecato/gettato (grammi/settimana)",
    min_value=0, max_value=2000, value=550, step=50,
    help="Media nazionale in Italia: ~555,8 g/settimana (~ kg/anno)"
)

# 5. CALCOLI LOGICI
kg_cibo_anno = (cibo_g_sett * 52) / 1000.0

co2_luce = luce_kwh * BENCHMARK["co2_per_kwh"]
co2_gas = gas_sm3 * BENCHMARK["co2_per_sm3"]
co2_cibo = kg_cibo_anno * BENCHMARK["co2_per_kg_cibo"]
co2_totale = co2_luce + co2_gas + co2_cibo

acqua_diretta_anno = acqua_giorno * 365
acqua_sprecata_cibo = kg_cibo_anno * BENCHMARK["acqua_per_kg_cibo"]

rapporto_consumo = (co2_totale / 1500)  
gha_stimati = round(BENCHMARK["impronta_media_italia_gha"] * rapporto_consumo, 1)
pianeti_equivalenti = round(gha_stimati / BENCHMARK["biocapacita_sostenibile_gha"], 1)

# DISPLAY METRICHE PRINCIPALI(KPI)
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric("Impronta CO₂ Totale", f"{round(co2_totale):,} kg", "CO₂e / anno")

with col2:
  st.metric("Acqua Virtuale Sprecata", f"{round(acqua_sprecata_cibo):,} L", "nel cibo buttato")

with col3:
  st.metric("Cibo Sprecato", f"{round(kg_cibo_anno, 1)} kg", "all'anno")

# Calcola la differenza rispetto alla soglia di 1 pianeta
delta_pianeti = round(pianeti_equivalenti - 1.0, 1)

with col4:
  st.metric("Pianeti Terra Necesari", f"{pianeti_equivalenti}", f"+({delta_pianeti} oltre la soglia" if delta_pianeti > 0 else "Sostenibile")

st.divider()

# 7. TABELLA E GRAFICI DETTAGLIATI
tab1, tab2, tab3 = st.tabs(["📊 Analisi Dettagliata", "💡 Simulatore What-If", "📈 Confronto Benchmark"])

with tab1:
  st.subheader("Ripartizione delle Emissioni di CO₂e")

  col_left, col_right = st.columns(2)

  with col_left:
    # Grafico a torta delle emissioni
    labels = ['Energia Elettrica', 'Gas Metano', 'Spreco Alimentare']
    valori = [co2_luce, co2_gas, co2_cibo]
    colori = ['#ff9999', '#66b3ff', '#99ff99']

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(valori, labels=labels, autopct='%1.1f%%', startangle=140, colors=colori)
    ax.axis('equal')
    st.pyplot(fig)

  with col_right:
    st.write("### Dettaglio numerico")
    st.write(f"- **Energia Elettrica:** {round(co2_luce, 1):,} kg CO₂e ({luce_kwh} kwh)")
    st.write(f"- **Gas Metano:** {round(co2_gas, 1):,} kg CO₂e ({gas_sm3} Sm³)")
    st.write(f"- **Speso Cibo:** {round(co2_cibo, 1):,} kg CO₂e ({kg_cibo_anno, 1} kg cibo)")
    st.write(f"- **Acqua Potabile diretta consumata:** {round(acqua_diretta_anno):,} litri/anno")

with tab2:
  st.subheader("Simulatore di Riduzione dello Spreco ('What-If)")
  st.write("Seleziona le buone abitudini che vuoi adottare per vedere il risparmio ambientale stimato:")

  taglio_cibo = st.checkbox("Dimezza lo spreco di cibo (taglio del 50%)")
  doccia_breve = st.checkbox("Riduci il tempo della doccia di 2 minuti (-20 L/giorno)")
  termostato = st.checkbox("Abbassa il termostato di 1°C in inverno (-7% gas metano)")

  co2_risparmiata = 0
  acqua_risparmiata = 0

  if taglio_cibo:
    co2_risparmiata += (kg_cibo_anno / 2.0) * BENCHMARK["co2_per_kg_cibo"]
    acqua_risparmiata += (kg_cibo_anno / 2.0) * BENCHMARK["acqua_per_kg_cibo"]

  if doccia_breve:
    acqua_risparmiata += 20*365

  if termostato:
    co2_risparmiata += (gas_sm3 * 0.07) * BENCHMARK["co2_per_sm3"]

  st.success(f"""
  ### 🎯 Risultato della Tua Simulazione:
  - **CO₂e evitata all'anno**: **{round(co2_risparmiata, 1)} kg**
  - **Acqua salvata all'anno**: **{round(acqua_risparmiata):,} Litri**
  """)

with tab3:
  st.subheader("Confronto con l'Impronta Ecologica Nazionale")
  st.write(f"La tua impronta stimata è di **{gha_stimati} ettari globali (gha)** pro capite.")
  st.write(f"• Media in Italia: **3.8 gha**")
  st.write(f"• Soglia di sostenibilità globale: **1.6 gha**")

  st.progress(min(gha_stimati / 5.0, 1.0))
  if gha_stimati > BENCHMARK["biocapacita_sostenibile_gha"]:
    st.warning(f"Attualmente i tuoi consumi richiedono l'equivalente di **{pianeti_equivalenti} pianeti Terra** se adottati da tutta la popolazione mondiale.")
  else:
    st.balloons()
    st.success("Complimenti! Il tuo livello di consumi rientra nei limiti della sostenibilità globale.")

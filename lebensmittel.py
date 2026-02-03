import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ernährungsübersicht", layout="wide")

# -------------------------
# GRUNDDATEN (NICHT SICHTBAR)
# Werte pro 100 g (Eier pro Stück)
# -------------------------
foods = pd.DataFrame([
    ["Haferflocken", 0.12, 13.0, 370, 3.6, 54, 4.3, 0.0, 0.0, 0.1, 177],
    ["Magerquark", 0.35, 11.0, 67, 0.6, 120, 0.1, 0.0, 0.0, 0.0, 11],
    ["Eier", 0.35, 13.0, 155, 1.3, 56, 1.8, 2.0, 0.0, 0.07, 12],
    ["Rote Linsen", 0.25, 26.0, 350, 3.3, 56, 7.5, 0.0, 4.5, 0.1, 122],
    ["Kartoffeln", 0.08, 2.0, 77, 0.3, 12, 0.8, 0.0, 20.0, 0.0, 23],
    ["Reis", 0.10, 7.5, 360, 1.2, 28, 1.5, 0.0, 0.0, 0.02, 25],
    ["Möhren", 0.09, 1.0, 41, 0.2, 33, 0.3, 0.0, 6.0, 0.0, 12],
    ["TK-Brokkoli", 0.18, 3.0, 34, 0.4, 47, 0.7, 0.0, 89.0, 0.0, 21],
    ["Rapsöl", 0.20, 0.0, 884, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0],
], columns=[
    "Lebensmittel", "Preis", "Eiweiß", "Kalorien", "Zink",
    "Calcium", "Eisen", "VitaminD", "VitaminC", "Omega3", "Magnesium"
])

foods.set_index("Lebensmittel", inplace=True)

# -------------------------
# TÄGLICHE AUFNAHME
# -------------------------
intake = {
    "Haferflocken": 100,
    "Magerquark": 250,
    "Eier": 3,            # Stück
    "Rote Linsen": 100,
    "Kartoffeln": 500,
    "Reis": 80,
    "Möhren": 200,
    "TK-Brokkoli": 200,
    "Rapsöl": 20,
}

intake = pd.Series(intake, name="Menge")

# Eier separat behandeln (pro Stück)
factors = intake / 100
factors["Eier"] = intake["Eier"]

# -------------------------
# BERECHNUNG
# -------------------------
result = foods.mul(factors, axis=0)
result["Kosten/Tag"] = foods["Preis"] * factors
result["Kosten/Monat"] = result["Kosten/Tag"] * 30

# -------------------------
# BEDARF
# -------------------------
bedarf = pd.Series({
    "Kalorien": 2500,
    "Eiweiß": 120,
    "Zink": 10,
    "Calcium": 1000,
    "Eisen": 10,
    "VitaminD": 20,
    "VitaminC": 100,
    "Omega3": 2,
    "Magnesium": 400,
})

# -------------------------
# SUMMEN & DIFFERENZEN
# -------------------------
summe = result.sum()
diff = summe[bedarf.index] - bedarf

# -------------------------
# AUSGABE
# -------------------------
st.title("Tägliche Ernährung – Analyse")

st.subheader("Aufnahme pro Lebensmittel")
st.dataframe(result.round(2))

st.subheader("Gesamtübersicht")
overview = pd.DataFrame({
    "Aufnahme": summe[bedarf.index],
    "Bedarf": bedarf,
    "Differenz": diff
})
st.dataframe(overview.round(2))

st.metric("Monatliche Kosten (€)", f"{summe['Kosten/Monat']:.2f}")
st.metric("Tägliche Kalorien", f"{summe['Kalorien']:.0f}")
st.metric("Tägliches Eiweiß (g)", f"{summe['Eiweiß']:.1f}")

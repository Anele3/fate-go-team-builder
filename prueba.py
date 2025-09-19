import requests
import streamlit as st

if "selected_servants" not in st.session_state:
    st.session_state.selected_servants = []

clases = [
    "saber",
    "archer",
    "lancer",
    "rider",
    "caster",
    "assassin",
    "berserker",
    "ruler",
    "avenger",
    "moonCancer",
    "alterEgo",
    "foreigner",
    "pretender",
    "shielder",
    "beast",
]

def handle_selection(id):
    if id in st.session_state.selected_servants:
        st.session_state.selected_servants.remove(id)
    else:
        if len(st.session_state.selected_servants) < 3:
            st.session_state.selected_servants.append(id)
        else:
            st.warning("Solo puedes tener 3 Servants en el equipo")

response = requests.get(f"https://api.atlasacademy.io/export/NA/basic_servant.json")
idpjs = response.json()

st.subheader("Tu equipo")
team_cols = st.columns(3, border=True)
for i, col in enumerate(team_cols):
    with col:
        if i < len(st.session_state.selected_servants):
            servant_id = st.session_state.selected_servants[i]
            pj = None
            for p in idpjs:
                if p["id"] == servant_id:
                    pj = p
                    break
            if pj:
                st.image(pj.get("face", ""), width=120)
                st.write(f"Integrante {i+1}: {pj['name']}")
        else:
            st.write(f"Integrante {i+1}: Vacío")

option = st.selectbox(
    "Elige una clase de Servant:",
    clases,
    index=None,
    placeholder="Selecciona una clase",
)

if option:
    filtrados = [p for p in idpjs if p.get("className") == option]
    for row in range(0, len(filtrados), 3):
        cols = st.columns(3, border=True)
        for col, p in enumerate(filtrados[row:row+3]):
            with cols[col]:
                st.image(p.get("face", ""), width=120)
                st.write(p["name"])
                checked = p["id"] in st.session_state.selected_servants
                st.checkbox(
                    "Elegir",
                    key=p['id'],
                    value=checked,
                    on_change=handle_selection,
                    args=[p["id"]],
                )

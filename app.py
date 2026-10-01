
import streamlit as st
import pandas as pd
import io
import wave

st.set_page_config(
    page_title="Piattaforma di Raccolta Bioacustica Lirica",
    page_icon="🎙️",
    layout="wide"
)

# -----------------------------
# Titolo
# -----------------------------
st.title("Piattaforma di Raccolta Bioacustica Lirica")
st.caption("Prototipo preliminare — interfaccia e flusso di ricerca")

# -----------------------------
# Stato iniziale
# -----------------------------
if "record" not in st.session_state:
    st.session_state.record = None

# -----------------------------
# Sidebar: configurazione
# -----------------------------
with st.sidebar:
    st.header("1. METADATI & ACQUISIZIONE")
    st.subheader("Configurazione prova")

    participant_id = st.text_input("ID Anonimo Partecipante", "P023")
    exercise = st.selectbox(
        "Esercizio",
        ["Vocale /a/ sostenuta", "Scala ascendente", "Scala discendente",
         "Arpeggio", "Frase operistica"]
    )
    note = st.text_input("Nota Eseguita", "La4")
    tuning = st.number_input(
        "Diapason di Taratura (Hz)",
        min_value=400,
        max_value=460,
        value=443,
        step=1
    )

    st.divider()
    st.markdown("**Acquisizione audio**")

    uploaded = st.file_uploader(
        "Carica file Audio WAV",
        type=["wav"],
        help="Per il prototipo: WAV. L'analisi automatica sarà implementata nella fase successiva."
    )

    recorded = st.audio_input("Oppure registra il campione")

    st.divider()

    if st.button("Avvia Elaborazione Bioacustica", type="primary", use_container_width=True):
        audio_file = recorded if recorded is not None else uploaded

        if audio_file is None:
            st.warning("Carica o registra prima un campione audio.")
        else:
            st.session_state.record = {
                "ID": participant_id,
                "Vocale": "/a/",
                "Nota": note,
                "Diapason": tuning,
                "Audio": audio_file,
            }
            st.success("Campione acquisito. Dati dimostrativi visualizzati.")

# -----------------------------
# Area principale
# -----------------------------
if st.session_state.record is None:
    st.info(
        "Configura la prova nella colonna sinistra, quindi carica o registra un campione WAV."
    )

    st.markdown("### Flusso previsto")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 1. Acquisizione")
        st.write("ID anonimo, esercizio, nota, diapason e campione WAV.")

    with c2:
        st.markdown("#### 2. Analisi")
        st.write("Estrazione di F0, formanti, armoniche e parametri di stabilità.")

    with c3:
        st.markdown("#### 3. Dataset")
        st.write("Registrazione strutturata dei parametri per l'analisi statistica e ML/DL.")

else:
    record = st.session_state.record
    audio = record["Audio"]

    st.subheader("2. ANALISI & 3. VETTORE BIOACUSTICO")

    st.audio(audio, format="audio/wav")

    st.success(
        "Elaborazione dimostrativa completata. "
        "I valori riportati sotto sono dati di esempio del prototipo."
    )

    # Valori dimostrativi: NON presentati come risultato scientifico.
    f0_mean = 442.8
    f0_std = 1.9
    jitter = 0.0038
    shimmer = 0.0192
    hnr = 22.4
    f1, f2, f3 = 745, 1195, 2450

    st.markdown("### Parametri Acustici Estratti (LIVELLO 2)")

    a, b, c = st.columns(3)
    with a:
        st.metric("F0 Media (Hz)", f"{f0_mean:.1f}")
        st.metric("Shimmer", f"{shimmer:.4f}")
    with b:
        st.metric("F0 Dev. Std (Hz)", f"{f0_std:.1f}")
        st.metric("HNR (dB)", f"{hnr:.1f}")
    with c:
        st.metric("Jitter", f"{jitter:.4f}")
        st.metric("Formanti (Hz)", f"F1: {f1} | F2: {f2} | F3: {f3}")

    st.divider()

    st.markdown("### Record Standardizzato per Dataset (LIVELLO 3)")

    row = pd.DataFrame([{
        "ID": record["ID"],
        "Vocale": record["Vocale"],
        "Nota": record["Nota"],
        "Diapason": record["Diapason"],
        "F0_mean": f0_mean,
        "F0_std": f0_std,
        "Jitter": jitter,
        "Shimmer": shimmer,
        "HNR": hnr,
        "F1": f1,
        "F2": f2,
        "F3": f3
    }])

    st.dataframe(row, use_container_width=True, hide_index=True)

    csv = row.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Esporta Record nel Dataset di Ricerca (CSV)",
        data=csv,
        file_name=f"{record['ID']}_bioacustica.csv",
        mime="text/csv",
        type="primary"
    )

    st.caption(
        "Nota metodologica: in questa versione i parametri acustici sono dimostrativi. "
        "L'estrazione reale tramite Parselmouth/Praat e librosa sarà integrata successivamente."
    )

    st.divider()
    st.markdown("### Stato del prototipo")

    s1, s2, s3 = st.columns(3)
    with s1:
        st.success("✓ Metadati")
    with s2:
        st.success("✓ Acquisizione WAV")
    with s3:
        st.success("✓ Struttura dataset")

    st.info(
        "Da implementare nella fase successiva: estrazione automatica F0/formanti/armoniche, "
        "Jitter/Shimmer/HNR, analisi statistica e modelli ML/DL."
    )

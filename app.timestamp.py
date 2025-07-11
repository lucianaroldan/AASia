import streamlit as st
import json, io, pathlib, datetime
from pathlib import Path
from llm_client import interpret_structure, generate_aas
from aas_builder import extract_environment_json
from validator import validate_environment
from summary import summarize_environment
from jsonschema.exceptions import ValidationError
from basyx_exporter import export_aasx_from_json
from utils import sanitize_aas_json, normalize_booleans
from fix_degree_symbols import fix_degree_symbols_in_json

# -----------------------
# Configuration & LLM Info
# -----------------------
MODEL_NAME = "meta-llama-3.1-8b-instruct"
TEMPERATURE = 0.1
MAX_NEW_TOKENS = 1500
TIME_FMT = "%H:%M:%S"

# -----------------------
# Page setup
# -----------------------
st.set_page_config(page_title="AAS Text-to-AAS Generator", layout="wide")
st.title("AAS Text-to-AAS Generator")

# Display LLM model info in sidebar
st.sidebar.header("LLM Model Information")
st.sidebar.write(f"**Model**: {MODEL_NAME}")
st.sidebar.write(f"**Temperature**: {TEMPERATURE}")
st.sidebar.write(f"**Max Tokens**: {MAX_NEW_TOKENS}")

# -----------------------
# Initialize session state
# -----------------------
for key in [
    "analysis_result",
    "aas_json_str",
    "env_dict",
    "analysis_timing",
    "generation_timing",
    "validation_timing",
    "export_timing",
]:
    if key not in st.session_state:
        st.session_state[key] = None

# -----------------------
# Step 1: (Commented Out) Upload & Validate external JSON
# -----------------------
# st.header("1. Upload & Validate AAS JSON")
# uploader = st.file_uploader(
#      "Upload an AAS Environment JSON for validation:",
#      type="json",
#      help="The file must contain `assetAdministrationShells`, `submodels` and `conceptDescriptions`."
# )
# if uploader is not None:
#      try:
#          external = json.load(io.TextIOWrapper(uploader, encoding="utf-8"))
#          validate_environment(external)
#          st.success("✅ External JSON is valid according to the IDTA schema.")
#          st.text(summarize_environment(external))
#          st.json(external, expanded=False)
#      except ValidationError as ve:
#          st.error(f"❌ Does not comply with the schema: {ve.message}")
#      except Exception as ex:
#          st.error(f"Error processing file: {ex}")

# -----------------------
# Step 2: Analyze description
# -----------------------
st.header("1. Analyze Asset Description")
desc = st.text_area("Asset description (EN/ES):", height=180)
if st.button("Analyze Description"):
    if not desc.strip():
        st.warning("Please enter a description.")
    else:
        start_time = datetime.datetime.now()
        with st.spinner("Analyzing description..."):
            st.session_state.analysis_result = interpret_structure(desc)
        end_time = datetime.datetime.now()
        st.session_state.analysis_timing = {
            "start": start_time,
            "end": end_time,
            "duration": (end_time - start_time).total_seconds(),
        }

# Display analysis result persistently
if st.session_state.analysis_result:
    st.subheader("Structured Interpretation of Text")
    #st.markdown(st.session_state.analysis_result)
    st.code(st.session_state.analysis_result, language="text")

    # Show timing information
    if st.session_state.analysis_timing:
        t = st.session_state.analysis_timing
        st.info(
            f"⏱️ **Timing** — Start: {t['start'].strftime(TIME_FMT)}, "
            f"End: {t['end'].strftime(TIME_FMT)}, "
            f"Elapsed: {t['duration']:.2f} s"
        )

# -----------------------
# Step 3: Generate AAS JSON
# -----------------------
st.header("2. Generate AAS JSON")
if st.session_state.analysis_result:
    if st.button("Generate AAS JSON"):
        start_time = datetime.datetime.now()
        with st.spinner("Generating AAS JSON via LLM..."):
            try:
                resp = generate_aas(
                    f"{st.session_state.analysis_result}",
                    model=MODEL_NAME,
                    temperature=TEMPERATURE,
                    max_new_tokens=MAX_NEW_TOKENS,
                    timeout=3600,
                    stream=True,
                )
                # --- sanitize idShorts & normalize booleans ---
                env_raw = json.loads(resp)
                env_clean = sanitize_aas_json(env_raw)
                env_clean = fix_degree_symbols_in_json(env_clean)
                env_clean = normalize_booleans(env_clean)
                resp = json.dumps(env_clean, ensure_ascii=False, indent=2)
                # ------------------------------------------------
                st.session_state.aas_json_str = resp
            except Exception as e:
                st.error(f"LLM error: {e}")
                st.stop()
        end_time = datetime.datetime.now()
        st.session_state.generation_timing = {
            "start": start_time,
            "end": end_time,
            "duration": (end_time - start_time).total_seconds(),
        }

# Display generated JSON persistently
if st.session_state.aas_json_str:
    st.subheader("Generated AAS JSON")
    st.code(st.session_state.aas_json_str, language="json")

    # Show timing information
    if st.session_state.generation_timing:
        t = st.session_state.generation_timing
        st.info(
            f"⏱️ **Timing** — Start: {t['start'].strftime(TIME_FMT)}, "
            f"End: {t['end'].strftime(TIME_FMT)}, "
            f"Elapsed: {t['duration']:.2f} s"
        )

    # Download button
    output_json = pathlib.Path("generated_aas.json")
    with open(output_json, "w", encoding="utf-8") as f:
        f.write(st.session_state.aas_json_str)
    with open(output_json, "rb") as f:
        st.download_button(
            "Download AAS JSON",
            f,
            file_name=output_json.name,
            mime="application/json",
        )

# -----------------------
# Step 4: Validate & Summarize
# -----------------------
st.header("3. Validate & Summarize Generated JSON")
if st.session_state.aas_json_str:
    if st.button("Validate & Summarize AAS JSON"):
        start_time = datetime.datetime.now()
        try:
            env = extract_environment_json(st.session_state.aas_json_str)
            validate_environment(env)
            st.session_state.env_dict = env
        except ValidationError as ve:
            st.error(f"Schema error: {ve.message}")
        except Exception as ex:
            st.error(f"Processing error: {ex}")
        end_time = datetime.datetime.now()
        st.session_state.validation_timing = {
            "start": start_time,
            "end": end_time,
            "duration": (end_time - start_time).total_seconds(),
        }

# Display validation & summary persistently
if st.session_state.env_dict:
    st.subheader("Validation Successful")
    st.success("✅ AAS Environment is valid.")
    st.subheader("Environment Summary")
    st.text(summarize_environment(st.session_state.env_dict))
    st.json(st.session_state.env_dict, expanded=False)

    # Show timing information
    if st.session_state.validation_timing:
        t = st.session_state.validation_timing
        st.info(
            f"⏱️ **Timing** — Start: {t['start'].strftime(TIME_FMT)}, "
            f"End: {t['end'].strftime(TIME_FMT)}, "
            f"Elapsed: {t['duration']:.2f} s"
        )

# -----------------------
# Step 5: Export to AASX Package
# -----------------------
st.header("4. Export to AASX Package")
if st.session_state.env_dict:
    if st.button("Export to AASX"):
        start_time = datetime.datetime.now()
        try:
            out_path = export_aasx_from_json(st.session_state.aas_json_str, Path("output.aasx"))
            st.success(f"AASX package generated: {out_path.name}")
            data = out_path.read_bytes()
            st.download_button(
                "Download AASX",
                data,
                file_name=out_path.name,
                mime="application/octet-stream",
            )
        except Exception as e:
            st.error(f"Error exporting AASX: {e}")
        end_time = datetime.datetime.now()
        st.session_state.export_timing = {
            "start": start_time,
            "end": end_time,
            "duration": (end_time - start_time).total_seconds(),
        }

    # Show timing information
    if st.session_state.export_timing:
        t = st.session_state.export_timing
        st.info(
            f"⏱️ **Timing** — Start: {t['start'].strftime(TIME_FMT)}, "
            f"End: {t['end'].strftime(TIME_FMT)}, "
            f"Elapsed: {t['duration']:.2f} s"
        )

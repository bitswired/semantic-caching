import streamlit as st

from semantic_caching.cache import CacheEvaluator

st.set_page_config(layout="wide")


@st.cache_resource
def get_cache():
    return CacheEvaluator()


if "prompts" not in st.session_state:
    st.session_state["prompts"] = []
    cache = get_cache()
    cache.reset()


st.title("Semantic Caching Evaluation")

with st.sidebar:
    st.header("Manage cache")
    title = st.text_input("Add prompt to the cache", "What is GitHub?")

    col1, col2 = st.columns(2)
    with col1:
        add_clicked = st.button("Add", type="primary", use_container_width=True)
    with col2:
        clear_clicked = st.button("Clear", type="secondary", use_container_width=True)

    if add_clicked:
        p_bar = st.progress(0, text="Adding to cache...")
        st.session_state["prompts"].append(title)
        cache = get_cache()
        with cache.use_cache("openai"):
            cache.add_to_cache(title)
        p_bar.progress(50, text="Adding to cache...")
        with cache.use_cache("onnx"):
            cache.add_to_cache(title)
        p_bar.progress(100, text="Adding to cache...")
        p_bar.empty()

    if clear_clicked:
        with st.spinner("Wait for it..."):
            st.session_state["prompts"] = []
            cache = get_cache()
            cache.reset()

    prompts = st.session_state["prompts"]
    st.markdown(f"### {len(prompts)} Prompts in the cache:")
    for prompt in prompts:
        st.write(prompt)


col1, col2 = st.columns([3, 1])
with col1:
    title = st.text_input("Query the cache", "What is GitHub?")
with col2:
    st.text("")
    st.text("")
    clicked = st.button("Query", type="primary")


if clicked:
    cache = get_cache()
    progress_text = "Querying..."
    p_bar = st.progress(0, text=progress_text)

    with cache.use_cache("openai"):
        openai_matches = cache.query(title)

    p_bar.progress(50, text=progress_text)

    with cache.use_cache("onnx"):
        onnx_matches = cache.query(title)

    p_bar.progress(100, text=progress_text)

    p_bar.empty()

    col1, col2 = st.columns(2)

    def display_matches(x):
        for i, (question, score) in enumerate(x):
            st.markdown(f"{i+1}. **{question}** ({score})")

    with col1:
        st.subheader("OpenAI Embedding (lower score is better)")
        if clicked:
            cache = get_cache()
            display_matches(openai_matches)

    with col2:
        st.subheader("ONNX Embedding (lower score is better)")
        if clicked:
            cache = get_cache()
            display_matches(onnx_matches)

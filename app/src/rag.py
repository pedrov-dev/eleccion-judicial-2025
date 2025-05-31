def retrieve_context(query, index, model, namespace, top_k=5):
    """
    Embed the query and retrieve top_k relevant texts from Pinecone.
    Returns a concatenated string of retrieved texts.
    """
    query_emb = model.encode([query])[0].tolist()
    results = index.query(
        vector=query_emb,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    context = "\n".join(
        [match['metadata']['text'] for match in results['matches']
         if 'metadata' in match and 'text' in match['metadata']]
    )
    return context


def build_rag_prompt(query, context):
    """
    Build a prompt for the LLM using the retrieved context and user query.
    """
    prompt = (
        "Usa la siguiente información de contexto para responder la pregunta.\n"
        "Contexto:\n"
        f"{context}\n"
        "Pregunta:\n"
        f"{query}\n"
        "Respuesta:"
    )
    return prompt


def rag_ask_openai(query, index, model, namespace, ask_openai_func, top_k=10):
    """
    Retrieve context, build prompt, and get answer from OpenAI.
    ask_openai_func should be a function that takes a prompt and returns a string.
    """
    context = retrieve_context(query, index, model, namespace, top_k=top_k)
    prompt = build_rag_prompt(query, context)
    response = ask_openai_func(prompt)
    if response:
        return response
    else:
        return "No response from OpenAI."
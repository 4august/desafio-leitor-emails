from transformers import pipeline
import threading

_sentiment_pipeline = None
_text_generation_pipeline = None
_lock = threading.Lock()

def get_text_generation_pipeline():
    global _text_generation_pipeline
    if _text_generation_pipeline is None:
        with _lock:
            if _text_generation_pipeline is None:
                _text_generation_pipeline = pipeline(
                    task="text-generation",
                    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
                )
    return _text_generation_pipeline

def generate_auto_reply(text: str):
    pipe = get_text_generation_pipeline()

    prompt = f"""
Você é um assistente profissional especializado em responder e-mails recebido de clientes ou usuários
de forma empresarial, educada e objetiva exclusivamente em língua portuguesa brasileiro.

Regras obrigatórias:
- NÃO faça diálogo ou bate-papo
- NÃO use listas, tópicos ou múltiplas frases
- No máximo 100 caracteres
- Termine a mensagem com ponto final

E-mail recebido:
{text[:150]}

Resposta:
"""

    result = pipe(
        prompt,
        max_new_tokens=60,
        do_sample=False,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.1
    )

    reply = result[0]["generated_text"]

    reply = reply.replace(prompt, "").strip()

    if not reply:
        return (
            "Olá, agradecemos seu contato. "
            "Vamos analisar a solicitação e retornaremos em breve."
        )

    return reply
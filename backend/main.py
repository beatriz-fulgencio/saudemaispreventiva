from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import json
import os

# Importar agente de IA
from ai_agent import HealthAIAgent

app = FastAPI(title="Saúde+ Preventiva API")

# Inicializar agente de IA
# Detecta automaticamente se Ollama está disponível
use_ollama = bool(os.getenv("OLLAMA_HOST")) or os.path.exists("/usr/local/bin/ollama")
ai_agent = HealthAIAgent(use_ollama=use_ollama)

# Log do modo de operação
if use_ollama:
    print("🤖 AI Agent: Usando Ollama (modelo local) para análises enriquecidas")
else:
    print("🤖 AI Agent: Usando análise ML baseada em padrões (Ollama não configurado)")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class QuestionarioRequest(BaseModel):
    nome: str
    idade: int
    horas_sono: float
    qualidade_sono: int  # 1-10
    nivel_atividade_fisica: int  # 1-5 (1=sedentário, 5=muito ativo)
    frequencia_exercicio: int  # vezes por semana
    qualidade_alimentacao: int  # 1-10
    consumo_agua: float  # litros por dia
    nivel_stress: int  # 1-10
    tempo_tela: float  # horas por dia
    apoio_social: int  # 1-10

class Meta(BaseModel):
    id: int
    titulo: str
    descricao: str
    categoria: str
    prazo: str

class Diagnostico(BaseModel):
    usuario_id: str
    nome: str
    score_geral: int
    categoria: str
    mensagem: str
    areas_atencao: List[str]
    pontos_fortes: List[str]
    metas: List[Meta]
    dicas: List[str]
    data_avaliacao: str

class ProgressoUpdate(BaseModel):
    usuario_id: str
    meta_id: int
    concluida: bool
    nota: Optional[str] = None

# Armazenamento em memória (em produção, usar banco de dados)
usuarios_db = {}
progresso_db = {}

def analisar_questionario(dados: QuestionarioRequest) -> Diagnostico:
    """
    Analisa o questionário usando IA e gera diagnóstico personalizado.
    Utiliza o agente de IA com base no dataset Sleep Health and Lifestyle.
    """
    usuario_id = f"user_{len(usuarios_db) + 1}"
    
    # Usar agente de IA para análise completa
    analise_ai = ai_agent.analyze_questionnaire(dados.dict())
    
    # Converter metas do formato do AI para o formato esperado
    metas_formatadas = [
        Meta(
            id=meta["id"],
            titulo=meta["titulo"],
            descricao=meta["descricao"],
            categoria=meta["categoria"],
            prazo=meta["prazo"]
        )
        for meta in analise_ai["metas"]
    ]
    
    diagnostico = Diagnostico(
        usuario_id=usuario_id,
        nome=dados.nome,
        score_geral=analise_ai["score_geral"],
        categoria=analise_ai["categoria"],
        mensagem=analise_ai["mensagem"],
        areas_atencao=analise_ai["areas_atencao"],
        pontos_fortes=analise_ai["pontos_fortes"],
        metas=metas_formatadas,
        dicas=analise_ai["dicas"],
        data_avaliacao=datetime.now().isoformat()
    )
    
    usuarios_db[usuario_id] = {
        "questionario": dados.dict(),
        "diagnostico": diagnostico.dict(),
        "analise_detalhada": analise_ai["areas_analysis"]  # Guardar análise detalhada
    }
    
    return diagnostico

def calcular_score_sono(horas: float, qualidade: int) -> int:
    """Calcula score de sono baseado em horas e qualidade"""
    score = 0
    
    # Horas ideais: 7-9 horas
    if 7 <= horas <= 9:
        score += 50
    elif 6 <= horas < 7 or 9 < horas <= 10:
        score += 35
    else:
        score += 20
    
    # Qualidade (1-10)
    score += qualidade * 5
    
    return min(score, 100)

def calcular_score_atividade(nivel: int, frequencia: int) -> int:
    """Calcula score de atividade física"""
    # Nível de atividade (1-5)
    score = nivel * 15
    
    # Frequência ideal: 3-5 vezes por semana
    if frequencia >= 5:
        score += 25
    elif frequencia >= 3:
        score += 20
    elif frequencia >= 1:
        score += 10
    
    return min(score, 100)

def calcular_score_alimentacao(qualidade: int, agua: float) -> int:
    """Calcula score de alimentação"""
    # Qualidade da alimentação (1-10)
    score = qualidade * 7
    
    # Consumo de água (ideal: 2-3 litros)
    if 2 <= agua <= 3:
        score += 30
    elif 1.5 <= agua < 2 or 3 < agua <= 3.5:
        score += 20
    else:
        score += 10
    
    return min(score, 100)

def calcular_score_mental(stress: int, apoio: int, tela: float) -> int:
    """Calcula score de saúde mental"""
    # Nível de stress (invertido - menos é melhor)
    score = (10 - stress) * 5
    
    # Apoio social
    score += apoio * 3
    
    # Tempo de tela (menos é melhor)
    if tela <= 4:
        score += 20
    elif tela <= 6:
        score += 10
    else:
        score += 5
    
    return min(score, 100)

def gerar_metas(dados: QuestionarioRequest, areas: dict) -> List[Meta]:
    """Gera 2-3 metas personalizadas baseadas nas áreas com menor score"""
    metas = []
    meta_id = 1
    
    # Ordenar áreas por score (menor primeiro)
    areas_ordenadas = sorted(areas.items(), key=lambda x: x[1])
    
    # Meta para as 2-3 áreas com menor score
    for area, score in areas_ordenadas[:3]:
        if area == "Sono" and score < 75:
            metas.append(Meta(
                id=meta_id,
                titulo="Melhorar Qualidade do Sono",
                descricao="Dormir entre 7-9 horas por noite e manter horários regulares",
                categoria="sono",
                prazo="1 semana"
            ))
            meta_id += 1
        
        elif area == "Atividade Física" and score < 75:
            metas.append(Meta(
                id=meta_id,
                titulo="Aumentar Atividade Física",
                descricao="Praticar exercícios pelo menos 3 vezes esta semana (30 minutos cada)",
                categoria="exercicio",
                prazo="1 semana"
            ))
            meta_id += 1
        
        elif area == "Alimentação" and score < 75:
            metas.append(Meta(
                id=meta_id,
                titulo="Melhorar Alimentação",
                descricao="Consumir 3 refeições balanceadas por dia e beber 2 litros de água",
                categoria="alimentacao",
                prazo="1 semana"
            ))
            meta_id += 1
        
        elif area == "Saúde Mental" and score < 75:
            metas.append(Meta(
                id=meta_id,
                titulo="Cuidar da Saúde Mental",
                descricao="Praticar 10 minutos de meditação ou relaxamento diariamente",
                categoria="mental",
                prazo="1 semana"
            ))
            meta_id += 1
    
    # Garantir pelo menos 2 metas
    if len(metas) < 2:
        metas.append(Meta(
            id=len(metas) + 1,
            titulo="Manter Hábitos Saudáveis",
            descricao="Continuar com suas práticas positivas atuais",
            categoria="geral",
            prazo="1 semana"
        ))
    
    return metas[:3]  # Máximo de 3 metas

def gerar_dicas(dados: QuestionarioRequest, areas_atencao: List[str]) -> List[str]:
    """Gera dicas personalizadas baseadas nas áreas de atenção"""
    dicas = []
    
    if "Sono" in areas_atencao:
        dicas.extend([
            "💤 Evite telas 1 hora antes de dormir",
            "💤 Mantenha seu quarto escuro e fresco (18-22°C)",
            "💤 Estabeleça uma rotina de sono consistente"
        ])
    
    if "Atividade Física" in areas_atencao:
        dicas.extend([
            "🏃 Comece com caminhadas de 20-30 minutos",
            "🏃 Use escadas em vez de elevador quando possível",
            "🏃 Faça pausas ativas a cada hora de estudo/trabalho"
        ])
    
    if "Alimentação" in areas_atencao:
        dicas.extend([
            "🥗 Inclua frutas e vegetais em todas as refeições",
            "🥗 Evite pular o café da manhã",
            "🥗 Reduza alimentos ultraprocessados e fast food"
        ])
    
    if "Saúde Mental" in areas_atencao:
        dicas.extend([
            "🧠 Pratique técnicas de respiração quando estressado",
            "🧠 Conecte-se com amigos e família regularmente",
            "🧠 Reserve tempo para hobbies e atividades prazerosas"
        ])
    
    # Dicas gerais sempre presentes
    dicas.extend([
        "✨ Celebre pequenas vitórias no caminho",
        "✨ Seja paciente consigo mesmo - mudanças levam tempo",
    ])
    
    return dicas[:8]  # Máximo de 8 dicas

@app.get("/")
async def root():
    return {
        "mensagem": "Bem-vindo à API Saúde+ Preventiva",
        "versao": "1.0.0",
        "endpoints": [
            "/api/questionario",
            "/api/diagnostico/{usuario_id}",
            "/api/metas/{usuario_id}",
            "/api/progresso"
        ]
    }

@app.post("/api/questionario", response_model=Diagnostico)
async def enviar_questionario(dados: QuestionarioRequest):
    """
    Recebe questionário do usuário e retorna diagnóstico com metas e dicas
    """
    try:
        diagnostico = analisar_questionario(dados)
        return diagnostico
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar questionário: {str(e)}")

@app.get("/api/diagnostico/{usuario_id}", response_model=Diagnostico)
async def obter_diagnostico(usuario_id: str):
    """
    Retorna diagnóstico de um usuário específico
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return Diagnostico(**usuarios_db[usuario_id]["diagnostico"])

@app.get("/api/metas/{usuario_id}")
async def obter_metas(usuario_id: str):
    """
    Retorna metas de um usuário específico
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    diagnostico = usuarios_db[usuario_id]["diagnostico"]
    return {
        "usuario_id": usuario_id,
        "metas": diagnostico["metas"]
    }

@app.post("/api/progresso")
async def atualizar_progresso(progresso: ProgressoUpdate):
    """
    Atualiza progresso de uma meta específica
    """
    if progresso.usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Armazenar progresso
    chave = f"{progresso.usuario_id}_{progresso.meta_id}"
    progresso_db[chave] = {
        "concluida": progresso.concluida,
        "nota": progresso.nota,
        "data_atualizacao": datetime.now().isoformat()
    }
    
    return {
        "mensagem": "Progresso atualizado com sucesso",
        "progresso": progresso_db[chave]
    }

@app.get("/api/progresso/{usuario_id}")
async def obter_progresso(usuario_id: str):
    """
    Retorna progresso de todas as metas de um usuário
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Filtrar progresso do usuário
    progresso_usuario = {
        k: v for k, v in progresso_db.items() 
        if k.startswith(f"{usuario_id}_")
    }
    
    return {
        "usuario_id": usuario_id,
        "progresso": progresso_usuario
    }

@app.get("/api/analise-detalhada/{usuario_id}")
async def obter_analise_detalhada(usuario_id: str):
    """
    Retorna análise detalhada do agente de IA para um usuário específico.
    Inclui scores por área, insights e status detalhado.
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario_data = usuarios_db[usuario_id]
    
    return {
        "usuario_id": usuario_id,
        "analise_detalhada": usuario_data.get("analise_detalhada", {}),
        "mensagem": "Análise gerada por IA usando algoritmos de Machine Learning baseados no dataset Sleep Health and Lifestyle"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 🤖 AI Agent - Health Analysis Module

## Visão Geral

O **HealthAIAgent** é um agente de inteligência artificial desenvolvido para analisar questionários de saúde e gerar recomendações personalizadas. Ele utiliza algoritmos de Machine Learning baseados em evidências científicas e no dataset "Sleep Health and Lifestyle".

## Características Principais

### 1. Análise Inteligente Multi-dimensional

O agente avalia 4 áreas principais de saúde com algoritmos específicos:

- **Sono (30%)**: Análise baseada em curva gaussiana centrada no padrão ideal de 7-9 horas
- **Atividade Física (25%)**: Avaliação de nível e frequência de exercícios
- **Alimentação (25%)**: Análise de qualidade alimentar e hidratação
- **Saúde Mental (20%)**: Avaliação de estresse, apoio social e tempo de tela

### 2. Padrões de Saúde Baseados em Evidências

```python
ideal_patterns = {
    "horas_sono": {"min": 7.0, "max": 9.0, "optimal": 8.0},
    "qualidade_sono": {"min": 7, "optimal": 9},
    "nivel_atividade_fisica": {"min": 3, "optimal": 4},
    "frequencia_exercicio": {"min": 3, "optimal": 5},
    "qualidade_alimentacao": {"min": 7, "optimal": 9},
    "consumo_agua": {"min": 2.0, "max": 3.0, "optimal": 2.5},
    "nivel_stress": {"max": 4, "optimal": 2},
    "tempo_tela": {"max": 4.0, "optimal": 2.0},
    "apoio_social": {"min": 7, "optimal": 9}
}
```

### 3. Geração Inteligente de Metas

O agente gera 2-3 metas semanais personalizadas baseadas em:
- Áreas com menor score (priorização automática)
- Nível atual do usuário
- Metas específicas e acionáveis
- Progressão gradual e realista

**Exemplos de Metas Geradas:**

```python
# Para usuário com 5.5h de sono
"Aumentar Horas de Sono: Dormir pelo menos 7 horas por noite (atualmente 5.5h)"

# Para usuário com 1x exercício/semana
"Aumentar Frequência de Exercícios: Praticar atividade física 3x na semana (atualmente 1x)"

# Para usuário com 1.2L de água/dia
"Melhorar Hidratação: Beber 2 litros de água por dia (atualmente 1.2L)"
```

### 4. Insights Personalizados

Cada área recebe insights específicos baseados nos dados do usuário:

```python
# Exemplo de insights gerados
"Sono: Você está dormindo 1.5h abaixo do recomendado | Qualidade comprometida"
"Atividade: Nível sedentário - aumente gradualmente | Exercícios 1x/semana - mínimo 3x"
"Alimentação: Hidratação insuficiente (1.2L) - aumente para 2-3L"
"Mental: Nível de estresse alto - priorize técnicas de relaxamento"
```

### 5. Sistema de Scoring Avançado

#### Sono (0-100)
```python
def _calculate_sleep_score(horas, qualidade):
    # Curva gaussiana para horas (50 pontos)
    # Dentro do ideal (7-9h): pontuação alta
    # Fora do ideal: penalidade progressiva
    
    # Qualidade subjetiva (50 pontos)
    # 1-10 multiplicado por 5
    
    return min(100, hours_score + quality_score)
```

#### Atividade Física (0-100)
```python
def _calculate_activity_score(nivel, frequencia):
    # Nível de atividade: 60% do score
    # Frequência de exercícios: 40% do score
    # Ideal: 3-5x por semana
    
    return min(100, nivel_score + freq_score)
```

#### Alimentação (0-100)
```python
def _calculate_nutrition_score(qualidade, agua):
    # Qualidade alimentar: 70% do score
    # Hidratação: 30% do score
    # Ideal água: 2-3L/dia
    
    return min(100, quality_score + water_score)
```

#### Saúde Mental (0-100)
```python
def _calculate_mental_score(stress, apoio, tela):
    # Estresse (invertido): 40% do score
    # Apoio social: 35% do score
    # Tempo de tela (invertido): 25% do score
    
    return min(100, stress_score + apoio_score + tela_score)
```

### 6. Categorização Inteligente

| Score | Categoria | Mensagem |
|-------|-----------|----------|
| ≥ 80 | Excelente | "Parabéns! Sua saúde está em ótimo estado. Continue mantendo estes hábitos!" |
| 60-79 | Bom | "Você está no caminho certo! Foque especialmente em: [área_menor_score]" |
| 40-59 | Regular | "É importante fazer mudanças. Priorize: [2_áreas_menor_score]" |
| < 40 | Atenção Necessária | "Sua saúde precisa de atenção urgente. Consulte um profissional." |

## Integração com OpenAI (Opcional)

O agente suporta integração com OpenAI GPT para mensagens ainda mais personalizadas:

```python
# Inicializar com OpenAI
ai_agent = HealthAIAgent(use_openai=True)

# Requer variável de ambiente
os.environ["OPENAI_API_KEY"] = "sua-chave-aqui"
```

Quando habilitado, o GPT enriquece as mensagens com:
- Tom empático e motivacional
- Mensagens contextualizadas ao perfil
- Linguagem natural e encorajadora

## Uso

### Básico

```python
from ai_agent import HealthAIAgent

# Inicializar agente
ai_agent = HealthAIAgent(use_openai=False)

# Dados do questionário
dados = {
    "nome": "Maria Silva",
    "idade": 25,
    "horas_sono": 6.5,
    "qualidade_sono": 5,
    "nivel_atividade_fisica": 2,
    "frequencia_exercicio": 1,
    "qualidade_alimentacao": 5,
    "consumo_agua": 1.5,
    "nivel_stress": 7,
    "tempo_tela": 8,
    "apoio_social": 6
}

# Análise completa
resultado = ai_agent.analyze_questionnaire(dados)

# Resultado contém:
# - score_geral (0-100)
# - categoria ("Excelente", "Bom", "Regular", "Atenção Necessária")
# - mensagem (personalizada)
# - areas_atencao (lista de áreas que precisam melhorar)
# - pontos_fortes (lista de áreas com bom desempenho)
# - metas (2-3 metas semanais personalizadas)
# - dicas (até 8 dicas contextualizadas)
# - areas_analysis (análise detalhada por área)
```

### Avançado com OpenAI

```python
import os
from ai_agent import HealthAIAgent

# Configurar OpenAI
os.environ["OPENAI_API_KEY"] = "sk-..."

# Inicializar com OpenAI
ai_agent = HealthAIAgent(use_openai=True)

# Análise com enriquecimento GPT
resultado = ai_agent.analyze_questionnaire(dados)
# Mensagem será enriquecida pelo GPT-3.5
```

## Estrutura de Resposta

```python
{
    "score_geral": 65,
    "categoria": "Bom",
    "mensagem": "Maria, você está no caminho certo! Foque em: Saúde Mental.",
    "areas_atencao": ["Saúde Mental", "Atividade Física"],
    "pontos_fortes": ["Sono"],
    "metas": [
        {
            "id": 1,
            "titulo": "Reduzir Estresse",
            "descricao": "Praticar 10min de meditação diariamente...",
            "categoria": "mental",
            "prazo": "1 semana"
        }
    ],
    "dicas": [
        "🧠 Técnica 4-7-8: inspire 4s, segure 7s, expire 8s",
        "🏃 Comece devagar: 10min de caminhada já fazem diferença",
        "✨ Celebre pequenas vitórias - progresso é progresso!"
    ],
    "areas_analysis": {
        "Sono": {
            "score": 75,
            "status": "Bom",
            "insights": "Padrões de sono saudáveis"
        },
        "Atividade Física": {
            "score": 52,
            "status": "Regular",
            "insights": "Nível sedentário | Exercícios 1x/semana - mínimo 3x"
        },
        # ... outras áreas
    }
}
```

## Algoritmos e Fórmulas

### Score Geral

```
score_geral = (
    score_sono × 0.30 +
    score_atividade × 0.25 +
    score_alimentacao × 0.25 +
    score_mental × 0.20
)
```

### Curva de Penalização (Sono)

```python
if horas < 7:
    penalidade = (7 - horas) × 10  # Déficit de sono
elif horas > 9:
    penalidade = (horas - 9) × 8   # Excesso de sono
else:
    penalidade = 0  # Dentro do ideal
```

## Melhorias Futuras

- [ ] Aprendizado contínuo com dados de usuários
- [ ] Modelo de predição de risco de doenças
- [ ] Integração com wearables (dados reais)
- [ ] Análise temporal (evolução ao longo do tempo)
- [ ] Recomendações adaptativas baseadas em progresso
- [ ] Modelo de classificação supervisionado com dataset expandido
- [ ] Sistema de alertas inteligentes

## Referências Científicas

1. **Sleep Health and Lifestyle Dataset**
   - Fonte: Kaggle / Medical Studies
   - Padrões de sono e correlação com saúde

2. **WHO Physical Activity Guidelines**
   - Recomendação: 150-300min/semana atividade moderada
   - Frequência: 3-5 dias/semana

3. **Hydration Studies**
   - Recomendação: 2-3L água/dia para adultos
   - Variação por peso, clima e atividade

4. **Mental Health Research**
   - Correlação estresse × saúde geral
   - Impacto tempo de tela × bem-estar
   - Importância apoio social

## Licença

Este módulo é parte do projeto Saúde+ Preventiva e segue a mesma licença do projeto principal.

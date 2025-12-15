# 📚 Documentação da API - Saúde+ Preventiva

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Root Endpoint
**GET /** 

Retorna informações sobre a API.

**Response:**
```json
{
  "mensagem": "Bem-vindo à API Saúde+ Preventiva",
  "versao": "1.0.0",
  "endpoints": [
    "/api/questionario",
    "/api/diagnostico/{usuario_id}",
    "/api/metas/{usuario_id}",
    "/api/progresso"
  ]
}
```

---

### 2. Enviar Questionário
**POST /api/questionario**

Envia o questionário preenchido pelo usuário e retorna um diagnóstico completo com metas e dicas personalizadas.

**Request Body:**
```json
{
  "nome": "Maria Santos",
  "idade": 25,
  "horas_sono": 7.5,
  "qualidade_sono": 7,
  "nivel_atividade_fisica": 3,
  "frequencia_exercicio": 3,
  "qualidade_alimentacao": 6,
  "consumo_agua": 2.0,
  "nivel_stress": 6,
  "tempo_tela": 5.0,
  "apoio_social": 7
}
```

**Campos:**
- `nome` (string, obrigatório): Nome completo do usuário
- `idade` (integer, obrigatório): Idade do usuário (15-100)
- `horas_sono` (float, obrigatório): Horas de sono por noite (0-24)
- `qualidade_sono` (integer, obrigatório): Qualidade do sono (1-10)
- `nivel_atividade_fisica` (integer, obrigatório): Nível de atividade física diária (1-5)
  - 1 = Sedentário
  - 5 = Muito ativo
- `frequencia_exercicio` (integer, obrigatório): Vezes por semana que pratica exercícios (0-7)
- `qualidade_alimentacao` (integer, obrigatório): Qualidade da alimentação (1-10)
- `consumo_agua` (float, obrigatório): Litros de água por dia (0-10)
- `nivel_stress` (integer, obrigatório): Nível de estresse (1-10)
- `tempo_tela` (float, obrigatório): Horas de tela por dia (0-24)
- `apoio_social` (integer, obrigatório): Avaliação do apoio social (1-10)

**Response (200 OK):**
```json
{
  "usuario_id": "user_1",
  "nome": "Maria Santos",
  "score_geral": 62,
  "categoria": "Bom",
  "mensagem": "Maria Santos, você está no caminho certo, mas há espaço para melhorias.",
  "areas_atencao": ["Atividade Física", "Saúde Mental"],
  "pontos_fortes": ["Sono"],
  "metas": [
    {
      "id": 1,
      "titulo": "Cuidar da Saúde Mental",
      "descricao": "Praticar 10 minutos de meditação ou relaxamento diariamente",
      "categoria": "mental",
      "prazo": "1 semana"
    },
    {
      "id": 2,
      "titulo": "Aumentar Atividade Física",
      "descricao": "Praticar exercícios pelo menos 3 vezes esta semana (30 minutos cada)",
      "categoria": "exercicio",
      "prazo": "1 semana"
    }
  ],
  "dicas": [
    "🏃 Comece com caminhadas de 20-30 minutos",
    "🧠 Pratique técnicas de respiração quando estressado",
    "✨ Celebre pequenas vitórias no caminho"
  ],
  "data_avaliacao": "2025-12-10T17:00:00.000000"
}
```

**Categorias de Score:**
- **Excelente**: Score ≥ 80
- **Bom**: Score 60-79
- **Regular**: Score 40-59
- **Atenção Necessária**: Score < 40

**Response (500 Internal Server Error):**
```json
{
  "detail": "Erro ao processar questionário: [mensagem de erro]"
}
```

---

### 3. Obter Diagnóstico
**GET /api/diagnostico/{usuario_id}**

Retorna o diagnóstico completo de um usuário específico.

**Parâmetros:**
- `usuario_id` (path, string, obrigatório): ID do usuário (ex: "user_1")

**Response (200 OK):**
```json
{
  "usuario_id": "user_1",
  "nome": "Maria Santos",
  "score_geral": 62,
  "categoria": "Bom",
  "mensagem": "Maria Santos, você está no caminho certo, mas há espaço para melhorias.",
  "areas_atencao": ["Atividade Física", "Saúde Mental"],
  "pontos_fortes": ["Sono"],
  "metas": [...],
  "dicas": [...],
  "data_avaliacao": "2025-12-10T17:00:00.000000"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Usuário não encontrado"
}
```

---

### 4. Obter Metas
**GET /api/metas/{usuario_id}**

Retorna as metas semanais de um usuário específico.

**Parâmetros:**
- `usuario_id` (path, string, obrigatório): ID do usuário

**Response (200 OK):**
```json
{
  "usuario_id": "user_1",
  "metas": [
    {
      "id": 1,
      "titulo": "Cuidar da Saúde Mental",
      "descricao": "Praticar 10 minutos de meditação ou relaxamento diariamente",
      "categoria": "mental",
      "prazo": "1 semana"
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Usuário não encontrado"
}
```

---

### 5. Atualizar Progresso
**POST /api/progresso**

Atualiza o progresso de uma meta específica.

**Request Body:**
```json
{
  "usuario_id": "user_1",
  "meta_id": 1,
  "concluida": true,
  "nota": "Consegui meditar por 10 minutos durante 5 dias!"
}
```

**Campos:**
- `usuario_id` (string, obrigatório): ID do usuário
- `meta_id` (integer, obrigatório): ID da meta
- `concluida` (boolean, obrigatório): Se a meta foi concluída
- `nota` (string, opcional): Observações sobre o progresso

**Response (200 OK):**
```json
{
  "mensagem": "Progresso atualizado com sucesso",
  "progresso": {
    "concluida": true,
    "nota": "Consegui meditar por 10 minutos durante 5 dias!",
    "data_atualizacao": "2025-12-10T17:00:00.000000"
  }
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Usuário não encontrado"
}
```

---

### 6. Obter Progresso
**GET /api/progresso/{usuario_id}**

Retorna o progresso de todas as metas de um usuário.

**Parâmetros:**
- `usuario_id` (path, string, obrigatório): ID do usuário

**Response (200 OK):**
```json
{
  "usuario_id": "user_1",
  "progresso": {
    "user_1_1": {
      "concluida": true,
      "nota": "Consegui meditar por 10 minutos durante 5 dias!",
      "data_atualizacao": "2025-12-10T17:00:00.000000"
    },
    "user_1_2": {
      "concluida": false,
      "nota": null,
      "data_atualizacao": "2025-12-10T17:00:00.000000"
    }
  }
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Usuário não encontrado"
}
```

---

## Códigos de Status HTTP

- **200 OK**: Requisição bem-sucedida
- **404 Not Found**: Recurso não encontrado
- **500 Internal Server Error**: Erro interno do servidor

## Documentação Interativa

A API possui documentação interativa Swagger UI disponível em:
```
http://localhost:8000/docs
```

Documentação alternativa ReDoc:
```
http://localhost:8000/redoc
```

## Exemplos de Uso

### Exemplo com cURL

```bash
# Enviar questionário
curl -X POST http://localhost:8000/api/questionario \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "idade": 25,
    "horas_sono": 6,
    "qualidade_sono": 4,
    "nivel_atividade_fisica": 2,
    "frequencia_exercicio": 1,
    "qualidade_alimentacao": 5,
    "consumo_agua": 1.5,
    "nivel_stress": 8,
    "tempo_tela": 9,
    "apoio_social": 6
  }'

# Obter diagnóstico
curl http://localhost:8000/api/diagnostico/user_1

# Atualizar progresso
curl -X POST http://localhost:8000/api/progresso \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": "user_1",
    "meta_id": 1,
    "concluida": true,
    "nota": "Ótima experiência!"
  }'
```

### Exemplo com JavaScript (fetch)

```javascript
// Enviar questionário
const response = await fetch('http://localhost:8000/api/questionario', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    nome: 'Maria Santos',
    idade: 25,
    horas_sono: 7.5,
    qualidade_sono: 7,
    nivel_atividade_fisica: 3,
    frequencia_exercicio: 3,
    qualidade_alimentacao: 6,
    consumo_agua: 2.0,
    nivel_stress: 6,
    tempo_tela: 5.0,
    apoio_social: 7
  })
});

const diagnostico = await response.json();
console.log(diagnostico);
```

## Notas Importantes

1. **Armazenamento em Memória**: Esta versão MVP armazena dados em memória. Os dados são perdidos quando o servidor é reiniciado.

2. **CORS**: O servidor está configurado para aceitar requisições de qualquer origem (`allow_origins=["*"]`). Em produção, isso deve ser restrito.

3. **Autenticação**: Esta versão não possui autenticação. Em produção, implemente autenticação JWT ou OAuth.

4. **Rate Limiting**: Não há limitação de taxa. Em produção, implemente rate limiting.

5. **Validação**: Todos os campos são validados pelo Pydantic. Valores fora dos limites retornarão erro 422.

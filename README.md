# 🌟 Saúde+ Preventiva

Uma plataforma web MVP para ajudar estudantes universitários e jovens profissionais a melhorarem seus hábitos de sono, alimentação, exercícios e saúde mental.

## 📋 Sobre o Projeto

Saúde+ Preventiva é uma aplicação que permite aos usuários:
- Preencher um questionário rápido sobre seus hábitos de saúde
- Receber um diagnóstico personalizado **baseado em Inteligência Artificial**
- Obter 2-3 metas semanais adaptadas ao seu perfil
- Acompanhar o progresso através de um dashboard interativo
- Receber dicas personalizadas para melhorar sua qualidade de vida

🤖 **Powered by AI**: O sistema utiliza um **agente de IA** com algoritmos de Machine Learning baseados em evidências científicas e no dataset "Sleep Health and Lifestyle" para gerar recomendações inteligentes e personalizadas.

## 🏗️ Arquitetura

### Backend (Python + FastAPI)
- **Framework**: FastAPI
- **Banco de Dados**: SQLite (em memória para MVP)
- **🤖 IA/ML**: Agente de IA com algoritmos de Machine Learning
  - Análise multi-dimensional de saúde (Sono, Atividade, Alimentação, Mental)
  - Scoring inteligente com curvas gaussianas e padrões ideais
  - Geração automática de metas personalizadas
  - Sistema de insights contextualizados
  - Suporte opcional para OpenAI GPT (mensagens enriquecidas)
- **API RESTful**: Endpoints para questionário, diagnóstico, metas e progresso

### Frontend (React + Vite)
- **Framework**: React 19
- **Build Tool**: Vite
- **Estilização**: CSS personalizado
- **Cor Principal**: #528aae

### Estrutura de Diretórios

```
saudemaispreventiva/
├── backend/
│   ├── main.py              # API FastAPI principal
│   ├── ai_agent.py          # 🤖 Agente de IA para análise
│   ├── AI_AGENT_README.md   # Documentação do agente de IA
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LandingPage.jsx
│   │   │   ├── Questionnaire.jsx
│   │   │   ├── Results.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── API_DOCUMENTATION.md
└── README.md
```

## 📊 Modelos de Dados

### QuestionarioRequest
```python
{
  "nome": str,
  "idade": int,
  "horas_sono": float,
  "qualidade_sono": int (1-10),
  "nivel_atividade_fisica": int (1-5),
  "frequencia_exercicio": int,
  "qualidade_alimentacao": int (1-10),
  "consumo_agua": float,
  "nivel_stress": int (1-10),
  "tempo_tela": float,
  "apoio_social": int (1-10)
}
```

### Diagnostico
```python
{
  "usuario_id": str,
  "nome": str,
  "score_geral": int (0-100),
  "categoria": str,
  "mensagem": str,
  "areas_atencao": List[str],
  "pontos_fortes": List[str],
  "metas": List[Meta],
  "dicas": List[str],
  "data_avaliacao": str
}
```

### Meta
```python
{
  "id": int,
  "titulo": str,
  "descricao": str,
  "categoria": str,
  "prazo": str
}
```

## 🔌 Endpoints da API

### `GET /`
Retorna informações sobre a API e endpoints disponíveis.

### `POST /api/questionario`
Envia o questionário preenchido e retorna o diagnóstico completo.

**Request Body**: QuestionarioRequest
**Response**: Diagnostico

### `GET /api/diagnostico/{usuario_id}`
Retorna o diagnóstico de um usuário específico.

**Response**: Diagnostico

### `GET /api/metas/{usuario_id}`
Retorna as metas de um usuário específico.

**Response**: 
```json
{
  "usuario_id": str,
  "metas": List[Meta]
}
```

### `POST /api/progresso`
Atualiza o progresso de uma meta específica.

**Request Body**:
```json
{
  "usuario_id": str,
  "meta_id": int,
  "concluida": bool,
  "nota": str (optional)
}
```

### `GET /api/progresso/{usuario_id}`
Retorna o progresso de todas as metas de um usuário.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- npm ou yarn

### Backend

1. Navegue até o diretório backend:
```bash
cd backend
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o servidor:
```bash
python main.py
```

O backend estará disponível em `http://localhost:8000`

Documentação interativa da API: `http://localhost:8000/docs`

### Frontend

1. Navegue até o diretório frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## 🧪 Testando a Aplicação

1. Certifique-se de que o backend está rodando em `http://localhost:8000`
2. Certifique-se de que o frontend está rodando em `http://localhost:5173`
3. Acesse o frontend no navegador
4. Clique em "Começar Avaliação"
5. Preencha o questionário com suas informações
6. Veja seu diagnóstico personalizado
7. Explore o dashboard de progresso

## 🎨 Design e Identidade Visual

- **Cor Principal**: #528aae (azul sereno)
- **Idioma**: Português (Brasil)
- **Estilo**: Clean, moderno e acessível
- **Responsividade**: Mobile-first design

## 🧠 Lógica de Análise

O sistema avalia quatro áreas principais:

1. **Sono** (30% do score)
   - Horas de sono ideais: 7-9 horas
   - Qualidade subjetiva do sono

2. **Atividade Física** (25% do score)
   - Nível de atividade diária
   - Frequência de exercícios (ideal: 3-5x/semana)

3. **Alimentação** (25% do score)
   - Qualidade da dieta
   - Consumo de água (ideal: 2-3L/dia)

4. **Saúde Mental** (20% do score)
   - Nível de estresse
   - Apoio social
   - Tempo de tela

### Categorias de Diagnóstico
- **Excelente**: Score ≥ 80
- **Bom**: Score 60-79
- **Regular**: Score 40-59
- **Atenção Necessária**: Score < 40

## 📈 Futuras Melhorias

- Integração com banco de dados persistente (PostgreSQL/MongoDB)
- Sistema de autenticação e perfis de usuário
- Histórico de avaliações ao longo do tempo
- Gráficos e visualizações de progresso
- Integração com wearables (smartwatches)
- Sistema de notificações e lembretes
- Gamificação e sistema de recompensas
- Compartilhamento social de conquistas
- Integração com profissionais de saúde

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📝 Licença

Este projeto é um MVP educacional para demonstração de conceitos de desenvolvimento full-stack.

## 👥 Autores

Desenvolvido como parte do projeto Saúde+ Preventiva.

---

**Nota**: Este é um MVP educacional. Para uso em produção, recomenda-se:
- Implementar autenticação e autorização robustas
- Usar banco de dados persistente
- Adicionar testes automatizados
- Implementar logging e monitoramento
- Seguir práticas de segurança OWASP
- Consultar profissionais de saúde para validação das recomendações
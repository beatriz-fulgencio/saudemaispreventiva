#!/bin/bash

# Script de inicialização do Saúde+ Preventiva MVP

echo "🌟 Iniciando Saúde+ Preventiva..."

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para iniciar o backend
start_backend() {
    echo -e "${BLUE}📡 Iniciando Backend (FastAPI)...${NC}"
    cd backend
    
    # Verificar se o virtualenv existe
    if [ ! -d "venv" ]; then
        echo "Criando ambiente virtual..."
        python3 -m venv venv
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Instalar dependências
    echo "Instalando dependências do backend..."
    pip install -q -r requirements.txt
    
    # Iniciar servidor
    echo -e "${GREEN}✅ Backend iniciado em http://localhost:8000${NC}"
    python main.py &
    BACKEND_PID=$!
    cd ..
}

# Função para iniciar o frontend
start_frontend() {
    echo -e "${BLUE}🎨 Iniciando Frontend (React + Vite)...${NC}"
    cd frontend
    
    # Verificar se node_modules existe
    if [ ! -d "node_modules" ]; then
        echo "Instalando dependências do frontend..."
        npm install
    fi
    
    # Iniciar servidor
    echo -e "${GREEN}✅ Frontend iniciado em http://localhost:5173${NC}"
    npm run dev &
    FRONTEND_PID=$!
    cd ..
}

# Função de limpeza ao sair
cleanup() {
    echo ""
    echo "🛑 Encerrando servidores..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servidores encerrados"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT SIGTERM

# Iniciar serviços
start_backend
sleep 3
start_frontend

echo ""
echo "========================================="
echo "🚀 Saúde+ Preventiva está rodando!"
echo "========================================="
echo "📡 Backend:  http://localhost:8000"
echo "🎨 Frontend: http://localhost:5173"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Pressione Ctrl+C para encerrar"
echo "========================================="

# Manter o script rodando
wait

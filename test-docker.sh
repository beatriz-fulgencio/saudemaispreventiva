#!/bin/bash

# Test script for Saúde+ Preventiva Docker deployment
# This script tests all major API endpoints

echo "🧪 Testing Saúde+ Preventiva Docker Deployment"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        echo "Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo -e "${BLUE}Backend API Tests${NC}"
echo "-------------------"

# Test 1: API Root
test_endpoint "API Root" "http://localhost:8000/" "GET"

# Test 2: Post Questionnaire
QUESTIONNAIRE_DATA='{
    "nome": "Docker Test User",
    "idade": 30,
    "horas_sono": 7,
    "qualidade_sono": 7,
    "nivel_atividade_fisica": 3,
    "frequencia_exercicio": 3,
    "qualidade_alimentacao": 6,
    "consumo_agua": 2,
    "nivel_stress": 6,
    "tempo_tela": 6,
    "apoio_social": 7
}'
test_endpoint "POST Questionnaire" "http://localhost:8000/api/questionario" "POST" "$QUESTIONNAIRE_DATA"

# Test 3: Get Diagnostico
test_endpoint "GET Diagnostico" "http://localhost:8000/api/diagnostico/user_1" "GET"

# Test 4: Get Metas
test_endpoint "GET Metas" "http://localhost:8000/api/metas/user_1" "GET"

# Test 5: Post Progress
PROGRESS_DATA='{
    "usuario_id": "user_1",
    "meta_id": 1,
    "concluida": true,
    "nota": "Test note from automated test"
}'
test_endpoint "POST Progress" "http://localhost:8000/api/progresso" "POST" "$PROGRESS_DATA"

# Test 6: Get Progress
test_endpoint "GET Progress" "http://localhost:8000/api/progresso/user_1" "GET"

# Test 7: API Documentation
test_endpoint "API Documentation" "http://localhost:8000/docs" "GET"

echo ""
echo -e "${BLUE}Frontend Tests${NC}"
echo "---------------"

# Test 8: Frontend Root
test_endpoint "Frontend Root" "http://localhost/" "GET"

# Test 9: Frontend Assets
test_endpoint "Frontend Assets" "http://localhost/vite.svg" "GET"

echo ""
echo "=============================================="
echo -e "Test Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
echo "=============================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Application URLs:"
    echo "  Frontend: http://localhost/"
    echo "  Backend:  http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi

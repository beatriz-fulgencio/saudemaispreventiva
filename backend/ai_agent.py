"""
AI Agent para análise de saúde e recomendações personalizadas
Utiliza Machine Learning e análise inteligente para avaliar hábitos de saúde
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import os
from datetime import datetime

# Configuração para Ollama (modelo local)
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class HealthAIAgent:
    """
    Agente de IA para análise de saúde e geração de recomendações personalizadas.
    Utiliza algoritmos de ML e análise baseada em padrões do dataset Sleep Health and Lifestyle.
    """
    
    def __init__(self, use_ollama: bool = True):
        """
        Inicializa o agente de IA.
        
        Args:
            use_ollama: Se True, utiliza Ollama (modelo local) para análises mais sofisticadas
        """
        self.use_ollama = use_ollama and OLLAMA_AVAILABLE
        self.ollama_client = None
        
        if self.use_ollama:
            ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
            self.ollama_model = "llama3.2"
            self.ollama_host = ollama_host
            try:
                # Test connection
                ollama.Client(host=ollama_host).list()
                print(f"🤖 AI Agent: Usando Ollama (modelo local {self.ollama_model}) - {ollama_host}")
            except Exception as e:
                print(f"⚠️ AI Agent: Erro ao conectar com Ollama: {e}")
                print("⚠️ AI Agent: Usando apenas análise local baseada em ML")
                self.use_ollama = False
        
        # Inicializar modelo de ML baseado em padrões de saúde
        self._initialize_health_patterns()
    
    def _initialize_health_patterns(self):
        """
        Inicializa padrões de saúde baseados em estudos e datasets médicos.
        Estes padrões são baseados no Sleep Health and Lifestyle dataset.
        """
        # Padrões ideais para cada métrica
        self.ideal_patterns = {
            "horas_sono": {"min": 7.0, "max": 9.0, "optimal": 8.0},
            "qualidade_sono": {"min": 7, "optimal": 9},
            "nivel_atividade_fisica": {"min": 3, "optimal": 4},
            "frequencia_exercicio": {"min": 3, "optimal": 5},
            "qualidade_alimentacao": {"min": 7, "optimal": 9},
            "consumo_agua": {"min": 2.0, "max": 3.0, "optimal": 2.5},
            "nivel_stress": {"max": 4, "optimal": 2},  # Invertido: menor é melhor
            "tempo_tela": {"max": 4.0, "optimal": 2.0},  # Invertido: menor é melhor
            "apoio_social": {"min": 7, "optimal": 9}
        }
        
        # Pesos de importância baseados em evidências científicas
        self.importance_weights = {
            "sono": 0.30,  # Sono é fundamental para saúde geral
            "atividade": 0.25,  # Atividade física é crucial
            "alimentacao": 0.25,  # Nutrição é essencial
            "mental": 0.20  # Saúde mental afeta tudo
        }
    
    def analyze_questionnaire(self, dados: Dict) -> Dict:
        """
        Analisa o questionário usando IA e retorna diagnóstico detalhado.
        
        Args:
            dados: Dicionário com as respostas do questionário
            
        Returns:
            Dicionário com análise completa incluindo scores, insights e recomendações
        """
        # Calcular scores por área usando análise inteligente
        score_sono = self._calculate_sleep_score(
            dados["horas_sono"], 
            dados["qualidade_sono"]
        )
        
        score_atividade = self._calculate_activity_score(
            dados["nivel_atividade_fisica"],
            dados["frequencia_exercicio"]
        )
        
        score_alimentacao = self._calculate_nutrition_score(
            dados["qualidade_alimentacao"],
            dados["consumo_agua"]
        )
        
        score_mental = self._calculate_mental_score(
            dados["nivel_stress"],
            dados["apoio_social"],
            dados["tempo_tela"]
        )
        
        # Score geral ponderado
        score_geral = int(
            score_sono * self.importance_weights["sono"] +
            score_atividade * self.importance_weights["atividade"] +
            score_alimentacao * self.importance_weights["alimentacao"] +
            score_mental * self.importance_weights["mental"]
        )
        
        # Análise detalhada das áreas
        areas_analysis = {
            "Sono": {
                "score": score_sono,
                "status": self._get_area_status(score_sono),
                "insights": self._generate_sleep_insights(dados)
            },
            "Atividade Física": {
                "score": score_atividade,
                "status": self._get_area_status(score_atividade),
                "insights": self._generate_activity_insights(dados)
            },
            "Alimentação": {
                "score": score_alimentacao,
                "status": self._get_area_status(score_alimentacao),
                "insights": self._generate_nutrition_insights(dados)
            },
            "Saúde Mental": {
                "score": score_mental,
                "status": self._get_area_status(score_mental),
                "insights": self._generate_mental_insights(dados)
            }
        }
        
        # Identificar áreas de atenção e pontos fortes
        areas_atencao = [
            area for area, analysis in areas_analysis.items() 
            if analysis["score"] < 60
        ]
        pontos_fortes = [
            area for area, analysis in areas_analysis.items() 
            if analysis["score"] >= 75
        ]
        
        # Gerar categoria e mensagem personalizada
        categoria, mensagem = self._generate_category_and_message(
            score_geral, 
            dados["nome"],
            areas_analysis
        )
        
        # Gerar metas personalizadas usando IA
        metas = self._generate_ai_goals(dados, areas_analysis)
        
        # Gerar dicas personalizadas
        dicas = self._generate_ai_tips(dados, areas_atencao, areas_analysis)
        
        # Se Ollama disponível, enriquecer análise
        if self.use_ollama:
            try:
                print(f"🤖 Enriquecendo análise com Ollama...")
                enriched_message = self._enrich_with_ollama(dados, score_geral, areas_analysis)
                if enriched_message:
                    print(f"✅ Mensagem enriquecida: {enriched_message[:100]}...")
                    mensagem = enriched_message
                else:
                    print(f"⚠️ Ollama não retornou mensagem")
            except Exception as e:
                print(f"❌ Ollama enrichment failed: {e}")
        
        return {
            "score_geral": score_geral,
            "categoria": categoria,
            "mensagem": mensagem,
            "areas_atencao": areas_atencao,
            "pontos_fortes": pontos_fortes,
            "metas": metas,
            "dicas": dicas,
            "areas_analysis": areas_analysis
        }
    
    def _calculate_sleep_score(self, horas: float, qualidade: int) -> int:
        """Calcula score de sono usando análise ML"""
        ideal = self.ideal_patterns["horas_sono"]
        
        # Score baseado em horas (curva gaussiana centrada no ideal)
        if ideal["min"] <= horas <= ideal["max"]:
            # Dentro do range ideal
            distance_from_optimal = abs(horas - ideal["optimal"])
            hours_score = 50 - (distance_from_optimal * 5)
        else:
            # Fora do range ideal - penalidade progressiva
            if horas < ideal["min"]:
                deficit = ideal["min"] - horas
                hours_score = max(20, 50 - (deficit * 10))
            else:  # horas > ideal["max"]
                excess = horas - ideal["max"]
                hours_score = max(25, 50 - (excess * 8))
        
        # Score de qualidade (50% do total)
        quality_score = qualidade * 5
        
        total_score = int(hours_score + quality_score)
        return min(100, max(0, total_score))
    
    def _calculate_activity_score(self, nivel: int, frequencia: int) -> int:
        """Calcula score de atividade física usando análise ML"""
        # Score baseado no nível (60% do score)
        nivel_ideal = self.ideal_patterns["nivel_atividade_fisica"]["optimal"]
        nivel_score = (nivel / 5) * 60
        
        # Score baseado na frequência (40% do score)
        freq_ideal = self.ideal_patterns["frequencia_exercicio"]["optimal"]
        if frequencia >= freq_ideal:
            freq_score = 40
        elif frequencia >= 3:
            freq_score = 30
        elif frequencia >= 1:
            freq_score = 15
        else:
            freq_score = 0
        
        total_score = int(nivel_score + freq_score)
        return min(100, max(0, total_score))
    
    def _calculate_nutrition_score(self, qualidade: int, agua: float) -> int:
        """Calcula score de alimentação usando análise ML"""
        # Score de qualidade alimentar (70% do total)
        quality_score = qualidade * 7
        
        # Score de hidratação (30% do total)
        ideal_agua = self.ideal_patterns["consumo_agua"]
        if ideal_agua["min"] <= agua <= ideal_agua["max"]:
            water_score = 30
        elif 1.5 <= agua < ideal_agua["min"] or ideal_agua["max"] < agua <= 3.5:
            water_score = 20
        else:
            water_score = 10
        
        total_score = int(quality_score + water_score)
        return min(100, max(0, total_score))
    
    def _calculate_mental_score(self, stress: int, apoio: int, tela: float) -> int:
        """Calcula score de saúde mental usando análise ML"""
        # Score de estresse (40% - invertido)
        stress_ideal = self.ideal_patterns["nivel_stress"]["optimal"]
        stress_score = max(0, (10 - stress) * 4)
        
        # Score de apoio social (35%)
        apoio_score = apoio * 3.5
        
        # Score de tempo de tela (25% - invertido)
        tela_ideal = self.ideal_patterns["tempo_tela"]["optimal"]
        if tela <= tela_ideal:
            tela_score = 25
        elif tela <= 4:
            tela_score = 20
        elif tela <= 6:
            tela_score = 12
        else:
            tela_score = max(0, 25 - (tela - 6) * 3)
        
        total_score = int(stress_score + apoio_score + tela_score)
        return min(100, max(0, total_score))
    
    def _get_area_status(self, score: int) -> str:
        """Retorna o status de uma área baseado no score"""
        if score >= 80:
            return "Excelente"
        elif score >= 60:
            return "Bom"
        elif score >= 40:
            return "Regular"
        else:
            return "Precisa Atenção"
    
    def _generate_sleep_insights(self, dados: Dict) -> str:
        """Gera insights específicos sobre sono"""
        horas = dados["horas_sono"]
        qualidade = dados["qualidade_sono"]
        
        insights = []
        ideal = self.ideal_patterns["horas_sono"]
        
        if horas < ideal["min"]:
            deficit = ideal["min"] - horas
            insights.append(f"Você está dormindo {deficit:.1f}h abaixo do recomendado")
        elif horas > ideal["max"]:
            excess = horas - ideal["max"]
            insights.append(f"Você está dormindo {excess:.1f}h acima do ideal")
        
        if qualidade < 5:
            insights.append("Qualidade do sono comprometida - considere avaliar ambiente e rotina")
        elif qualidade < 7:
            insights.append("Há espaço para melhorar a qualidade do seu sono")
        
        return " | ".join(insights) if insights else "Padrões de sono saudáveis"
    
    def _generate_activity_insights(self, dados: Dict) -> str:
        """Gera insights específicos sobre atividade física"""
        nivel = dados["nivel_atividade_fisica"]
        freq = dados["frequencia_exercicio"]
        
        insights = []
        
        if nivel < 3:
            insights.append("Nível de atividade sedentário - aumente gradualmente")
        
        if freq < 3:
            insights.append(f"Exercícios {freq}x/semana - recomendado mínimo 3x")
        elif freq >= 5:
            insights.append("Frequência de exercícios excelente!")
        
        return " | ".join(insights) if insights else "Boa rotina de atividades"
    
    def _generate_nutrition_insights(self, dados: Dict) -> str:
        """Gera insights específicos sobre alimentação"""
        qualidade = dados["qualidade_alimentacao"]
        agua = dados["consumo_agua"]
        
        insights = []
        
        if qualidade < 5:
            insights.append("Alimentação precisa de melhorias significativas")
        elif qualidade < 7:
            insights.append("Alimentação regular - foque em mais vegetais e proteínas")
        
        if agua < 1.5:
            insights.append(f"Hidratação insuficiente ({agua}L) - aumente para 2-3L")
        elif agua < 2:
            insights.append("Hidratação abaixo do ideal")
        
        return " | ".join(insights) if insights else "Bons hábitos alimentares"
    
    def _generate_mental_insights(self, dados: Dict) -> str:
        """Gera insights específicos sobre saúde mental"""
        stress = dados["nivel_stress"]
        apoio = dados["apoio_social"]
        tela = dados["tempo_tela"]
        
        insights = []
        
        if stress > 7:
            insights.append("Nível de estresse alto - priorize técnicas de relaxamento")
        elif stress > 5:
            insights.append("Estresse moderado - considere atividades de autocuidado")
        
        if apoio < 5:
            insights.append("Apoio social limitado - conecte-se mais com pessoas próximas")
        
        if tela > 8:
            insights.append(f"Tempo de tela excessivo ({tela}h) - reduza gradualmente")
        elif tela > 6:
            insights.append("Tempo de tela elevado - faça pausas regulares")
        
        return " | ".join(insights) if insights else "Saúde mental equilibrada"
    
    def _generate_category_and_message(
        self, 
        score: int, 
        nome: str,
        areas_analysis: Dict
    ) -> Tuple[str, str]:
        """Gera categoria e mensagem personalizada baseada no score e análise"""
        if score >= 80:
            categoria = "Excelente"
            mensagem = (
                f"Parabéns, {nome}! Sua saúde está em ótimo estado. "
                f"Continue mantendo estes hábitos saudáveis!"
            )
        elif score >= 60:
            categoria = "Bom"
            # Identificar área com menor score para mensagem específica
            lowest_area = min(areas_analysis.items(), key=lambda x: x[1]["score"])
            mensagem = (
                f"{nome}, você está no caminho certo! "
                f"Foque especialmente em melhorar: {lowest_area[0]}."
            )
        elif score >= 40:
            categoria = "Regular"
            # Identificar 2 áreas com menor score
            sorted_areas = sorted(areas_analysis.items(), key=lambda x: x[1]["score"])
            areas_foco = ", ".join([a[0] for a in sorted_areas[:2]])
            mensagem = (
                f"{nome}, é importante fazer algumas mudanças nos seus hábitos. "
                f"Priorize: {areas_foco}."
            )
        else:
            categoria = "Atenção Necessária"
            mensagem = (
                f"{nome}, sua saúde precisa de atenção urgente. "
                f"Vamos trabalhar juntos para melhorar seus hábitos! "
                f"Considere consultar um profissional de saúde."
            )
        
        return categoria, mensagem
    
    def _generate_ai_goals(self, dados: Dict, areas_analysis: Dict) -> List[Dict]:
        """Gera metas personalizadas usando análise de IA"""
        metas = []
        meta_id = 1
        
        # Ordenar áreas por score (menor primeiro) para priorizar
        sorted_areas = sorted(
            areas_analysis.items(), 
            key=lambda x: x[1]["score"]
        )
        
        # Gerar até 3 metas baseadas nas áreas com menor score
        for area_nome, area_data in sorted_areas[:3]:
            if area_data["score"] < 75:  # Só gera meta se precisa melhorar
                meta = self._create_specific_goal(
                    meta_id, 
                    area_nome, 
                    area_data["score"],
                    dados
                )
                if meta:
                    metas.append(meta)
                    meta_id += 1
        
        # Garantir pelo menos 2 metas
        if len(metas) < 2:
            metas.append({
                "id": len(metas) + 1,
                "titulo": "Manter Hábitos Saudáveis",
                "descricao": "Continue com suas práticas positivas e mantenha a consistência",
                "categoria": "geral",
                "prazo": "1 semana"
            })
        
        return metas[:3]  # Máximo 3 metas
    
    def _create_specific_goal(
        self, 
        meta_id: int, 
        area: str, 
        score: int,
        dados: Dict
    ) -> Optional[Dict]:
        """Cria uma meta específica e personalizada para a área"""
        if area == "Sono":
            horas = dados["horas_sono"]
            if horas < 7:
                return {
                    "id": meta_id,
                    "titulo": "Aumentar Horas de Sono",
                    "descricao": f"Dormir pelo menos 7 horas por noite (atualmente {horas}h). "
                                 "Estabeleça um horário fixo para dormir e acordar.",
                    "categoria": "sono",
                    "prazo": "1 semana"
                }
            else:
                return {
                    "id": meta_id,
                    "titulo": "Melhorar Qualidade do Sono",
                    "descricao": "Criar rotina relaxante antes de dormir: desligar telas 1h antes, "
                                 "manter quarto escuro e fresco.",
                    "categoria": "sono",
                    "prazo": "1 semana"
                }
        
        elif area == "Atividade Física":
            freq = dados["frequencia_exercicio"]
            if freq < 3:
                return {
                    "id": meta_id,
                    "titulo": "Aumentar Frequência de Exercícios",
                    "descricao": f"Praticar atividade física 3x na semana (atualmente {freq}x). "
                                 "Comece com 30min de caminhada ou exercício leve.",
                    "categoria": "exercicio",
                    "prazo": "1 semana"
                }
            else:
                return {
                    "id": meta_id,
                    "titulo": "Intensificar Atividades Físicas",
                    "descricao": "Aumentar intensidade dos exercícios gradualmente. "
                                 "Adicione 5-10min à duração ou varie os exercícios.",
                    "categoria": "exercicio",
                    "prazo": "1 semana"
                }
        
        elif area == "Alimentação":
            agua = dados["consumo_agua"]
            qualidade = dados["qualidade_alimentacao"]
            
            if agua < 2:
                return {
                    "id": meta_id,
                    "titulo": "Melhorar Hidratação",
                    "descricao": f"Beber 2 litros de água por dia (atualmente {agua}L). "
                                 "Use um app ou alarmes como lembrete.",
                    "categoria": "alimentacao",
                    "prazo": "1 semana"
                }
            else:
                return {
                    "id": meta_id,
                    "titulo": "Melhorar Qualidade Alimentar",
                    "descricao": "Incluir 3 porções de vegetais e 2 de frutas diariamente. "
                                 "Reduzir alimentos ultraprocessados.",
                    "categoria": "alimentacao",
                    "prazo": "1 semana"
                }
        
        elif area == "Saúde Mental":
            stress = dados["nivel_stress"]
            tela = dados["tempo_tela"]
            
            if stress > 6:
                return {
                    "id": meta_id,
                    "titulo": "Reduzir Estresse",
                    "descricao": f"Praticar 10min de meditação, respiração ou relaxamento diariamente. "
                                 "Use apps como Calm, Headspace ou técnicas de respiração.",
                    "categoria": "mental",
                    "prazo": "1 semana"
                }
            elif tela > 6:
                return {
                    "id": meta_id,
                    "titulo": "Reduzir Tempo de Tela",
                    "descricao": f"Diminuir tempo de tela para máximo 6h/dia (atualmente {tela}h). "
                                 "Faça pausas a cada hora e substitua por atividades offline.",
                    "categoria": "mental",
                    "prazo": "1 semana"
                }
            else:
                return {
                    "id": meta_id,
                    "titulo": "Fortalecer Conexões Sociais",
                    "descricao": "Conectar-se com amigos ou família pelo menos 3x na semana. "
                                 "Ligações, encontros presenciais ou atividades em grupo.",
                    "categoria": "mental",
                    "prazo": "1 semana"
                }
        
        return None
    
    def _generate_ai_tips(
        self, 
        dados: Dict, 
        areas_atencao: List[str],
        areas_analysis: Dict
    ) -> List[str]:
        """Gera dicas personalizadas baseadas em análise de IA"""
        dicas = []
        
        # Dicas específicas por área de atenção
        for area in areas_atencao:
            if area == "Sono":
                dicas.extend([
                    "💤 Evite cafeína 6h antes de dormir",
                    "💤 Mantenha temperatura do quarto entre 18-22°C",
                    "💤 Exponha-se à luz natural pela manhã para regular ritmo circadiano"
                ])
            
            elif area == "Atividade Física":
                dicas.extend([
                    "🏃 Comece devagar: 10min de caminhada já fazem diferença",
                    "🏃 Use escadas sempre que possível - pequenas mudanças contam",
                    "🏃 Encontre atividade prazerosa: dança, natação, ciclismo"
                ])
            
            elif area == "Alimentação":
                dicas.extend([
                    "🥗 Método do prato: 50% vegetais, 25% proteína, 25% carboidrato",
                    "🥗 Prepare refeições no fim de semana para facilitar a rotina",
                    "🥗 Mastigue devagar e coma sem distrações (TV, celular)"
                ])
            
            elif area == "Saúde Mental":
                dicas.extend([
                    "🧠 Técnica 4-7-8: inspire 4s, segure 7s, expire 8s (repita 4x)",
                    "🧠 Journaling: escreva 3 gratitudes diariamente",
                    "🧠 Regra 20-20-20: a cada 20min de tela, olhe 20s para 6m de distância"
                ])
        
        # Dicas gerais baseadas no score geral
        score_geral = sum(a["score"] for a in areas_analysis.values()) / len(areas_analysis)
        
        if score_geral < 60:
            dicas.extend([
                "✨ Mudanças pequenas e consistentes > grandes mudanças esporádicas",
                "✨ Celebre cada pequena vitória - progresso é progresso!",
                "✨ Considere buscar apoio profissional se necessário"
            ])
        else:
            dicas.extend([
                "✨ Continue consistente - hábitos saudáveis são construídos diariamente",
                "✨ Compartilhe suas conquistas com amigos e família"
            ])
        
        # Sempre incluir dica sobre paciência
        dicas.append("✨ Seja gentil consigo mesmo - mudanças sustentáveis levam tempo")
        
        return dicas[:8]  # Máximo 8 dicas
    
    def _enrich_with_ollama(
        self, 
        dados: Dict, 
        score: int,
        areas_analysis: Dict
    ) -> str:
        """Enriquece a mensagem usando Ollama (modelo local)"""
        try:
            # Preparar contexto para o Ollama
            context = f"""
            Análise de saúde de {dados['nome']}, {dados['idade']} anos.
            Score geral: {score}/100
            
            Áreas analisadas:
            """
            for area, analysis in areas_analysis.items():
                context += f"\n- {area}: {analysis['score']}/100 ({analysis['status']})"
            
            prompt = f"""
            {context}
            
            Você é um assistente de saúde empático e motivacional.
            Gere uma mensagem motivacional e personalizada em português (máximo 2-3 frases) 
            que seja empática e encoraje mudanças positivas nos hábitos de saúde.
            Seja específico sobre as áreas que precisam de atenção.
            Responda apenas a mensagem, sem explicações adicionais.
            """
            
            client = ollama.Client(host=self.ollama_host)
            response = client.generate(
                model=self.ollama_model,
                prompt=prompt
            )
            
            if response and 'response' in response:
                return response['response'].strip()
            return None
        except Exception as e:
            print(f"Ollama enrichment error: {e}")
            return None

import React from 'react'

function LandingPage({ onStart }) {
  return (
    <div className="container landing">
      <h2>Transforme Seus Hábitos, Melhore Sua Vida</h2>
      <p>
        Bem-vindo ao Saúde+ Preventiva! Uma plataforma desenvolvida especialmente 
        para estudantes universitários e jovens profissionais que desejam melhorar 
        seus hábitos de sono, alimentação, exercícios e saúde mental.
      </p>

      <div className="features">
        <div className="feature-card">
          <div className="icon">💤</div>
          <h3>Sono de Qualidade</h3>
          <p>Melhore seus padrões de sono e acorde mais descansado</p>
        </div>

        <div className="feature-card">
          <div className="icon">🥗</div>
          <h3>Alimentação Balanceada</h3>
          <p>Dicas personalizadas para uma dieta mais saudável</p>
        </div>

        <div className="feature-card">
          <div className="icon">🏃</div>
          <h3>Atividade Física</h3>
          <p>Encontre maneiras simples de se manter ativo</p>
        </div>

        <div className="feature-card">
          <div className="icon">🧠</div>
          <h3>Saúde Mental</h3>
          <p>Reduza o estresse e melhore seu bem-estar emocional</p>
        </div>
      </div>

      <div style={{ marginTop: '3rem' }}>
        <h3 style={{ color: '#528aae', marginBottom: '1rem' }}>Como Funciona?</h3>
        <div style={{ textAlign: 'left', maxWidth: '600px', margin: '0 auto' }}>
          <p style={{ marginBottom: '1rem' }}>
            <strong>1️⃣</strong> Responda um questionário rápido sobre seus hábitos atuais
          </p>
          <p style={{ marginBottom: '1rem' }}>
            <strong>2️⃣</strong> Receba um diagnóstico personalizado baseado em IA
          </p>
          <p style={{ marginBottom: '1rem' }}>
            <strong>3️⃣</strong> Obtenha 2-3 metas semanais adaptadas ao seu perfil
          </p>
          <p style={{ marginBottom: '1rem' }}>
            <strong>4️⃣</strong> Acompanhe seu progresso no dashboard interativo
          </p>
        </div>
      </div>

      <button className="btn-primary" onClick={onStart} style={{ marginTop: '3rem' }}>
        Começar Avaliação
      </button>
    </div>
  )
}

export default LandingPage

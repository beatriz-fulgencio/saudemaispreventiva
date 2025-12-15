import React from 'react'

function Results({ diagnostico, onViewDashboard, onBackToLanding }) {
  const getScoreColor = (score) => {
    if (score >= 80) return '#4caf50'
    if (score >= 60) return '#528aae'
    if (score >= 40) return '#ff9800'
    return '#f44336'
  }

  return (
    <div className="container results">
      <div className="score-card">
        <div 
          className="score-circle" 
          style={{ background: getScoreColor(diagnostico.score_geral) }}
        >
          <div className="score">{diagnostico.score_geral}</div>
          <div className="label">Score</div>
        </div>
        <div className="category">{diagnostico.categoria}</div>
        <div className="message">{diagnostico.mensagem}</div>
      </div>

      {/* Áreas de Atenção */}
      {diagnostico.areas_atencao.length > 0 && (
        <div className="section">
          <h3>⚠️ Áreas que Precisam de Atenção</h3>
          <div className="areas-grid">
            {diagnostico.areas_atencao.map((area, index) => (
              <div key={index} className="area-badge area-attention">
                {area}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pontos Fortes */}
      {diagnostico.pontos_fortes.length > 0 && (
        <div className="section">
          <h3>💪 Seus Pontos Fortes</h3>
          <div className="areas-grid">
            {diagnostico.pontos_fortes.map((area, index) => (
              <div key={index} className="area-badge area-strength">
                {area}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Metas Semanais */}
      <div className="section">
        <h3>🎯 Suas Metas para Esta Semana</h3>
        <p style={{ color: '#666', marginBottom: '0.8rem' }}>
          Concentre-se nestas {diagnostico.metas.length} metas para começar sua jornada de transformação:
        </p>
        <p style={{ 
          color: '#528aae', 
          fontSize: '0.9rem', 
          marginBottom: '1.5rem',
          fontStyle: 'italic'
        }}>
          🤖 Metas geradas por IA baseadas na sua análise personalizada
        </p>
        <div className="goals-list">
          {diagnostico.metas.map((meta) => (
            <div key={meta.id} className="goal-card">
              <div className="goal-header">
                <div className="goal-title">{meta.titulo}</div>
                <div className="goal-badge">{meta.prazo}</div>
              </div>
              <div className="goal-description">{meta.descricao}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Dicas Personalizadas */}
      <div className="section">
        <h3>💡 Dicas Personalizadas para Você</h3>
        <div className="tips-list">
          {diagnostico.dicas.map((dica, index) => (
            <div key={index} className="tip-item">
              {dica}
            </div>
          ))}
        </div>
      </div>

      <div className="button-group" style={{ marginTop: '2rem' }}>
        <button className="btn-secondary" onClick={onBackToLanding}>
          Nova Avaliação
        </button>
        <button className="btn-primary" onClick={onViewDashboard}>
          Ver Dashboard de Progresso
        </button>
      </div>
    </div>
  )
}

export default Results

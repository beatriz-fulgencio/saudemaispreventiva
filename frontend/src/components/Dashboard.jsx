import React, { useState } from 'react'

function Dashboard({ diagnostico, onBack }) {
  const [progressData, setProgressData] = useState(
    diagnostico.metas.reduce((acc, meta) => {
      acc[meta.id] = { concluida: false, nota: '' }
      return acc
    }, {})
  )

  const handleCheckboxChange = (metaId) => {
    setProgressData(prev => ({
      ...prev,
      [metaId]: {
        ...prev[metaId],
        concluida: !prev[metaId].concluida
      }
    }))
  }

  const handleNotaChange = (metaId, nota) => {
    setProgressData(prev => ({
      ...prev,
      [metaId]: {
        ...prev[metaId],
        nota
      }
    }))
  }

  const calcularProgresso = () => {
    const total = diagnostico.metas.length
    const concluidas = Object.values(progressData).filter(p => p.concluida).length
    return Math.round((concluidas / total) * 100)
  }

  const progresso = calcularProgresso()

  return (
    <div className="container dashboard">
      <div className="score-card">
        <h2 style={{ color: '#528aae', marginBottom: '1rem' }}>
          Dashboard de Progresso
        </h2>
        <p style={{ color: '#666', marginBottom: '1.5rem' }}>
          Acompanhe o desenvolvimento das suas metas semanais
        </p>

        <div style={{ marginBottom: '2rem' }}>
          <div style={{ 
            background: '#f5f8fa', 
            height: '30px', 
            borderRadius: '15px',
            overflow: 'hidden',
            position: 'relative'
          }}>
            <div style={{
              background: 'linear-gradient(90deg, #528aae 0%, #3a6280 100%)',
              height: '100%',
              width: `${progresso}%`,
              transition: 'width 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold'
            }}>
              {progresso > 10 && `${progresso}%`}
            </div>
          </div>
          <p style={{ textAlign: 'center', marginTop: '0.5rem', color: '#666' }}>
            {progresso}% das metas concluídas
          </p>
        </div>
      </div>

      {/* Informações do Usuário */}
      <div className="section">
        <h3>👤 Seu Perfil</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div style={{ padding: '1rem', background: '#f5f8fa', borderRadius: '8px' }}>
            <div style={{ fontSize: '0.9rem', color: '#666' }}>Nome</div>
            <div style={{ fontSize: '1.1rem', fontWeight: '600', marginTop: '0.3rem' }}>
              {diagnostico.nome}
            </div>
          </div>
          <div style={{ padding: '1rem', background: '#f5f8fa', borderRadius: '8px' }}>
            <div style={{ fontSize: '0.9rem', color: '#666' }}>Score Geral</div>
            <div style={{ fontSize: '1.1rem', fontWeight: '600', marginTop: '0.3rem' }}>
              {diagnostico.score_geral}/100
            </div>
          </div>
          <div style={{ padding: '1rem', background: '#f5f8fa', borderRadius: '8px' }}>
            <div style={{ fontSize: '0.9rem', color: '#666' }}>Categoria</div>
            <div style={{ fontSize: '1.1rem', fontWeight: '600', marginTop: '0.3rem' }}>
              {diagnostico.categoria}
            </div>
          </div>
          <div style={{ padding: '1rem', background: '#f5f8fa', borderRadius: '8px' }}>
            <div style={{ fontSize: '0.9rem', color: '#666' }}>Data da Avaliação</div>
            <div style={{ fontSize: '1.1rem', fontWeight: '600', marginTop: '0.3rem' }}>
              {new Date(diagnostico.data_avaliacao).toLocaleDateString('pt-BR')}
            </div>
          </div>
        </div>
      </div>

      {/* Metas e Progresso */}
      <div className="section">
        <h3>🎯 Acompanhamento de Metas</h3>
        <p style={{ color: '#666', marginBottom: '1.5rem' }}>
          Marque as metas conforme você as completa e adicione notas sobre seu progresso
        </p>

        {diagnostico.metas.map((meta) => (
          <div key={meta.id} style={{ marginBottom: '2rem' }}>
            <div className="goal-card">
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                <input
                  type="checkbox"
                  className="checkbox"
                  checked={progressData[meta.id]?.concluida || false}
                  onChange={() => handleCheckboxChange(meta.id)}
                  style={{ marginTop: '0.3rem' }}
                />
                <div style={{ flex: 1 }}>
                  <div className="goal-header">
                    <div className="goal-title" style={{
                      textDecoration: progressData[meta.id]?.concluida ? 'line-through' : 'none',
                      opacity: progressData[meta.id]?.concluida ? 0.6 : 1
                    }}>
                      {meta.titulo}
                    </div>
                    <div className={`progress-status ${progressData[meta.id]?.concluida ? 'status-completed' : 'status-pending'}`}>
                      {progressData[meta.id]?.concluida ? '✓ Concluída' : 'Pendente'}
                    </div>
                  </div>
                  <div className="goal-description">{meta.descricao}</div>
                  
                  <div style={{ marginTop: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.5rem', color: '#666' }}>
                      Adicionar nota (opcional):
                    </label>
                    <textarea
                      value={progressData[meta.id]?.nota || ''}
                      onChange={(e) => handleNotaChange(meta.id, e.target.value)}
                      placeholder="Como foi sua experiência com esta meta? O que funcionou bem?"
                      style={{
                        width: '100%',
                        padding: '0.8rem',
                        border: '2px solid #e0e0e0',
                        borderRadius: '8px',
                        fontSize: '0.95rem',
                        fontFamily: 'inherit',
                        minHeight: '80px',
                        resize: 'vertical'
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Motivação */}
      <div className="section" style={{ 
        background: 'linear-gradient(135deg, #528aae 0%, #3a6280 100%)',
        color: 'white',
        textAlign: 'center'
      }}>
        <h3 style={{ color: 'white' }}>💪 Continue Assim!</h3>
        <p style={{ fontSize: '1.1rem', marginTop: '1rem' }}>
          {progresso === 100 
            ? '🎉 Parabéns! Você completou todas as suas metas desta semana!'
            : progresso >= 50
            ? '👏 Você está indo muito bem! Continue com o ótimo trabalho!'
            : '🌟 Cada pequeno passo conta. Você está no caminho certo!'
          }
        </p>
        <p style={{ fontSize: '0.95rem', marginTop: '0.5rem', opacity: 0.9 }}>
          Lembre-se: mudanças sustentáveis levam tempo. Seja gentil consigo mesmo!
        </p>
      </div>

      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <button className="btn-primary" onClick={onBack}>
          Fazer Nova Avaliação
        </button>
      </div>
    </div>
  )
}

export default Dashboard

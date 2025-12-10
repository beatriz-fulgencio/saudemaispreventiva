import React, { useState } from 'react'

const API_URL = 'http://localhost:8000'

function Questionnaire({ onComplete, onBack }) {
  const [formData, setFormData] = useState({
    nome: '',
    idade: 25,
    horas_sono: 7,
    qualidade_sono: 5,
    nivel_atividade_fisica: 3,
    frequencia_exercicio: 2,
    qualidade_alimentacao: 5,
    consumo_agua: 2,
    nivel_stress: 5,
    tempo_tela: 5,
    apoio_social: 5
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'nome' ? value : parseFloat(value)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/questionario`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error('Erro ao enviar questionário')
      }

      const result = await response.json()
      onComplete(result)
    } catch (err) {
      setError('Erro ao processar o questionário. Por favor, tente novamente.')
      console.error(err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="container">
      <div className="questionnaire">
        <h2>Questionário de Saúde</h2>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '2rem' }}>
          Preencha as informações abaixo para receber sua avaliação personalizada
        </p>

        <form onSubmit={handleSubmit}>
          {/* Informações Pessoais */}
          <div className="form-group">
            <label htmlFor="nome">Nome Completo *</label>
            <input
              type="text"
              id="nome"
              name="nome"
              value={formData.nome}
              onChange={handleChange}
              required
              placeholder="Digite seu nome"
            />
          </div>

          <div className="form-group">
            <label htmlFor="idade">Idade *</label>
            <input
              type="number"
              id="idade"
              name="idade"
              value={formData.idade}
              onChange={handleChange}
              required
              min="15"
              max="100"
            />
          </div>

          {/* Sono */}
          <h3 style={{ color: '#528aae', marginTop: '2rem', marginBottom: '1rem' }}>
            💤 Sono
          </h3>

          <div className="form-group">
            <label htmlFor="horas_sono">
              Quantas horas você dorme por noite? *
            </label>
            <input
              type="number"
              id="horas_sono"
              name="horas_sono"
              value={formData.horas_sono}
              onChange={handleChange}
              required
              min="0"
              max="24"
              step="0.5"
            />
            <small>Horas por noite (exemplo: 7.5)</small>
          </div>

          <div className="form-group">
            <label htmlFor="qualidade_sono">
              Como você avalia a qualidade do seu sono? *
              <span className="range-value">{formData.qualidade_sono}/10</span>
            </label>
            <input
              type="range"
              id="qualidade_sono"
              name="qualidade_sono"
              value={formData.qualidade_sono}
              onChange={handleChange}
              min="1"
              max="10"
            />
            <small>1 = Péssimo | 10 = Excelente</small>
          </div>

          {/* Atividade Física */}
          <h3 style={{ color: '#528aae', marginTop: '2rem', marginBottom: '1rem' }}>
            🏃 Atividade Física
          </h3>

          <div className="form-group">
            <label htmlFor="nivel_atividade_fisica">
              Qual seu nível de atividade física diária? *
              <span className="range-value">{formData.nivel_atividade_fisica}/5</span>
            </label>
            <input
              type="range"
              id="nivel_atividade_fisica"
              name="nivel_atividade_fisica"
              value={formData.nivel_atividade_fisica}
              onChange={handleChange}
              min="1"
              max="5"
            />
            <small>1 = Sedentário | 5 = Muito ativo</small>
          </div>

          <div className="form-group">
            <label htmlFor="frequencia_exercicio">
              Quantas vezes por semana você faz exercícios? *
            </label>
            <input
              type="number"
              id="frequencia_exercicio"
              name="frequencia_exercicio"
              value={formData.frequencia_exercicio}
              onChange={handleChange}
              required
              min="0"
              max="7"
            />
            <small>Vezes por semana</small>
          </div>

          {/* Alimentação */}
          <h3 style={{ color: '#528aae', marginTop: '2rem', marginBottom: '1rem' }}>
            🥗 Alimentação
          </h3>

          <div className="form-group">
            <label htmlFor="qualidade_alimentacao">
              Como você avalia sua alimentação? *
              <span className="range-value">{formData.qualidade_alimentacao}/10</span>
            </label>
            <input
              type="range"
              id="qualidade_alimentacao"
              name="qualidade_alimentacao"
              value={formData.qualidade_alimentacao}
              onChange={handleChange}
              min="1"
              max="10"
            />
            <small>1 = Péssima | 10 = Excelente</small>
          </div>

          <div className="form-group">
            <label htmlFor="consumo_agua">
              Quantos litros de água você bebe por dia? *
            </label>
            <input
              type="number"
              id="consumo_agua"
              name="consumo_agua"
              value={formData.consumo_agua}
              onChange={handleChange}
              required
              min="0"
              max="10"
              step="0.5"
            />
            <small>Litros por dia (exemplo: 2.5)</small>
          </div>

          {/* Saúde Mental */}
          <h3 style={{ color: '#528aae', marginTop: '2rem', marginBottom: '1rem' }}>
            🧠 Saúde Mental
          </h3>

          <div className="form-group">
            <label htmlFor="nivel_stress">
              Qual seu nível de estresse atual? *
              <span className="range-value">{formData.nivel_stress}/10</span>
            </label>
            <input
              type="range"
              id="nivel_stress"
              name="nivel_stress"
              value={formData.nivel_stress}
              onChange={handleChange}
              min="1"
              max="10"
            />
            <small>1 = Muito baixo | 10 = Muito alto</small>
          </div>

          <div className="form-group">
            <label htmlFor="tempo_tela">
              Quantas horas por dia você passa em telas (celular, computador, TV)? *
            </label>
            <input
              type="number"
              id="tempo_tela"
              name="tempo_tela"
              value={formData.tempo_tela}
              onChange={handleChange}
              required
              min="0"
              max="24"
              step="0.5"
            />
            <small>Horas por dia</small>
          </div>

          <div className="form-group">
            <label htmlFor="apoio_social">
              Como você avalia seu apoio social (amigos, família)? *
              <span className="range-value">{formData.apoio_social}/10</span>
            </label>
            <input
              type="range"
              id="apoio_social"
              name="apoio_social"
              value={formData.apoio_social}
              onChange={handleChange}
              min="1"
              max="10"
            />
            <small>1 = Muito baixo | 10 = Muito alto</small>
          </div>

          {error && (
            <div style={{ 
              color: '#f44336', 
              background: '#ffebee', 
              padding: '1rem', 
              borderRadius: '8px',
              marginTop: '1rem'
            }}>
              {error}
            </div>
          )}

          <div className="button-group">
            <button 
              type="button" 
              className="btn-secondary" 
              onClick={onBack}
              disabled={isSubmitting}
            >
              Voltar
            </button>
            <button 
              type="submit" 
              className="btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Processando...' : 'Enviar Avaliação'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Questionnaire

import { useState } from 'react'
import './App.css'
import LandingPage from './components/LandingPage'
import Questionnaire from './components/Questionnaire'
import Results from './components/Results'
import Dashboard from './components/Dashboard'

function App() {
  const [currentPage, setCurrentPage] = useState('landing')
  const [diagnostico, setDiagnostico] = useState(null)

  const handleStartQuestionnaire = () => {
    setCurrentPage('questionnaire')
  }

  const handleQuestionnaireComplete = (result) => {
    setDiagnostico(result)
    setCurrentPage('results')
  }

  const handleViewDashboard = () => {
    setCurrentPage('dashboard')
  }

  const handleBackToLanding = () => {
    setCurrentPage('landing')
    setDiagnostico(null)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🌟 Saúde+ Preventiva</h1>
        <p>Seu parceiro para uma vida mais saudável</p>
      </header>

      {currentPage === 'landing' && (
        <LandingPage onStart={handleStartQuestionnaire} />
      )}

      {currentPage === 'questionnaire' && (
        <Questionnaire 
          onComplete={handleQuestionnaireComplete}
          onBack={handleBackToLanding}
        />
      )}

      {currentPage === 'results' && diagnostico && (
        <Results 
          diagnostico={diagnostico}
          onViewDashboard={handleViewDashboard}
          onBackToLanding={handleBackToLanding}
        />
      )}

      {currentPage === 'dashboard' && diagnostico && (
        <Dashboard 
          diagnostico={diagnostico}
          onBack={handleBackToLanding}
        />
      )}
    </div>
  )
}

export default App

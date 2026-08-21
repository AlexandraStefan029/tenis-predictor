import { useState } from "react";
import FormMeci from "./components/FormMeci";
import RezultatPredictie from "./components/RezultatPredictie";
import ValueBet from "./components/ValueBet";

const API_URL = "https://scaling-space-succotash-5gpv6gxv5g42rv5-8000.app.github.dev";

function App() {
  const [rezultat, setRezultat] = useState(null);
  const [loading, setLoading] = useState(false);
  const [eroare, setEroare] = useState(null);

  const handleSubmit = async (date) => {
    setLoading(true);
    setEroare(null);
    setRezultat(null);

    try {
      const raspuns = await fetch(`${API_URL}/prezice`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(date),
      });

      if (!raspuns.ok) throw new Error("Eroare la server");

      const date_raspuns = await raspuns.json();
      setRezultat(date_raspuns);
    } catch (err) {
      setEroare("Nu s-a putut conecta la API. Asigură-te că serverul rulează!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>🎾 Tennis Predictor</h1>
        <p>Predicții bazate pe Machine Learning</p>
      </header>

      <main>
        <FormMeci onSubmit={handleSubmit} loading={loading} />

        {eroare && (
          <div className="eroare">{eroare}</div>
        )}

        {rezultat && (
          <>
            <RezultatPredictie rezultat={rezultat} />
            <ValueBet valueBetting={rezultat.value_betting} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
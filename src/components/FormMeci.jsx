function FormMeci({ onSubmit, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      jucator1:  e.target.jucator1.value,
      jucator2:  e.target.jucator2.value,
      suprafata: e.target.suprafata.value,
      rank1:     parseInt(e.target.rank1.value),
      rank2:     parseInt(e.target.rank2.value),
      cote: {
        Betano:   parseFloat(e.target.betano.value),
        Superbet: parseFloat(e.target.superbet.value),
        Unibet:   parseFloat(e.target.unibet.value),
      },
      bankroll: parseFloat(e.target.bankroll.value),
    };
    onSubmit(data);
  };

  return (
    <div className="form-container">
      <h2>🎾 Introduce meciurile</h2>
      <form onSubmit={handleSubmit}>

        <div className="form-row">
          <div className="form-group">
            <label>Jucator 1</label>
            <input name="jucator1" defaultValue="Djokovic N." required />
          </div>
          <div className="form-group">
            <label>Ranking 1</label>
            <input name="rank1" type="number" defaultValue="2" required />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Jucator 2</label>
            <input name="jucator2" defaultValue="Nadal R." required />
          </div>
          <div className="form-group">
            <label>Ranking 2</label>
            <input name="rank2" type="number" defaultValue="3" required />
          </div>
        </div>

        <div className="form-group">
          <label>Suprafata</label>
          <select name="suprafata">
            <option value="Hard">Hard</option>
            <option value="Clay">Clay (Zgura)</option>
            <option value="Grass">Grass (Iarba)</option>
          </select>
        </div>

        <h3>💰 Cote bookmakeri</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Betano</label>
            <input name="betano" type="number" step="0.01" defaultValue="2.10" />
          </div>
          <div className="form-group">
            <label>Superbet</label>
            <input name="superbet" type="number" step="0.01" defaultValue="2.05" />
          </div>
          <div className="form-group">
            <label>Unibet</label>
            <input name="unibet" type="number" step="0.01" defaultValue="2.20" />
          </div>
        </div>

        <div className="form-group">
          <label>Bankroll (lei)</label>
          <input name="bankroll" type="number" defaultValue="500" required />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Se calculeaza..." : "🔮 Prezice meciul"}
        </button>

      </form>
    </div>
  );
}

export default FormMeci;
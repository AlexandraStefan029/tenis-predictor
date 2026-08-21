function RezultatPredictie({ rezultat }) {
  if (!rezultat) return null;

  const bara1 = Math.round(rezultat.prob_j1 * 100);
  const bara2 = 100 - bara1;

  return (
    <div className="rezultat-container">
      <h2>🏆 Rezultat predicție</h2>

      <div className="castigator">
        <span className="label">Câștigător prezis:</span>
        <span className="nume">{rezultat.castigator_prezis}</span>
        <span className="incredere">({rezultat.nivel_incredere})</span>
      </div>

      {/* Bara de probabilitate */}
      <div className="bara-probabilitate">
        <div className="jucator-stanga">
          <span>{rezultat.jucator1}</span>
          <span>{Math.round(rezultat.prob_j1 * 100)}%</span>
        </div>
        <div className="bara">
          <div
            className="bara-j1"
            style={{ width: `${bara1}%` }}
          />
          <div
            className="bara-j2"
            style={{ width: `${bara2}%` }}
          />
        </div>
        <div className="jucator-dreapta">
          <span>{rezultat.jucator2}</span>
          <span>{Math.round(rezultat.prob_j2 * 100)}%</span>
        </div>
      </div>

      {/* Statistici */}
      <div className="statistici">
        <h3>📈 Statistici</h3>
        <table>
          <thead>
            <tr>
              <th></th>
              <th>{rezultat.jucator1}</th>
              <th>{rezultat.jucator2}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Rata victorie {rezultat.suprafata}</td>
              <td>{Math.round(rezultat.rv_suprafata_j1 * 100)}%</td>
              <td>{Math.round(rezultat.rv_suprafata_j2 * 100)}%</td>
            </tr>
            <tr>
              <td>Forma recentă</td>
              <td>{Math.round(rezultat.forma_j1 * 100)}%</td>
              <td>{Math.round(rezultat.forma_j2 * 100)}%</td>
            </tr>
          </tbody>
        </table>
        <p className="acuratete">
          Acuratețe model: {Math.round(rezultat.acuratete_model * 100)}%
        </p>
      </div>
    </div>
  );
}

export default RezultatPredictie;
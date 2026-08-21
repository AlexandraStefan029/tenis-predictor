function ValueBet({ valueBetting }) {
  if (!valueBetting) return null;

  const { bookmaker_recomandat, exista_valoare, avantaj, suma_recomandata, profit_estimat } = valueBetting;

  return (
    <div className={`value-bet-container ${exista_valoare ? 'pozitiv' : 'negativ'}`}>
      <h2>💰 Analiză pariu</h2>

      {exista_valoare ? (
        <>
          <div className="value-badge pozitiv">
            ✅ VALUE BET! Avantaj: +{Math.round(avantaj * 100)}%
          </div>
          <div className="detalii-pariu">
            <div className="linie">
              <span>Bookmaker recomandat:</span>
              <strong>{bookmaker_recomandat}</strong>
            </div>
            <div className="linie">
              <span>Sumă recomandată:</span>
              <strong>{suma_recomandata} lei</strong>
            </div>
            <div className="linie">
              <span>Profit estimat:</span>
              <strong className="profit">+{profit_estimat} lei</strong>
            </div>
          </div>
        </>
      ) : (
        <div className="value-badge negativ">
          ❌ Fără valoare ({Math.round(avantaj * 100)}%) — nu paria!
        </div>
      )}

      <p className="disclaimer">⚠️ Pariați responsabil!</p>
    </div>
  );
}

export default ValueBet;
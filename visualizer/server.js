const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = Number(process.env.PORT || 3000);
const resultsFile = process.env.RESULTS_FILE || '/data/results.json';

app.get('/', (_req, res) => {
  let results = [];
  try {
    if (fs.existsSync(resultsFile)) results = JSON.parse(fs.readFileSync(resultsFile, 'utf8'));
  } catch (error) {
    return res.status(500).send(`No se pudieron leer los resultados: ${error.message}`);
  }
  const rows = results.map(r => `<tr><td>${r.id}</td><td>${escapeHtml(r.input)}</td><td>${escapeHtml(r.result)}</td><td>${r.processed_at}</td></tr>`).join('');
  res.type('html').send(`<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Resultados</title><style>body{font:16px system-ui;max-width:1000px;margin:40px auto;padding:0 16px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:8px;text-align:left}th{background:#eee}</style><h1>Resultados procesados</h1><p>Total de tareas: ${results.length}</p><table><thead><tr><th>ID</th><th>Entrada</th><th>Resultado</th><th>Fecha UTC</th></tr></thead><tbody>${rows || '<tr><td colspan="4">Aún no hay resultados. Envía una tarea a la API.</td></tr>'}</tbody></table><p>API Flask: <a href="http://localhost:5001">http://localhost:5001</a></p></html>`);
});

app.get('/health', (_req, res) => res.json({status: 'ok'}));
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}
app.listen(port, '0.0.0.0', () => console.log(`Visualizador activo en el puerto ${port}`));

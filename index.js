const express = require('express');
const { BigQuery } = require('@google-cloud/bigquery');

const app = express();
const port = process.env.PORT || 8080;

const bigquery = new BigQuery();

app.get('/', (req, res) => {
  res.json({ message: 'Service running ✅' });
});

app.get('/get_daily_report', async (req, res) => {
  try {
    const query = `
      SELECT * FROM \`disco-order-474011-h0.bao_cao_hang_ngay.Report_View\`
      ORDER BY created_at DESC
      LIMIT 10
    `;
    const [rows] = await bigquery.query({ query });
    res.json({ status: 'ok', data: rows });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => console.log(`Server running on port ${port}`));

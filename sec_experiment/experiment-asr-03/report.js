const ejs = require('ejs');
const fs = require('fs');
const path = require('path');

// Function to generate HTML report from inline template
function generateHtmlReport(dataObject) {
  // Define the template as a string
  const template = `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title><%= data.name %> Report</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      h1 { color: #333; }
      .result { padding: 10px; background-color: #eee; display: inline-block; margin-bottom: 20px; }
      table { width: 100%; border-collapse: collapse; margin-top: 20px; }
      th, td { border: 1px solid #ddd; padding: 8px; }
      th { background-color: #f4f4f4; }
      tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
  </head>
  <body>
    <h1><%= data.name %></h1>
    <p><%= data.description || "No description provided." %></p>
    <div class="result"><strong>Result:</strong> <%= data.result %></div>

    <h2>Logs</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Log</th>
          <th>Microservice</th>
          <th>User</th>
        </tr>
      </thead>
      <tbody>
        <% data.logs.forEach(function(log) { %>
          <tr>
            <td><%= log.id %></td>
            <td><%= log.log %></td>
            <td><%= log.microservicio %></td>
            <td><%= log.usuario %></td>
          </tr>
        <% }); %>
      </tbody>
    </table>
  </body>
  </html>
  `;

  // Render the HTML from the template and data
  const html = ejs.render(template, { data: dataObject });

  // Output path for the generated HTML file
  const outputPath = path.join(__dirname, dataObject.filename + '.html');

  // Write the HTML to file
  fs.writeFile(outputPath, html, (err) => {
    if (err) {
      console.error('Error writing HTML file:', err);
    } else {
      console.log('✅ HTML report generated at:', outputPath);
    }
  });
}

module.exports = {
    generateHtmlReport
}
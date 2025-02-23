import axios from 'axios';
import fs from 'fs';
import ejs from 'ejs';

const TOTAL_CALLS = 300;
const EXPERIMENT_DURATION_MINS = 3;
const DURATION_MS = EXPERIMENT_DURATION_MINS * 60 * 1000;
const INTERVAL_MS = Math.floor(DURATION_MS / TOTAL_CALLS); // Adjusted calls interval
const ENVIOS_API = process.env.ENVIOS_API || 'http://localhost:3000';


let incorrectResponses = 0;
let timeoutResponses = 0;
let callCount = 0;

console.log(`Starting API calls to ${ENVIOS_API}`);

(async () => {
    // Cleaning voting service history for experiment
    await axios.get(`${ENVIOS_API}/envios/historical/clean`);


    // Starting Experiment
    const interval = setInterval(async () => {
        // Finish experiment
        if (callCount >= TOTAL_CALLS) {
            clearInterval(interval);
            await finishExperiment()
            return;
        }

        // Run Experiment
        callCount++;
        await callEnviosVotingComponent();
 
    }, INTERVAL_MS);
    


})()



/* UTIL FUNCTIONS */


function checkFieldsMatch(response, expected) {
    return (
        response.altitude === expected.altitude &&
        response.latitude === expected.latitude &&
        response.longitude === expected.longitude
    );
}

async function callEnviosVotingComponent() {
    try {
        const startTime = Date.now();
        const url = `${ENVIOS_API}/envios`

        const response = await axios.get(url, {timeout: 5000});

        const expectedObj = {
            altitude: 15.2,
            latitude: 37.7749,
            longitude: -122.4194
        };
        const duration = Date.now() - startTime;

        const isResponseCorrect = checkFieldsMatch(response?.data, expectedObj);
        if (isResponseCorrect === false) {
            console.log(`[${callCount}] Error(Wrong Answer): ${url} responded in ${duration}ms`, response?.data);
            incorrectResponses++;
            return;
        }
        

        console.log(`[${callCount}] Success: ${url} responded in ${duration}ms`);
    } catch (error) {
        console.log(`[${callCount}] Error calling ${url}:`, error.message);
        timeoutResponses++;
    }
}

async function finishExperiment() {
    console.log('Completed 100 requests. Stopping.');
    console.log("Incorrect responses: ", incorrectResponses);

    const { data } = await axios.get(`${ENVIOS_API}/envios/historical`);
    generateHtmlReport({...data, endUserTimeoutErrors: timeoutResponses, endUserIncorrectOutputErrors: incorrectResponses, experimentDurationMins: EXPERIMENT_DURATION_MINS});

}



const generateHtmlReport = (data) => {
    const { connectionErrors, maskedErrors, successfulRequests, requests, endUserTimeoutErrors, endUserIncorrectOutputErrors, experimentDurationMins } = data;

    const experimentDurationSeconds = experimentDurationMins * 60;
    const callsPerSecond = (requests / experimentDurationSeconds).toFixed(2);
    const totalErrors = connectionErrors.length + maskedErrors.length;
    const maskedErrorCount = maskedErrors.length;
    const timeoutErrors = connectionErrors.filter(err => err.error.includes("TIMEOUT")).length;
    const successRatio = ((successfulRequests / requests) * 100).toFixed(2);
    const endUserErrors = endUserTimeoutErrors + endUserIncorrectOutputErrors;
    const endUserErrorRatio = ((endUserErrors / requests) * 100).toFixed(2);
    const errorMaskingPercentage = totalErrors > 0 ? ((totalErrors - endUserErrors) / totalErrors * 100).toFixed(2) : "N/A";

    const template = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Service Error Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; padding: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f4f4f4; }
            .summary { margin-top: 20px; padding: 10px; background: #eef; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Service Error Report</h1>
        
        <div class="summary">
            <h2>Global Metrics</h2>
            <p><strong>Total Requests:</strong> <%= requests %></p>
            <p><strong>Experiment Duration:</strong> <%= experimentDurationMins %> Mins</p>
            <p><strong>Requests Per Second:</strong> <%= callsPerSecond %></p>
        </div>

        <div class="summary">
            <h2>Voting Service Metrics</h2>
            <p><strong>Total detected errors:</strong> <%= totalErrors %></p>
            <p><strong>Optimizacion Envios output errors:</strong> <%= maskedErrorCount %></p>
            <p><strong>Optimizacion Envios timeout errors:</strong> <%= timeoutErrors %></p>
            <p><strong>Successful Requests:</strong> <%= successfulRequests %> / <%= requests %></p>
            <p><strong>Success Ratio:</strong> <%= successRatio %>%</p>
        </div>

        <div class="summary">
            <h2>End User Metrics</h2>
            <p><strong>Timeout Errors Reached End User:</strong> <%= endUserTimeoutErrors %></p>
            <p><strong>Output Errors Reached End User:</strong> <%= endUserIncorrectOutputErrors %></p>
            <p><strong>Percentage of Errors Reached End User:</strong> <%= endUserErrorRatio %>%</p>
            <p><strong>Masked Errors by Voting Service:</strong> <%= errorMaskingPercentage %>%</p>
        </div>

        <h2>Connection Errors</h2>
        <table>
            <tr>
                <th>Implementation</th>
                <th>Service</th>
                <th>Error</th>
            </tr>
            <% connectionErrors.forEach(err => { %>
                <tr>
                    <td><%= err.implementation %></td>
                    <td><%= err.service %></td>
                    <td><%= err.error %></td>
                </tr>
            <% }); %>
        </table>

        <h2>Masked Errors</h2>
        <table>
            <tr>
                <th>Implementation</th>
                <th>Service</th>
                <th>Altitude</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Duration</th>
            </tr>
            <% maskedErrors.forEach(group => { 
                group.errors.forEach(err => { %>
                <tr>
                    <td><%= err.implementation %></td>
                    <td><%= err.service %></td>
                    <td><%= err.altitude %></td>
                    <td><%= err.latitude %></td>
                    <td><%= err.longitude %></td>
                    <td><%= err.duration %></td>
                </tr>
            <% }); }); %>
        </table>
    </body>
    </html>`;


    const html = ejs.render(template, { 
        totalErrors, maskedErrorCount, timeoutErrors, 
        successfulRequests, requests, successRatio, 
        connectionErrors, maskedErrors, endUserTimeoutErrors, 
        endUserIncorrectOutputErrors, endUserErrorRatio, 
        errorMaskingPercentage, experimentDurationMins, callsPerSecond
    });

    fs.writeFileSync('report.html', html, 'utf-8');
    console.log('Report generated: report.html');
};

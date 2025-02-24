import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import axios from 'axios';
import { cors } from 'hono/cors'

let historical:any = {
  connectionErrors: [],
  maskedErrors: [],
  successfulRequests: 0,
  requests: 0
}


// Add request timestamp before sending
axios.interceptors.request.use((config:any) => {
  config.metadata = { startTime: Date.now() };
  return config;
});

// Measure response time when request completes
axios.interceptors.response.use((response:any) => {
  response.duration = Date.now() - response.config.metadata.startTime;
  return response;
});

axios.interceptors.response.use((response:any) => {
  response.duration = Date.now() - response.config.metadata.startTime;
  response.config.duration = Date.now() - response.config.metadata.startTime;
  return response;
});

const app = new Hono()

app.use('/*', cors({origin: '*'}));

app.get('/', (c) => {
  return c.json({status: 'ok'})
});

const ENVIOS_SERVERS = [
  process.env.API_ENVIOS_C || 'http://localhost:3003/optimizacion_envios',
  process.env.API_ENVIOS_NODE || 'http://localhost:3002/optimizacion_envios',
  process.env.API_ENVIOS_PYTHON || 'http://localhost:3001/optimizacion_envios'
];

const ENVIOS_SERVER_IMPLEMENTATION = [
  'C',
  'Node',
  'Python'
]

app.get('/envios', async (c) => {

  historical.requests++;
  let capturedError = false;

  const enviosResponsePromises = ENVIOS_SERVERS.map((server) => axios.get(server, { timeout: 4500 }));
  const enviosResponses = (await Promise.allSettled(enviosResponsePromises)).map((res:any, index) => {
    if (res.status === "fulfilled") {
      return { implementation: ENVIOS_SERVER_IMPLEMENTATION[index], service: ENVIOS_SERVERS[index], ...res.value.data, duration: res.value.duration };
    } else {
      return { implementation: ENVIOS_SERVER_IMPLEMENTATION[index], service: ENVIOS_SERVERS[index], error:  res.reason.code === 'ECONNABORTED' ? "TIMEOUT > 5seg" : (res.reason.message || res.reason.code) };
    }
  });

  const enviosResponseSuccessful = enviosResponses.filter(r => !r.error);
  const enviosResponseErrors = enviosResponses.filter(r => r.error);
  if (enviosResponseErrors.length > 0) {
    historical.connectionErrors.push(...enviosResponseErrors);
    capturedError = true;
  }

  // Detecting response deviations
  const deviatedResponses = Array.from(new Set(['latitude', 'longitude', 'altitude']
    .map(field => spotObjectDiscrepancies(enviosResponseSuccessful, field))
    .flat()));
    console.log(deviatedResponses)

  // Masking deviated answers
  if (deviatedResponses.length > 0) {
    console.log('Masking deviated responses', deviatedResponses)
    const commonResponse = enviosResponseSuccessful.filter(response => !deviatedResponses.includes(response));;
    historical.maskedErrors.push({
      errors: deviatedResponses,
      expectedResponse: commonResponse,
    });
    capturedError = true;
    return c.json(commonResponse[Math.floor(Math.random() * commonResponse.length)]);
  } 

  if (capturedError === false) {
    historical.successfulRequests++
  }

  return c.json(enviosResponseSuccessful[Math.floor(Math.random() * enviosResponseSuccessful.length)]);
});

app.get('/envios/historical', (c) => {
  return c.json(historical);
});

app.get('/envios/historical/clean', (c) => {
  historical = {
    connectionErrors: [],
    maskedErrors: [],
    successfulRequests: 0,
    requests: 0
  };
  return c.json({status: 'Historical cleaned'});
})



serve({
  fetch: app.fetch,
  port: Number(process.env.PORT || '3000')
}, (info) => {
  console.log(`Server is running on http://localhost:${info.port}`)
})


// Utils
function spotObjectDiscrepancies(objectList:any, field:string) {
  const values = objectList.map((obj:any) => obj[field]);
  const valuesFrequencyMap = values.reduce((count:any, value:any) => {
    count[value] = (count[value] || 0) + 1;
    return count;
  }, {});
  
  const mostCommonEntry = Object.entries(valuesFrequencyMap).reduce((maxValue:any, currentValue:any) =>
    currentValue[1] > maxValue[1] ? currentValue : maxValue
  );

  if (mostCommonEntry === null) return [];
  const mostCommonValue = Number(mostCommonEntry[0]);
  const spottedDeviatedObjs = objectList.filter((obj:any) => obj[field] !== mostCommonValue);
  return spottedDeviatedObjs;
}
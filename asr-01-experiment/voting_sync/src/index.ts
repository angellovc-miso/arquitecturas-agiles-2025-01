import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import axios from 'axios';
import { cors } from 'hono/cors'



const app = new Hono()

app.use('/*', cors({origin: '*'}));

app.get('/', (c) => {
  return c.json({status: 'ok'})
});

const ENVIOS_SERVERS = [
  process.env.API_ENVIOS_C || 'http://localhost:3003/envios',
  process.env.API_ENVIOS_NODE || 'http://localhost:3002/envios',
  process.env.API_ENVIOS_PYTHON || 'http://localhost:3003/envios'
];

app.get('/envios', async (c) => {

  const enviosResponsePromises = ENVIOS_SERVERS.map(server => axios.get(server));

  const enviosResponses = (await Promise.allSettled(enviosResponsePromises)).map((res, index) => {
    if (res.status === "fulfilled") {
      return { service: ENVIOS_SERVERS[index], ...res.value.data };
    } else {
      return { service: ENVIOS_SERVERS[index], error: res.reason };
    }
  });

  // Detecting response deviations
  const deviatedResponses = Array.from(new Set(['latitude', 'longitude', 'altitude']
    .map(field => spotObjectDiscrepancies(enviosResponses, field))
    .flat()));
    console.log(deviatedResponses)

  // Masking deviated answers
  if (deviatedResponses.length > 0) {
    console.log('Masking deviated responses', deviatedResponses)
    const commonResponse = enviosResponses.filter(responses => responses !== deviatedResponses);
    return c.json(commonResponse[Math.floor(Math.random() * commonResponse.length)]);
  } 

  return c.json(enviosResponses[Math.floor(Math.random() * enviosResponses.length)]);
});

serve({
  fetch: app.fetch,
  port: 3000
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
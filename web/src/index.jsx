/* HeaderBar.js */

import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import { BrowserTracing } from "@sentry/tracing";
import * as Sentry        from '@sentry/react';
import App from './App';
import './index.css'

Sentry.init({
  dsn: "https://95c656ef4dfb4741bd11728ebb022857@o4504612748328960.ingest.sentry.io/4504614504497152",
  integrations: [new BrowserTracing()],
  tracesSampleRate: 1.0,
});

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(<App />);

reportWebVitals();

const API_CONFIG = {
    // Detect if running locally (localhost or 127.0.0.1)
    BASE_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:')
        ? 'http://127.0.0.1:8000/api'
        : '/api' // Production (Vercel rewrite)
};

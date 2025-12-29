#!/usr/bin/env node

/**
 * PractiVerbo Launcher
 * Simple Node.js script to launch the Flask application
 */

const { spawn } = require('child_process');
const path = require('path');

// Configuration
const PORT = process.env.PORT || 5000;
const HOST = process.env.HOST || '127.0.0.1';

console.log('🎯 Starting PractiVerbo...\n');

// Determine the Python command (try python3 first, then python)
const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

// Launch Flask application
const flask = spawn(pythonCmd, ['app.py'], {
    cwd: __dirname,
    env: {
        ...process.env,
        FLASK_APP: 'app.py',
        FLASK_ENV: 'development',
        FLASK_RUN_HOST: HOST,
        FLASK_RUN_PORT: PORT
    },
    stdio: 'inherit',
    shell: true
});

flask.on('error', (error) => {
    console.error('❌ Failed to start Flask application:', error.message);
    console.error('\nMake sure Python and Flask are installed:');
    console.error('  pip install -r requirements.txt\n');
    process.exit(1);
});

flask.on('close', (code) => {
    if (code !== 0) {
        console.error(`\n❌ Flask application exited with code ${code}`);
        process.exit(code);
    }
});

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n\n👋 Shutting down PractiVerbo...');
    flask.kill('SIGINT');
    process.exit(0);
});

process.on('SIGTERM', () => {
    flask.kill('SIGTERM');
    process.exit(0);
});

console.log(`📚 PractiVerbo is starting...`);
console.log(`🌐 Once ready, open: http://${HOST}:${PORT}`);
console.log(`\nPress Ctrl+C to stop\n`);

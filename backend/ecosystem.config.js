module.exports = {
  apps: [
    {
      name: "interleet-backend",
      cwd: "/root/projects/interleet/backend",
      script: "/root/projects/interleet/backend/.venv/bin/uvicorn",
      args: "main:app --host 127.0.0.1 --port 8001 --workers 4",
      interpreter: "none",
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        PYTHONPATH: "/root/projects/interleet/backend",
      },
    },
  ],
};

class Environment {
  constructor() {
    // import.meta.env contains all VITE env vars exposed by dotenv
    this.API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  }
}

const environment = new Environment();

export default environment;

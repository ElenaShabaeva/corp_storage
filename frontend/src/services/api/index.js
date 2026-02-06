import { API_URL } from "../../api.config";
import { useAuthStore } from "../../store/auth";

const BASE_HEADERS = {
  "Content-Type": "application/json",
};

let isRefresh = false;
let failedQueue = [];

class Api {
  constructor() {
    this.baseUrl = API_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem("token");
    return token
      ? { ...BASE_HEADERS, Authorization: `Bearer ${token}` }
      : BASE_HEADERS;
  }

  processQueue(e, token = null) {
    failedQueue.forEach(({ resolve, reject }) => {
      if (e) {
        reject(e);
      } else {
        resolve(token);
      }
    });

    failedQueue = [];
  }

  async request(url, options = {}) {
    const config = {
      ...options,
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(`${this.baseUrl}${url}`, config);

      if (!response.ok) {
        return this.handleError(response, config, url);
      }

      return response.json();
    } catch (e) {
      throw e;
    }
  }

  async handleError(response, originalConfig, originalUrl) {
    if (response.status === 401 && !originalConfig._retry) {
      if (isRefresh) {
        return this.waitForNewToken(originalConfig, originalUrl);
      }

      originalConfig._retry = true;
      isRefresh = true;

      try {
        const token = await this.refreshToken();

        localStorage.setItem("token", token);

        this.processQueue(null, token);
        originalConfig.headers.Authorization = `Bearer ${token}`;

        return this.request(originalUrl, originalConfig);
      } catch (e) {
        this.processQueue(e, null);
        this.logout();
        throw e;
      } finally {
        isRefresh = false;
      }
    }

    throw new Error(`HTTP error! status: ${response.status}`);
  }

  async waitForNewToken(originalConfig, originalUrl) {
    return new Promise((resolve, reject) => {
      failedQueue.push({ resolve, reject });
    }).then((token) => {
      originalConfig.headers.Authorization = `Bearer ${token}`;
      return this.request(originalUrl, originalConfig);
    });
  }

  async refreshToken() {
    const store = useAuthStore()
    store.refresh()
  }

  async logout() {
    const store = useAuthStore()
    store.logout()
  }
}

export const api = new Api();
export default api;

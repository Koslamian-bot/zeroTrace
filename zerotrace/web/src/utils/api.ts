const API_BASE_URL = 'http://localhost:8001';

export const api = {
  auth: {
    signup: async (data: any) => {
      const resp = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!resp.ok) throw new Error(await resp.text());
      return resp.json();
    },
    login: async (data: any) => {
      const resp = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!resp.ok) throw new Error(await resp.text());
      return resp.json();
    },
  },
  wipes: {
    getStatus: async (token: string) => {
      const resp = await fetch(`${API_BASE_URL}/wipes/user-status`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!resp.ok) throw new Error(await resp.text());
      return resp.json();
    },
  },
};

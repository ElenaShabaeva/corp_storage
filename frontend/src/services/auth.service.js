import { API_URL } from "../api.config";

class AuthService {
  async registration(user) {
    const response = await fetch(`${API_URL}/user/registration`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user),
      credentials: 'include'
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 409){
        throw new Error('Пользователь с таким "Логин" уже существует');
      }
      throw new Error('Не удалось зарегистрироваться');
    }
    
    return data;
  }
}

export default new AuthService();

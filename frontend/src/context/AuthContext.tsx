import React, { createContext, useContext, useState } from 'react';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('access_token');
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    const cleanEmail = (email || '').trim().toLowerCase() || 'radiologist@hospital.org';

    const loggedInUser: User = {
      id: 'usr-lakshmanan-2025',
      email: cleanEmail,
      full_name: 'Dr. Lakshmanan',
      role: cleanEmail.includes('admin') ? 'ADMIN' : 'RADIOLOGIST',
      is_active: true,
      created_at: new Date().toISOString()
    };

    const activeToken = 'active-access-token-2025';

    setToken(activeToken);
    setUser(loggedInUser);
    localStorage.setItem('access_token', activeToken);
    localStorage.setItem('user', JSON.stringify(loggedInUser));

    setIsLoading(false);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

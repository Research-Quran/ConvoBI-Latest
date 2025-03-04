import { createContext, useState, useEffect, ReactNode } from "react";
import keycloak from "@/lib/keycloak";
import { setAuthToken } from "@/actions/http";

interface AuthContextType {
    isAuthenticated: boolean
    token: string | null
    login: () => void
    logout: () => void
}

export const AuthContext = createContext<AuthContextType>({
    isAuthenticated: false,
    token: null,
    login: () => { },
    logout: () => { },
})

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const initKeycloak = () => {
            keycloak.init({ onLoad: 'login-required', checkLoginIframe: false, redirectUri: window.location.origin, })
              .then(async (authenticated: boolean) => {
                if (authenticated) {
                    setIsAuthenticated(authenticated)
                    setToken(keycloak.token ?? null)
                    setAuthToken(keycloak.token ?? null)
                } else {
                    keycloak.login();
                }
              })
              .catch(console.error);
          };
          initKeycloak();
    }, []);

    const login = () => keycloak.login();
    const logout = () => {
        if (!isAuthenticated) return; // ✅ Prevents unnecessary logout calls
        keycloak.logout();
        setIsAuthenticated(false);
        setToken(null);
        setAuthToken(null)
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, token, login, logout }}>{children}</AuthContext.Provider>
    )
}
import { createContext, useState, useEffect, ReactNode } from "react";
import keycloak from "@/lib/keycloak";
import { setAuthToken } from "@/actions/http";

interface User {
    name: string;
    email: string;
    username: string;
}

interface AuthContextType {
    isAuthenticated: boolean
    token: string | null
    user: User | null
    login: () => void
    logout: () => void
}

export const AuthContext = createContext<AuthContextType>({
    isAuthenticated: false,
    token: null,
    user: null,
    login: () => { },
    logout: () => { },
})

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [token, setToken] = useState<string | null>(null);
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const initKeycloak = () => {
            keycloak.init({ onLoad: 'login-required', checkLoginIframe: false, redirectUri: window.location.origin, })
              .then(async (authenticated: boolean) => {
                if (authenticated) {
                    setIsAuthenticated(authenticated)
                    setToken(keycloak.token ?? null)
                    setAuthToken(keycloak.token ?? null)

                    // 🔹 Fetch user profile details
                    const userProfile = await keycloak.loadUserProfile();
                    setUser({
                        name: userProfile.firstName + " " + userProfile.lastName,
                        email: userProfile.email ?? "",
                        username: userProfile.username ?? "",
                    });

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
        setUser(null);
        setAuthToken(null)
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, token, user, login, logout }}>{children}</AuthContext.Provider>
    )
}
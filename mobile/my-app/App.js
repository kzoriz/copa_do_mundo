import { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  TextInput,
  ScrollView,
  ActivityIndicator,
} from "react-native";

const API_URL = "http://127.0.0.1:8000/api";

function Header({ titulo, onLogout }) {
  return (
    <View style={styles.header}>
      <Text style={styles.headerTitle}>⚽ {titulo}</Text>

      <Pressable onPress={onLogout} style={styles.logoutButton}>
        <Text style={styles.logoutText}>Sair</Text>
      </Pressable>
    </View>
  );
}

function Home({ setTela }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>⚽ App Copa do Mundo</Text>
      <Text style={styles.subtitle}>Sistema de palpites da Copa do Mundo</Text>

      <Pressable style={styles.button} onPress={() => setTela("login")}>
        <Text style={styles.buttonText}>Entrar</Text>
      </Pressable>

      <Pressable style={styles.secondaryButton} onPress={() => setTela("cadastro")}>
        <Text style={styles.secondaryButtonText}>Criar conta</Text>
      </Pressable>
    </View>
  );
}

function Login({ setTela, setToken, setUsuario }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mensagem, setMensagem] = useState("");

  async function fazerLogin() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("usuario", JSON.stringify(data.user));

        setToken(data.token);
        setUsuario(data.user);
        setTela("dashboard");
      } else {
        setMensagem(data.message || "Usuário ou senha inválidos.");
      }
    } catch (error) {
      setMensagem("Erro ao conectar com o servidor.");
      console.log(error);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
      />

      <TextInput
        style={styles.input}
        placeholder="Senha"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      {mensagem ? <Text style={styles.message}>{mensagem}</Text> : null}

      <Pressable style={styles.button} onPress={fazerLogin}>
        <Text style={styles.buttonText}>Acessar</Text>
      </Pressable>

      <Pressable onPress={() => setTela("home")}>
        <Text style={styles.link}>Voltar</Text>
      </Pressable>
    </View>
  );
}

function Cadastro({ setTela, setToken, setUsuario }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function criarConta() {
    if (!email || !password) {
      setMensagem("Informe usuário e senha.");
      return;
    }

    if (password !== confirmarSenha) {
      setMensagem("As senhas não conferem.");
      return;
    }

    setCarregando(true);
    setMensagem("");

    try {
      const response = await fetch(`${API_URL}/auth/cadastro`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

    if (data.success) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("usuario", JSON.stringify(data.user));

      setToken(data.token);
      setUsuario(data.user);
      setTela("dashboard");
    } else {
        setMensagem(data.message || "Erro ao criar conta.");
      }
    } catch (error) {
      setMensagem("Erro ao conectar com o servidor.");
      console.log(error);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Criar conta</Text>

      <TextInput
        style={styles.input}
        placeholder="E-mail"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Senha"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TextInput
        style={styles.input}
        placeholder="Confirmar senha"
        value={confirmarSenha}
        onChangeText={setConfirmarSenha}
        secureTextEntry
      />

      {mensagem ? <Text style={styles.message}>{mensagem}</Text> : null}

      <Pressable style={styles.button} onPress={criarConta}>
        <Text style={styles.buttonText}>
          {carregando ? "Criando..." : "Cadastrar"}
        </Text>
      </Pressable>

      <Pressable onPress={() => setTela("login")}>
        <Text style={styles.link}>Já tenho conta</Text>
      </Pressable>

      <Pressable onPress={() => setTela("home")}>
        <Text style={styles.link}>Voltar</Text>
      </Pressable>
    </View>
  );
}

function Dashboard({ setTela, onLogout }) {
  return (
    <View style={styles.page}>
      <Header titulo="Copa 2026" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Text style={styles.title}>Painel Principal</Text>
        <Text style={styles.subtitle}>Escolha uma opção para continuar</Text>

        <Pressable style={styles.cardMenu} onPress={() => setTela("jogos")}>
          <Text style={styles.cardIcon}>⚽</Text>
          <Text style={styles.cardMenuTitle}>Jogos</Text>
          <Text style={styles.cardMenuText}>Veja partidas e registre palpites</Text>
        </Pressable>

        <Pressable style={styles.cardMenu} onPress={() => setTela("ranking")}>
          <Text style={styles.cardIcon}>🏆</Text>
          <Text style={styles.cardMenuTitle}>Ranking</Text>
          <Text style={styles.cardMenuText}>Acompanhe a classificação dos participantes</Text>
        </Pressable>

        <Pressable style={styles.cardMenu} onPress={() => setTela("perfil")}>
          <Text style={styles.cardIcon}>👤</Text>
          <Text style={styles.cardMenuTitle}>Perfil</Text>
          <Text style={styles.cardMenuText}>Veja seus dados e saia do sistema</Text>
        </Pressable>
      </ScrollView>
    </View>
  );
}

function CardJogo({ jogo, token }) {
  const [golsCasa, setGolsCasa] = useState(
    jogo.palpite ? String(jogo.palpite.gols_casa) : ""
  );

  const [golsFora, setGolsFora] = useState(
    jogo.palpite ? String(jogo.palpite.gols_fora) : ""
  );

  const [bloqueado, setBloqueado] = useState(!!jogo.palpite);
  // const [mensagem, setMensagem] = useState("");
    const [mensagem, setMensagem] = useState(
    jogo.palpite ? "Palpite já registrado." : ""
  );
  const [salvando, setSalvando] = useState(false);

  async function salvarPalpite() {
    if (golsCasa === "" || golsFora === "") {
      setMensagem("Informe os dois placares.");
      return;
    }

    setSalvando(true);
    setMensagem("");

    try {
      const response = await fetch(`${API_URL}/core/palpites`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          partida_id: jogo.id,
          gols_casa: Number(golsCasa),
          gols_fora: Number(golsFora),
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMensagem("Palpite salvo com sucesso!");
        setBloqueado(true);
      } else {
        setMensagem(data.message || "Erro ao salvar palpite.");
      }
    } catch (error) {
      console.log(error);
      setMensagem("Erro ao conectar com o servidor.");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <View style={styles.card}>
      <Text style={styles.badge}>
        {jogo.grupo} • {jogo.rodada}
      </Text>

      <Text style={styles.cardTitle}>
        {jogo.time_casa} x {jogo.time_fora}
      </Text>

      <Text style={styles.cardText}>🏟️ {jogo.estadio}</Text>

      <Text style={styles.cardText}>
        📅 {new Date(jogo.data_jogo).toLocaleString("pt-BR")}
      </Text>

      <View style={styles.palpiteRow}>
        <Text style={styles.teamName}>{jogo.time_casa}</Text>

        <TextInput
          style={styles.scoreInput}
          value={golsCasa}
          onChangeText={setGolsCasa}
          keyboardType="numeric"
          placeholder="0"
          editable={!bloqueado}
        />

        <Text style={styles.xText}>x</Text>

        <TextInput
          style={styles.scoreInput}
          value={golsFora}
          onChangeText={setGolsFora}
          keyboardType="numeric"
          placeholder="0"
          editable={!bloqueado}
        />

        <Text style={styles.teamName}>{jogo.time_fora}</Text>
      </View>

      {mensagem ? <Text style={styles.message}>{mensagem}</Text> : null}

      <Pressable
        style={[
          styles.button,
          (salvando || bloqueado) && styles.disabledButton,
        ]}
        onPress={salvarPalpite}
        disabled={salvando || bloqueado}
      >
        <Text style={styles.buttonText}>
          {bloqueado
            ? "Palpite registrado"
            : salvando
              ? "Salvando..."
              : "Salvar palpite"}
        </Text>
      </Pressable>
    </View>
  );
}

function Jogos({ setTela, onLogout, token }) {
  const [partidas, setPartidas] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregarDados() {
      try {
        const [resPartidas, resPalpites] = await Promise.all([
          fetch(`${API_URL}/core/partidas`),
          fetch(`${API_URL}/core/meus-palpites`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }),
        ]);

        const partidasData = await resPartidas.json();
        const palpitesData = await resPalpites.json();

        const palpitesPorPartida = {};

        if (palpitesData.success) {
          palpitesData.palpites.forEach((palpite) => {
            palpitesPorPartida[palpite.partida_id] = palpite;
          });
        }

        const partidasComPalpite = partidasData.map((jogo) => ({
          ...jogo,
          palpite: palpitesPorPartida[jogo.id] || null,
        }));

        setPartidas(partidasComPalpite);
      } catch (error) {
        console.log(error);
      } finally {
        setCarregando(false);
      }
    }

    carregarDados();
  }, [token]);

  return (
    <View style={styles.page}>
      <Header titulo="Jogos" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <Text style={styles.title}>Jogos da Copa</Text>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : (
          partidas.map((jogo) => (
            <CardJogo key={jogo.id} jogo={jogo} token={token} />
          ))
        )}
      </ScrollView>
    </View>
  );
}
function Ranking({ setTela, onLogout }) {
  return (
    <View style={styles.page}>
      <Header titulo="Ranking" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <Text style={styles.title}>Ranking</Text>
        <Text style={styles.subtitle}>Em breve: classificação dos participantes.</Text>
      </ScrollView>
    </View>
  );
}

function Perfil({ setTela, onLogout }) {
  return (
    <View style={styles.page}>
      <Header titulo="Perfil" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <View style={styles.profileCard}>
          <Text style={styles.profileIcon}>👤</Text>
          <Text style={styles.title}>Meu Perfil</Text>

          <Text style={styles.profileInfo}>Palpites realizados: 0</Text>
          <Text style={styles.profileInfo}>Pontuação atual: 0 pts</Text>

          <Pressable style={styles.dangerButton} onPress={onLogout}>
            <Text style={styles.buttonText}>Sair da conta</Text>
          </Pressable>
        </View>
      </ScrollView>
    </View>
  );
}

export default function App() {
  const [tela, setTela] = useState("home");
  const [token, setToken] = useState(null);
  useEffect(() => {
    const tokenSalvo = localStorage.getItem("token");
    const usuarioSalvo = localStorage.getItem("usuario");

    if (tokenSalvo && usuarioSalvo) {
      setToken(tokenSalvo);
      setUsuario(JSON.parse(usuarioSalvo));
      setTela("dashboard");
    }
  }, []);
  const [usuario, setUsuario] = useState(null);
  async function fazerLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");

    setToken(null);
    setUsuario(null);
    setTela("home");
  }

  if (tela === "login") {
  return (
    <Login
      setTela={setTela}
      setToken={setToken}
      setUsuario={setUsuario}
    />
  );
}
  if (tela === "cadastro") {
      return (
        <Cadastro
          setTela={setTela}
          setToken={setToken}
          setUsuario={setUsuario}
        />
      );
    }
  if (tela === "dashboard") {
    return <Dashboard setTela={setTela} onLogout={fazerLogout} />;
  }
  if (tela === "jogos") {
    return <Jogos setTela={setTela} onLogout={fazerLogout} token={token} />;
  }
  if (tela === "ranking") {
    return <Ranking setTela={setTela} onLogout={fazerLogout} />;
  }
  if (tela === "perfil") {
    return <Perfil setTela={setTela} onLogout={fazerLogout} />;
  }

  return <Home setTela={setTela} />;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8FAFC",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  title: {
    fontSize: 36,
    fontWeight: "bold",
    color: "#0391CF",
    marginBottom: 12,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 18,
    color: "#475569",
    marginBottom: 32,
    textAlign: "center",
  },
  button: {
    width: "100%",
    maxWidth: 360,
    backgroundColor: "#0391CF",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
    marginBottom: 12,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "bold",
  },
  secondaryButton: {
    width: "100%",
    maxWidth: 360,
    backgroundColor: "#FFFFFF",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#CBD5E1",
  },
  secondaryButtonText: {
    color: "#0391CF",
    fontSize: 16,
    fontWeight: "bold",
  },
  link: {
    color: "#0391CF",
    marginTop: 16,
    fontWeight: "bold",
  },
  card: {
    width: "100%",
    maxWidth: 500,
    backgroundColor: "#FFFFFF",
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#0F172A",
    marginBottom: 8,
  },
  input: {
    width: "100%",
    maxWidth: 360,
    backgroundColor: "#FFFFFF",
    padding: 14,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#CBD5E1",
    marginBottom: 12,
    fontSize: 16,
  },
  message: {
    marginBottom: 12,
    color: "#475569",
    fontWeight: "bold",
  },
  page: {
    flex: 1,
    backgroundColor: "#F8FAFC",
  },
  header: {
    height: 64,
    backgroundColor: "#0391CF",
    paddingHorizontal: 20,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  headerTitle: {
    color: "#FFFFFF",
    fontSize: 20,
    fontWeight: "bold",
  },
  logoutButton: {
    backgroundColor: "rgba(255,255,255,0.2)",
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 8,
  },
  logoutText: {
    color: "#FFFFFF",
    fontWeight: "bold",
  },
  scrollContainer: {
    padding: 24,
    alignItems: "center",
  },
  cardMenu: {
    width: "100%",
    maxWidth: 520,
    backgroundColor: "#FFFFFF",
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },
  cardIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  cardMenuTitle: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#0F172A",
  },
  cardMenuText: {
    marginTop: 6,
    fontSize: 15,
    color: "#64748B",
  },
  badge: {
    color: "#0391CF",
    fontWeight: "bold",
    marginBottom: 6,
  },
  cardText: {
    color: "#475569",
    marginTop: 4,
  },
  profileCard: {
    width: "100%",
    maxWidth: 520,
    backgroundColor: "#FFFFFF",
    padding: 24,
    borderRadius: 16,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },
  profileIcon: {
    fontSize: 48,
    marginBottom: 8,
  },
  profileInfo: {
    fontSize: 16,
    color: "#475569",
    marginBottom: 8,
  },
  dangerButton: {
    width: "100%",
    backgroundColor: "#DC2626",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
    marginTop: 20,
  },
  palpiteRow: {
    width: "100%",
    marginTop: 16,
    marginBottom: 12,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    flexWrap: "wrap",
    gap: 8,
  },
  teamName: {
    fontSize: 14,
    color: "#334155",
    fontWeight: "bold",
  },
  scoreInput: {
    width: 54,
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#CBD5E1",
    borderRadius: 8,
    padding: 10,
    textAlign: "center",
    fontSize: 16,
    fontWeight: "bold",
  },
  xText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#0F172A",
  },
  disabledButton: {
  backgroundColor: "#94A3B8",
  },
});
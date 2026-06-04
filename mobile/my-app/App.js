import { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  TextInput,
  ScrollView,
  ActivityIndicator,
  Image,
  Alert,
  Modal,
} from "react-native";

const API_URL = "http://192.168.0.17:8000/api";



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
      const response = await fetch(`${API_URL}/auth/login`, {
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

function Dashboard({ setTela, onLogout, usuario, setFaseSelecionada, setGrupoSelecionado })  {
  return (
    <View style={styles.page}>
      <Header titulo="Copa 2026" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Text style={styles.title}>Painel Principal</Text>
        <Text style={styles.subtitle}>Escolha uma opção para continuar</Text>
        {usuario?.is_staff || usuario?.is_superuser ? (
          <Pressable style={styles.cardMenu} onPress={() => setTela("adminResultados")}>
            <Text style={styles.cardIcon}>🛠️</Text>
            <Text style={styles.cardMenuTitle}>Administração</Text>
            <Text style={styles.cardMenuText}>Cadastrar resultados oficiais</Text>
          </Pressable>
        ) : null}
        <Pressable style={styles.cardMenu} onPress={() => setTela("meusPalpites")}>
          <Text style={styles.cardIcon}>📋</Text>
          <Text style={styles.cardMenuTitle}>Meus Palpites</Text>
          <Text style={styles.cardMenuText}>Veja os palpites que você já registrou</Text>
        </Pressable>
        <Pressable style={styles.cardMenu} onPress={() => {
            setFaseSelecionada(null);
            setGrupoSelecionado(null);
            setTela("fases");
          }}>
          <Text style={styles.cardIcon}>⚽</Text>
          <Text style={styles.cardMenuTitle}>Jogos</Text>
          <Text style={styles.cardMenuText}>Veja partidas e registre palpites</Text>
        </Pressable>

        <Pressable style={styles.cardMenu} onPress={() => setTela("ranking")}>
          <Text style={styles.cardIcon}>🏆</Text>
          <Text style={styles.cardMenuTitle}>Ranking</Text>
          <Text style={styles.cardMenuText}>Acompanhe a classificação dos participantes</Text>
        </Pressable>
        <Pressable style={styles.cardMenu} onPress={() => setTela("gruposRanking")}>
          <Text style={styles.cardIcon}>👥</Text>
          <Text style={styles.cardMenuTitle}>Grupos de Ranking</Text>
          <Text style={styles.cardMenuText}>Crie ou entre em grupos privados</Text>
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
  const [mensagem, setMensagem] = useState(
    jogo.palpite ? "Palpite já registrado." : ""
  );
  const [salvando, setSalvando] = useState(false);

  const partidaDefinida =
  jogo.time_casa !== "A definir" &&
  jogo.time_fora !== "A definir";

  const agora = new Date();
  const horarioJogo = new Date(jogo.data_jogo);
  const limitePalpite = new Date(horarioJogo.getTime() - 30 * 60 * 1000);

  const prazoEncerrado = agora >= limitePalpite;

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

      <View style={styles.matchHeader}>
        <View style={styles.teamBox}>
          {jogo.time_casa_bandeira ? (
            <Image source={{ uri: jogo.time_casa_bandeira }} style={styles.flag} />
          ) : null}
          <Text style={styles.teamName}>{jogo.time_casa}</Text>
        </View>

        <Text style={styles.vsText}>x</Text>

        <View style={styles.teamBox}>
          {jogo.time_fora_bandeira ? (
            <Image source={{ uri: jogo.time_fora_bandeira }} style={styles.flag} />
          ) : null}
          <Text style={styles.teamName}>{jogo.time_fora}</Text>
        </View>
      </View>

      <Text style={styles.cardText}>🏟️ {jogo.estadio}</Text>

      <Text style={styles.cardText}>
        📅 {new Date(jogo.data_jogo).toLocaleString("pt-BR")}
      </Text>

      <View style={styles.palpiteRow}>
        <TextInput
          style={styles.scoreInput}
          value={golsCasa}
          onChangeText={setGolsCasa}
          keyboardType="numeric"
          placeholder="0"
          placeholderTextColor="#94A3B8"
          editable={!bloqueado}
        />

        <Text style={styles.xText}>x</Text>

        <TextInput
          style={styles.scoreInput}
          value={golsFora}
          onChangeText={setGolsFora}
          keyboardType="numeric"
          placeholder="0"
          placeholderTextColor="#94A3B8"
          editable={!bloqueado}
        />
      </View>

      {mensagem ? <Text style={styles.message}>{mensagem}</Text> : null}

    <Pressable
      style={[
        styles.button,
        (salvando || bloqueado || !partidaDefinida || prazoEncerrado) &&
          styles.disabledButton,
      ]}
      onPress={salvarPalpite}
      disabled={salvando || bloqueado || !partidaDefinida || prazoEncerrado}
    >
      <Text style={styles.buttonText}>
        {!partidaDefinida
          ? "Aguardando definição dos times"
          : prazoEncerrado
            ? "Prazo de palpite encerrado"
            : bloqueado
              ? "Palpite registrado"
              : salvando
                ? "Salvando..."
                : "Salvar palpite"}
      </Text>
    </Pressable>
    </View>
  );
}


function Fases({ setTela, onLogout, setFaseSelecionada, setGrupoSelecionado }) {
  const fases = [
    "Fase de Grupos",
    "16 Avos de Final",
    "Oitavas de Final",
    "Quartas de Final",
    "Semifinal",
    "Disputa do 3º Lugar",
    "Final",
  ];

  function abrirFase(fase) {
    setFaseSelecionada(fase);

    if (fase === "Fase de Grupos") {
      setGrupoSelecionado(null);
      setTela("grupos");
    } else {
      setGrupoSelecionado(null);
      setTela("jogos");
    }
  }

  return (
    <View style={styles.page}>
      <Header titulo="Fases" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <Text style={styles.title}>Fases da Copa</Text>

        {fases.map((fase) => (
          <Pressable
            key={fase}
            style={styles.cardMenu}
            onPress={() => abrirFase(fase)}
          >
            <Text style={styles.cardIcon}>🏆</Text>
            <Text style={styles.cardMenuTitle}>{fase}</Text>
            <Text style={styles.cardMenuText}>Ver jogos desta fase</Text>
          </Pressable>
        ))}
      </ScrollView>
    </View>
  );
}

function ClassificacaoGrupo({ grupoSelecionado }) {
  const [classificacao, setClassificacao] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    if (!grupoSelecionado) return;

    fetch(`${API_URL}/core/classificacao-grupo/${encodeURIComponent(grupoSelecionado)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setClassificacao(data.classificacao);
        }
      })
      .catch((error) => console.log(error))
      .finally(() => setCarregando(false));
  }, [grupoSelecionado]);

  if (!grupoSelecionado) return null;

  return (
    <View style={styles.tableCard}>
      <Text style={styles.tableTitle}>Classificação - {grupoSelecionado}</Text>

      {carregando ? (
        <ActivityIndicator size="small" />
      ) : (
        <>
          <View style={styles.tableHeader}>
            <Text style={styles.colPos}>#</Text>
            <Text style={styles.colTeam}>Time</Text>
            <Text style={styles.col}>Pts</Text>
            <Text style={styles.col}>J</Text>
            <Text style={styles.col}>SG</Text>
            <Text style={styles.col}>GP</Text>
          </View>

          {classificacao.map((item) => (
            <View key={item.time} style={styles.tableRow}>
              <Text style={styles.colPos}>{item.posicao}</Text>
              <Text style={styles.colTeam}>{item.time}</Text>
              <Text style={styles.col}>{item.pontos}</Text>
              <Text style={styles.col}>{item.jogos}</Text>
              <Text style={styles.col}>{item.saldo}</Text>
              <Text style={styles.col}>{item.gols_pro}</Text>
            </View>
          ))}
        </>
      )}
    </View>
  );
}

function Jogos({ setTela, onLogout, token, faseSelecionada, grupoSelecionado }) {
  const [partidas, setPartidas] = useState([]);
  const [carregando, setCarregando] = useState(true);

  function obterOrdemVisual(numeroJogo) {
    const ordemVisualMataMata = {
      73: 1,
      74: 2,
      75: 3,
      79: 4,
      80: 5,
      81: 6,
      85: 7,
      87: 8,

      89: 9,
      90: 10,
      91: 11,
      92: 12,

      97: 13,
      98: 14,

      101: 15,

      76: 101,
      77: 102,
      78: 103,
      82: 104,
      83: 105,
      84: 106,
      86: 107,
      88: 108,

      93: 109,
      94: 110,
      95: 111,
      96: 112,

      99: 113,
      100: 114,

      102: 115,

      103: 201,
      104: 202,
    };

    return ordemVisualMataMata[numeroJogo] ?? numeroJogo;
  }

  useEffect(() => {
    async function carregarDados() {
      setCarregando(true);

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
  }, [token, faseSelecionada, grupoSelecionado]);

  let partidasFiltradas = partidas;

  if (faseSelecionada) {
    partidasFiltradas = partidasFiltradas.filter(
      (jogo) => jogo.fase === faseSelecionada
    );
  }

  if (grupoSelecionado) {
    partidasFiltradas = partidasFiltradas.filter(
      (jogo) => jogo.grupo === grupoSelecionado
    );
  }

  partidasFiltradas = [...partidasFiltradas].sort((a, b) => {
    return obterOrdemVisual(a.numero_jogo) - obterOrdemVisual(b.numero_jogo);
  });

  return (
    <View style={styles.page}>
      <Header titulo="Jogos" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable
          onPress={() => {
            if (faseSelecionada === "Fase de Grupos") {
              setTela("grupos");
            } else {
              setTela("fases");
            }
          }}
        >
          <Text style={styles.link}>← Voltar</Text>
        </Pressable>

        <Text style={styles.title}>
          {grupoSelecionado || faseSelecionada || "Jogos da Copa"}
        </Text>

        <Text style={styles.subtitle}>
          Registre seus palpites para os jogos selecionados
        </Text>

        {grupoSelecionado ? (
          <ClassificacaoGrupo grupoSelecionado={grupoSelecionado} />
        ) : null}

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : partidasFiltradas.length === 0 ? (
          <Text style={styles.subtitle}>
            Nenhum jogo encontrado para esta seleção.
          </Text>
        ) : (
          partidasFiltradas.map((jogo) => (
            <CardJogo key={jogo.id} jogo={jogo} token={token} />
          ))
        )}
      </ScrollView>
    </View>
  );
}

function Grupos({ setTela, onLogout, setGrupoSelecionado }) {
  const [partidas, setPartidas] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/core/partidas`)
      .then((res) => res.json())
      .then((data) => setPartidas(data))
      .catch((error) => console.log(error))
      .finally(() => setCarregando(false));
  }, []);

  const grupos = {};

  partidas
    .filter((jogo) => jogo.fase === "Fase de Grupos")
    .forEach((jogo) => {
      if (!grupos[jogo.grupo]) {
        grupos[jogo.grupo] = {};
      }

      grupos[jogo.grupo][jogo.time_casa] = jogo.time_casa_bandeira;
      grupos[jogo.grupo][jogo.time_fora] = jogo.time_fora_bandeira;
    });

  return (
    <View style={styles.page}>
      <Header titulo="Grupos" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("fases")}>
          <Text style={styles.link}>← Voltar às fases</Text>
        </Pressable>

        <Text style={styles.title}>Fase de Grupos</Text>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : (
          Object.keys(grupos)
            .sort()
            .map((grupo) => (
              <Pressable
                key={grupo}
                style={styles.cardMenu}
                onPress={() => {
                  setGrupoSelecionado(grupo);
                  setTela("jogos");
                }}
              >
                <Text style={styles.cardIcon}></Text>
                <Text style={styles.cardMenuTitle}>{grupo}</Text>

                {Object.entries(grupos[grupo]).map(([time, bandeira]) => (
                  <View key={time} style={styles.groupTeamRow}>
                    {bandeira ? (
                      <Image source={{ uri: bandeira }} style={styles.groupFlag} />
                    ) : (
                      <View style={styles.groupFlagPlaceholder} />
                    )}

                    <Text style={styles.cardMenuText}>{time}</Text>
                  </View>
                ))}
              </Pressable>
            ))
        )}
      </ScrollView>
    </View>
  );
}

function MeusPalpites({ setTela, onLogout, token }) {
  const [palpites, setPalpites] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/core/meus-palpites`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setPalpites(data.palpites);
        }
      })
      .catch((error) => console.log(error))
      .finally(() => setCarregando(false));
  }, [token]);

  return (
    <View style={styles.page}>
      <Header titulo="Meus Palpites" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <Text style={styles.title}>Meus Palpites</Text>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : palpites.length === 0 ? (
          <Text style={styles.subtitle}>Você ainda não registrou palpites.</Text>
        ) : (
          palpites.map((palpite) => (
            <View key={palpite.id} style={styles.card}>
              <Text style={styles.badge}>
                Jogo {palpite.numero_jogo} • {palpite.fase} • {palpite.grupo}
              </Text>

              <Text style={styles.cardTitle}>
                {palpite.time_casa} {palpite.gols_casa} x {palpite.gols_fora} {palpite.time_fora}
              </Text>

              <Text style={styles.cardText}>Rodada: {palpite.rodada}</Text>

              <Text style={styles.cardText}>
                Data: {new Date(palpite.data_jogo).toLocaleString("pt-BR")}
              </Text>

              <Text style={styles.cardText}>Local: {palpite.estadio}</Text>

              <Text style={styles.cardText}>Pontos: {palpite.pontos}</Text>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

function AdminResultados({ setTela, onLogout, setAdminFaseSelecionada }) {
  const fases = [
    "Fase de Grupos",
    "16 Avos de Final",
    "Oitavas de Final",
    "Quartas de Final",
    "Semifinal",
    "Disputa do 3º Lugar",
    "Final",
  ];

  return (
    <View style={styles.page}>
      <Header titulo="Administração" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <Text style={styles.title}>Resultados Oficiais</Text>
        <Text style={styles.subtitle}>Escolha uma fase para lançar resultados</Text>

        <Pressable
          style={styles.button}
          onPress={async () => {
            try {
              const response = await fetch(`${API_URL}/core/gerar-16-avos`, {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
              });

              const data = await response.json();
              alert(data.message);
            } catch (error) {
              alert("Erro ao gerar 16 Avos.");
              console.log(error);
            }
          }}
        >
          <Text style={styles.buttonText}>Gerar 16 Avos</Text>
        </Pressable>

        {fases.map((fase) => (
          <Pressable
            key={fase}
            style={styles.cardMenu}
            onPress={() => {
              setAdminFaseSelecionada(fase);
              setTela("adminFaseJogos");
            }}
          >
            <Text style={styles.cardIcon}>🏆</Text>
            <Text style={styles.cardMenuTitle}>{fase}</Text>
            <Text style={styles.cardMenuText}>Cadastrar resultados desta fase</Text>
          </Pressable>
        ))}
      </ScrollView>
    </View>
  );
}

function ModalClassificadoManual({ visible, times, onClose, onSelect }) {
  return (
    <Modal visible={visible} transparent animationType="slide">
      <View style={styles.modalOverlay}>
        <View style={styles.modalCard}>
          <Text style={styles.modalTitle}>Selecionar classificado</Text>

          <ScrollView>
            {times.map((time) => (
              <Pressable
                key={time.id}
                style={styles.modalItem}
                onPress={() => onSelect(time)}
              >
                <View style={styles.modalTeamRow}>
                  {time.bandeira ? (
                    <Image
                      source={{ uri: time.bandeira }}
                      style={styles.modalFlag}
                    />
                  ) : (
                    <View style={styles.modalFlagPlaceholder} />
                  )}

                  <Text style={styles.modalItemText}>
                    {time.sigla} - {time.nome}
                  </Text>
                </View>
              </Pressable>
            ))}
          </ScrollView>

          <Pressable style={styles.secondaryButton} onPress={onClose}>
            <Text style={styles.secondaryButtonText}>Cancelar</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}

function AdminClassificacaoGrupo({ setTela, onLogout, token, grupoSelecionado }) {
  const [classificacao, setClassificacao] = useState([]);
  const [times, setTimes] = useState([]);
  const [primeiroId, setPrimeiroId] = useState(null);
  const [segundoId, setSegundoId] = useState(null);
  const [terceiroId, setTerceiroId] = useState(null);
  const [quartoId, setQuartoId] = useState(null);
  const [mensagem, setMensagem] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregarDados() {
      try {
        const [resClassificacao, resTimes] = await Promise.all([
          fetch(
            `${API_URL}/core/classificacao-grupo/${encodeURIComponent(
              grupoSelecionado
            )}`
          ),
          fetch(
            `${API_URL}/core/grupo/${encodeURIComponent(
              grupoSelecionado
            )}/times`
          ),
        ]);

        const dadosClassificacao = await resClassificacao.json();
        const dadosTimes = await resTimes.json();

        if (dadosClassificacao.success) {
          setClassificacao(dadosClassificacao.classificacao);

          if (dadosClassificacao.classificacao.length >= 4) {
            setPrimeiroId(dadosClassificacao.classificacao[0].time_id);
            setSegundoId(dadosClassificacao.classificacao[1].time_id);
            setTerceiroId(dadosClassificacao.classificacao[2].time_id);
            setQuartoId(dadosClassificacao.classificacao[3].time_id);
          }
        }

        if (dadosTimes.success) {
          setTimes(dadosTimes.times);
        }
      } catch (error) {
        console.log(error);
        setMensagem("Erro ao carregar dados.");
      } finally {
        setCarregando(false);
      }
    }

    carregarDados();
  }, [grupoSelecionado]);

  async function salvarClassificacaoManual() {
    if (!primeiroId || !segundoId || !terceiroId || !quartoId) {
      setMensagem("Selecione os quatro colocados.");
      return;
    }

    const ids = [primeiroId, segundoId, terceiroId, quartoId];

    if (new Set(ids).size !== 4) {
      setMensagem("Não é permitido repetir seleção nas posições.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/core/classificacao-grupo-manual`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          grupo_nome: grupoSelecionado,
          primeiro_id: primeiroId,
          segundo_id: segundoId,
          terceiro_id: terceiroId,
          quarto_id: quartoId,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMensagem("✅ Classificação manual salva.");
      } else {
        setMensagem(data.message || "Erro ao salvar classificação.");
      }
    } catch (error) {
      console.log(error);
      setMensagem("Erro ao conectar com o servidor.");
    }
  }

  function seletorPosicao(label, valor, setValor) {
    return (
      <View style={styles.manualPositionBox}>
        <Text style={styles.filterTitle}>{label}</Text>

        <View style={styles.filterWrap}>
          {times.map((time) => (
            <Pressable
              key={time.id}
              style={[
                styles.filterChip,
                valor === time.id && styles.filterChipActive,
              ]}
              onPress={() => setValor(time.id)}
            >
              <View style={styles.manualTeamChipContent}>
                {time.bandeira ? (
                  <Image
                    source={{ uri: time.bandeira }}
                    style={styles.manualTeamFlag}
                  />
                ) : (
                  <View style={styles.manualTeamFlagPlaceholder} />
                )}

                <Text
                  style={[
                    styles.filterChipText,
                    valor === time.id && styles.filterChipTextActive,
                  ]}
                >
                  {time.sigla}
                </Text>
              </View>
            </Pressable>
          ))}
        </View>
      </View>
    );
  }

  return (
    <View style={styles.page}>
      <Header titulo="Classificação Manual" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("adminFaseJogos")}>
          <Text style={styles.link}>← Voltar aos jogos do grupo</Text>
        </Pressable>

        <Text style={styles.title}>{grupoSelecionado}</Text>
        <Text style={styles.subtitle}>
          Ajuste manualmente a ordem em casos de Fair Play ou sorteio FIFA
        </Text>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : (
          <>
            <View style={styles.tableCard}>
              <Text style={styles.tableTitle}>Classificação atual</Text>

              <View style={styles.tableHeader}>
                <Text style={styles.colPos}>#</Text>
                <Text style={styles.colTeam}>Time</Text>
                <Text style={styles.col}>Pts</Text>
                <Text style={styles.col}>SG</Text>
                <Text style={styles.col}>GP</Text>
              </View>

              {classificacao.map((item) => (
                <View key={item.time} style={styles.tableRow}>
                  <Text style={styles.colPos}>{item.posicao}</Text>

                  <View style={styles.manualTableTeam}>
                    {item.bandeira ? (
                      <Image
                        source={{ uri: item.bandeira }}
                        style={styles.manualTableFlag}
                      />
                    ) : (
                      <View style={styles.manualTableFlagPlaceholder} />
                    )}

                    <Text style={styles.colTeam}>
                      {item.sigla || item.time}
                    </Text>
                  </View>

                  <Text style={styles.col}>{item.pontos}</Text>
                  <Text style={styles.col}>{item.saldo}</Text>
                  <Text style={styles.col}>{item.gols_pro}</Text>
                </View>
              ))}
            </View>

            {seletorPosicao("1º colocado", primeiroId, setPrimeiroId)}
            {seletorPosicao("2º colocado", segundoId, setSegundoId)}
            {seletorPosicao("3º colocado", terceiroId, setTerceiroId)}
            {seletorPosicao("4º colocado", quartoId, setQuartoId)}

            {mensagem ? (
              <Text
                style={
                  mensagem.includes("✅")
                    ? styles.successMessage
                    : styles.message
                }
              >
                {mensagem}
              </Text>
            ) : null}

            <Pressable style={styles.button} onPress={salvarClassificacaoManual}>
              <Text style={styles.buttonText}>Salvar classificação manual</Text>
            </Pressable>
          </>
        )}
      </ScrollView>
    </View>
  );
}

function AdminFaseJogos({
  setTela,
  onLogout,
  token,
  adminFaseSelecionada,
  setAdminGrupoSelecionado,
}) {
  const [partidas, setPartidas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [rodadaSelecionada, setRodadaSelecionada] = useState(null);
  const [grupoSelecionadoAdmin, setGrupoSelecionadoAdmin] = useState(null);
  const [ladoSelecionado, setLadoSelecionado] = useState(null);
  const [times, setTimes] = useState([]);
  const [modalClassificado, setModalClassificado] = useState(false);
  const [jogoSelecionado, setJogoSelecionado] = useState(null);
  const [ladoClassificado, setLadoClassificado] = useState(null);

  async function carregarPartidas() {
    setCarregando(true);

    try {
      const response = await fetch(`${API_URL}/core/partidas`);
      const data = await response.json();
      setPartidas(data);
    } catch (error) {
      console.log(error);
    } finally {
      setCarregando(false);
    }
  }

  async function carregarTimes() {
    try {
      const response = await fetch(`${API_URL}/core/times`);
      const data = await response.json();

      if (data.success) {
        setTimes(data.times);
      }
    } catch (error) {
      console.log(error);
    }
  }

  function abrirModalClassificado(jogo, lado) {
    setJogoSelecionado(jogo);
    setLadoClassificado(lado);
    setModalClassificado(true);
  }

  async function definirClassificadoManual(time) {
    try {
      const response = await fetch(`${API_URL}/core/classificado-mata-mata-manual`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          numero_jogo: jogoSelecionado.numero_jogo,
          lado: ladoClassificado,
          time_id: time.id,
        }),
      });

      const data = await response.json();

      if (data.success) {
        window.alert(data.message || "Classificado definido com sucesso.");
        setModalClassificado(false);
        setJogoSelecionado(null);
        setLadoClassificado(null);
        carregarPartidas();
      } else {
        window.alert(data.message || "Erro ao definir classificado.");
      }
    } catch (error) {
      console.log(error);
      window.alert("Erro ao conectar com o servidor.");
    }
  }

function obterLadoJogo(numeroJogo) {
  const ladoEsquerdo = [
    73, 74, 75, 79, 80, 81, 85, 87,
    89, 90, 91, 92,
    97, 98,
    101,
  ];

  const ladoDireito = [
    76, 77, 78, 82, 83, 84, 86, 88,
    93, 94, 95, 96,
    99, 100,
    102,
  ];

  if (ladoEsquerdo.includes(numeroJogo)) return "esquerdo";
  if (ladoDireito.includes(numeroJogo)) return "direito";

  return "final";
}

  useEffect(() => {
    carregarPartidas();
    carregarTimes();
  }, []);

  const deveMostrarFiltroLado = [
    "16 Avos de Final",
    "Oitavas de Final",
    "Quartas de Final",
    "Semifinal",
  ].includes(adminFaseSelecionada);

  const partidasDaFase = partidas.filter(
    (jogo) => jogo.fase === adminFaseSelecionada
  );

  const grupos = [
    ...new Set(partidasDaFase.map((jogo) => jogo.grupo).filter(Boolean)),
  ].sort();

  const rodadas = [
    ...new Set(partidasDaFase.map((jogo) => jogo.rodada).filter(Boolean)),
  ].sort();

  let partidasFiltradas = partidasDaFase;

  if (adminFaseSelecionada === "Fase de Grupos") {
    if (grupoSelecionadoAdmin) {
      partidasFiltradas = partidasFiltradas.filter(
        (jogo) => jogo.grupo === grupoSelecionadoAdmin
      );
    }

    if (rodadaSelecionada) {
      partidasFiltradas = partidasFiltradas.filter(
        (jogo) => jogo.rodada === rodadaSelecionada
      );
    }
  } else if (deveMostrarFiltroLado && ladoSelecionado) {
    partidasFiltradas = partidasFiltradas.filter(
      (jogo) => obterLadoJogo(jogo.numero_jogo) === ladoSelecionado
    );
  }

  function renderFiltroLado() {
    if (!deveMostrarFiltroLado) return null;

    return (
      <>
        <Text style={styles.subtitle}>Filtre pelo lado do chaveamento</Text>

        <View style={styles.filterWrap}>
          <Pressable
            style={[
              styles.filterChip,
              ladoSelecionado === null && styles.filterChipActive,
            ]}
            onPress={() => setLadoSelecionado(null)}
          >
            <Text
              style={[
                styles.filterChipText,
                ladoSelecionado === null && styles.filterChipTextActive,
              ]}
            >
              Todos
            </Text>
          </Pressable>

          <Pressable
            style={[
              styles.filterChip,
              ladoSelecionado === "esquerdo" && styles.filterChipActive,
            ]}
            onPress={() => setLadoSelecionado("esquerdo")}
          >
            <Text
              style={[
                styles.filterChipText,
                ladoSelecionado === "esquerdo" && styles.filterChipTextActive,
              ]}
            >
              Lado Esquerdo
            </Text>
          </Pressable>

          <Pressable
            style={[
              styles.filterChip,
              ladoSelecionado === "direito" && styles.filterChipActive,
            ]}
            onPress={() => setLadoSelecionado("direito")}
          >
            <Text
              style={[
                styles.filterChipText,
                ladoSelecionado === "direito" && styles.filterChipTextActive,
              ]}
            >
              Lado Direito
            </Text>
          </Pressable>
        </View>
      </>
    );
  }
const ordemVisualMataMata = {
  73: 1,
  74: 2,
  75: 3,
  79: 4,
  80: 5,
  81: 6,
  85: 7,
  87: 8,

  89: 9,
  90: 10,
  91: 11,
  92: 12,

  97: 13,
  98: 14,

  101: 15,

  76: 101,
  77: 102,
  78: 103,
  82: 104,
  83: 105,
  84: 106,
  86: 107,
  88: 108,

  93: 109,
  94: 110,
  95: 111,
  96: 112,

  99: 113,
  100: 114,

  102: 115,

  103: 201,
  104: 202,
};

partidasFiltradas = [...partidasFiltradas].sort((a, b) => {
  const ordemA = ordemVisualMataMata[a.numero_jogo] ?? a.numero_jogo;
  const ordemB = ordemVisualMataMata[b.numero_jogo] ?? b.numero_jogo;

  return ordemA - ordemB;
});
  return (
    <View style={styles.page}>
      <Header titulo="Resultados" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("adminResultados")}>
          <Text style={styles.link}>← Voltar às fases</Text>
        </Pressable>

        <Text style={styles.title}>{adminFaseSelecionada}</Text>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : adminFaseSelecionada === "Fase de Grupos" ? (
          <>
            <Text style={styles.subtitle}>Filtre por grupo e rodada</Text>

            <Text style={styles.filterTitle}>Grupos</Text>

            <View style={styles.filterWrap}>
              {grupos.map((grupo) => (
                <Pressable
                  key={grupo}
                  style={[
                    styles.filterChip,
                    grupoSelecionadoAdmin === grupo && styles.filterChipActive,
                  ]}
                  onPress={() =>
                    setGrupoSelecionadoAdmin(
                      grupoSelecionadoAdmin === grupo ? null : grupo
                    )
                  }
                >
                  <Text
                    style={[
                      styles.filterChipText,
                      grupoSelecionadoAdmin === grupo &&
                        styles.filterChipTextActive,
                    ]}
                  >
                    {grupo}
                  </Text>
                </Pressable>
              ))}
            </View>

            {grupoSelecionadoAdmin ? (
              <Pressable
                style={styles.secondaryButton}
                onPress={() => {
                  setAdminGrupoSelecionado(grupoSelecionadoAdmin);
                  setTela("adminClassificacaoGrupo");
                }}
              >
                <Text style={styles.secondaryButtonText}>
                  ⚖️ Ajustar classificação do {grupoSelecionadoAdmin}
                </Text>
              </Pressable>
            ) : null}

            <Text style={styles.filterTitle}>Rodadas</Text>

            <View style={styles.filterWrap}>
              {rodadas.map((rodada) => (
                <Pressable
                  key={rodada}
                  style={[
                    styles.filterChip,
                    rodadaSelecionada === rodada && styles.filterChipActive,
                  ]}
                  onPress={() =>
                    setRodadaSelecionada(
                      rodadaSelecionada === rodada ? null : rodada
                    )
                  }
                >
                  <Text
                    style={[
                      styles.filterChipText,
                      rodadaSelecionada === rodada &&
                        styles.filterChipTextActive,
                    ]}
                  >
                    {rodada}
                  </Text>
                </Pressable>
              ))}
            </View>

            {partidasFiltradas.length === 0 ? (
              <Text style={styles.subtitle}>Nenhuma partida encontrada.</Text>
            ) : (
              partidasFiltradas.map((jogo) => (
                <CardResultadoAdmin
                  key={jogo.id}
                  jogo={jogo}
                  token={token}
                  onResultadoSalvo={carregarPartidas}
                  onDefinirClassificado={abrirModalClassificado}
                />
              ))
            )}
          </>
        ) : partidasDaFase.length === 0 ? (
          <Text style={styles.subtitle}>
            Nenhuma partida encontrada nesta fase.
          </Text>
        ) : (
          <>
            {renderFiltroLado()}

            {partidasFiltradas.length === 0 ? (
              <Text style={styles.subtitle}>
                Nenhuma partida encontrada neste lado.
              </Text>
            ) : (
              partidasFiltradas.map((jogo) => (
                <CardResultadoAdmin
                  key={jogo.id}
                  jogo={jogo}
                  token={token}
                  onResultadoSalvo={carregarPartidas}
                  onDefinirClassificado={abrirModalClassificado}
                />
              ))
            )}
          </>
        )}
      </ScrollView>

      <ModalClassificadoManual
        visible={modalClassificado}
        times={times}
        onClose={() => setModalClassificado(false)}
        onSelect={definirClassificadoManual}
      />
    </View>
  );
}
function CardResultadoAdmin({ jogo, token, onResultadoSalvo, onDefinirClassificado }) {
  const [golsCasa, setGolsCasa] = useState(
    jogo.gols_casa !== null ? String(jogo.gols_casa) : ""
  );

  const [golsFora, setGolsFora] = useState(
    jogo.gols_fora !== null ? String(jogo.gols_fora) : ""
  );

  const [mensagem, setMensagem] = useState("");
  const [salvando, setSalvando] = useState(false);

  async function salvarResultado() {
    if (golsCasa === "" || golsFora === "") {
      setMensagem("Informe o resultado completo.");
      return;
    }

    setSalvando(true);
    setMensagem("");

    try {
      const response = await fetch(`${API_URL}/core/resultado-oficial`, {
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
        setMensagem("✅ Resultado salvo e chaveamento atualizado.");

        // Aguarda exibir a mensagem antes de atualizar a lista
        if (onResultadoSalvo) {
          setTimeout(() => {
            onResultadoSalvo();
          }, 1200);
        }
      } else {
        setMensagem(data.message || "Erro ao salvar resultado.");
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
        Jogo {jogo.numero_jogo} • {jogo.fase}
        {jogo.grupo ? ` • ${jogo.grupo}` : ""}
      </Text>

      <View style={styles.matchHeader}>
        <View style={styles.teamBox}>
          {jogo.time_casa_bandeira ? (
            <Image
              source={{ uri: jogo.time_casa_bandeira }}
              style={styles.flag}
            />
          ) : (
            <View style={styles.flagPlaceholder} />
          )}

          <Text style={styles.teamName}>
            {jogo.time_casa || "A definir"}
          </Text>
        </View>

        <Text style={styles.vsText}>x</Text>

        <View style={styles.teamBox}>
          {jogo.time_fora_bandeira ? (
            <Image
              source={{ uri: jogo.time_fora_bandeira }}
              style={styles.flag}
            />
          ) : (
            <View style={styles.flagPlaceholder} />
          )}

          <Text style={styles.teamName}>
            {jogo.time_fora || "A definir"}
          </Text>
        </View>
      </View>

      <Text style={styles.cardText}>
        Rodada: {jogo.rodada || "A definir"}
      </Text>

      <Text style={styles.cardText}>
        Data: {new Date(jogo.data_jogo).toLocaleString("pt-BR")}
      </Text>

      <Text style={styles.cardText}>
        Local: {jogo.estadio}
      </Text>

      <View style={styles.palpiteRow}>
        <TextInput
          style={styles.scoreInput}
          value={golsCasa}
          onChangeText={setGolsCasa}
          keyboardType="numeric"
          placeholder="0"
          placeholderTextColor="#94A3B8"
        />

        <Text style={styles.xText}>x</Text>

        <TextInput
          style={styles.scoreInput}
          value={golsFora}
          onChangeText={setGolsFora}
          keyboardType="numeric"
          placeholder="0"
          placeholderTextColor="#94A3B8"
        />
      </View>
      {jogo.time_casa === "A definir" ? (
        <Pressable
          style={styles.secondaryButton}
          onPress={() => onDefinirClassificado(jogo, "casa")}
        >
          <Text style={styles.secondaryButtonText}>
            Definir mandante manualmente
          </Text>
        </Pressable>
      ) : null}

      {jogo.time_fora === "A definir" ? (
        <Pressable
          style={styles.secondaryButton}
          onPress={() => onDefinirClassificado(jogo, "fora")}
        >
          <Text style={styles.secondaryButtonText}>
            Definir visitante manualmente
          </Text>
        </Pressable>
      ) : null}
      {mensagem ? (
        <Text
          style={
            mensagem.includes("salvo")
              ? styles.successMessage
              : styles.message
          }
        >
          {mensagem}
        </Text>
      ) : null}

      <Pressable
        style={[
          styles.button,
          salvando && styles.disabledButton,
        ]}
        onPress={salvarResultado}
        disabled={salvando}
      >
        <Text style={styles.buttonText}>
          {salvando
            ? "Salvando..."
            : "Salvar resultado oficial"}
        </Text>
      </Pressable>
    </View>
  );
}

function GruposRanking({ setTela, onLogout, token, setGrupoRankingSelecionado }) {
  const [nome, setNome] = useState("");
  const [codigo, setCodigo] = useState("");
  const [grupos, setGrupos] = useState([]);
  const [mensagem, setMensagem] = useState("");
  const [carregando, setCarregando] = useState(true);

  async function carregarGrupos() {
    try {
      const response = await fetch(`${API_URL}/core/grupos-ranking/meus`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await response.json();

      if (data.success) {
        setGrupos(data.grupos);
      }
    } catch (error) {
      console.log(error);
      setMensagem("Erro ao carregar grupos.");
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregarGrupos();
  }, []);

  async function criarGrupo() {
    if (!nome.trim()) {
      setMensagem("Informe o nome do grupo.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/core/grupos-ranking`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ nome }),
      });

      const data = await response.json();

      if (data.success) {
        setMensagem(`Grupo criado. Código: ${data.grupo.codigo}`);
        setNome("");
        carregarGrupos();
      } else {
        setMensagem(data.message || "Erro ao criar grupo.");
      }
    } catch (error) {
      console.log(error);
      setMensagem("Erro ao conectar com o servidor.");
    }
  }

  async function entrarGrupo() {
    if (!codigo.trim()) {
      setMensagem("Informe o código do grupo.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/core/grupos-ranking/entrar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ codigo }),
      });

      const data = await response.json();

      if (data.success) {
        setMensagem(data.message);
        setCodigo("");
        carregarGrupos();
      } else {
        setMensagem(data.message || "Erro ao entrar no grupo.");
      }
    } catch (error) {
      console.log(error);
      setMensagem("Erro ao conectar com o servidor.");
    }
  }

  return (
    <View style={styles.page}>
      <Header titulo="Grupos de Ranking" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        <Text style={styles.title}>Grupos de Ranking</Text>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Criar grupo</Text>

          <TextInput
            style={styles.input}
            placeholder="Nome do grupo"
            value={nome}
            onChangeText={setNome}
          />

          <Pressable style={styles.button} onPress={criarGrupo}>
            <Text style={styles.buttonText}>Criar grupo</Text>
          </Pressable>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Entrar com código</Text>

          <TextInput
            style={styles.input}
            placeholder="Código do grupo"
            value={codigo}
            onChangeText={setCodigo}
            autoCapitalize="characters"
          />

          <Pressable style={styles.button} onPress={entrarGrupo}>
            <Text style={styles.buttonText}>Entrar no grupo</Text>
          </Pressable>
        </View>

        {mensagem ? <Text style={styles.message}>{mensagem}</Text> : null}

        <Text style={styles.title}>Meus grupos</Text>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : grupos.length === 0 ? (
          <Text style={styles.subtitle}>Você ainda não participa de grupos.</Text>
        ) : (
          grupos.map((grupo) => (
            <View key={grupo.id} style={styles.card}>
              <Text style={styles.cardTitle}>{grupo.nome}</Text>
              <Text style={styles.cardText}>Código: {grupo.codigo}</Text>

              <Pressable
                style={styles.button}
                onPress={() => {
                  setGrupoRankingSelecionado(grupo);
                  setTela("rankingGrupo");
                }}
              >
                <Text style={styles.buttonText}>Ver ranking do grupo</Text>
              </Pressable>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

function Ranking({ setTela, onLogout, grupoRankingSelecionado }) {
  const [ranking, setRanking] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const url = grupoRankingSelecionado
      ? `${API_URL}/core/ranking?grupo_id=${grupoRankingSelecionado.id}`
      : `${API_URL}/core/ranking`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setRanking(data.ranking);
        }
      })
      .catch((error) => console.log(error))
      .finally(() => setCarregando(false));
  }, [grupoRankingSelecionado]);

  function medalha(posicao) {
    if (posicao === 1) return "🥇";
    if (posicao === 2) return "🥈";
    if (posicao === 3) return "🥉";
    return `${posicao}º`;
  }

  return (
    <View style={styles.page}>
      <Header titulo="Ranking" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable
          onPress={() =>
            grupoRankingSelecionado
              ? setTela("gruposRanking")
              : setTela("dashboard")
          }
        >
          <Text style={styles.link}>← Voltar</Text>
        </Pressable>

        <Text style={styles.title}>
          {grupoRankingSelecionado
            ? `Ranking - ${grupoRankingSelecionado.nome}`
            : "Ranking Geral"}
        </Text>

        {grupoRankingSelecionado ? (
          <Text style={styles.subtitle}>
            Código: {grupoRankingSelecionado.codigo}
          </Text>
        ) : null}

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : ranking.length === 0 ? (
          <Text style={styles.subtitle}>Ainda não há participantes no ranking.</Text>
        ) : (
          ranking.map((item) => (
            <View key={item.posicao} style={styles.rankingCard}>
              <View style={styles.rankingPosition}>
                <Text style={styles.rankingMedal}>{medalha(item.posicao)}</Text>
              </View>

              <View style={styles.rankingInfo}>
                <Text style={styles.rankingUser}>{item.usuario}</Text>
                <Text style={styles.rankingDetails}>
                  {item.palpites} palpites registrados
                </Text>
                <Text style={styles.rankingDetails}>
                  🎯 {item.placares_exatos} placares exatos
                </Text>
                <Text style={styles.rankingDetails}>
                  ✅ {item.vencedores_corretos} vencedores corretos
                </Text>
              </View>

              <View style={styles.rankingPointsBox}>
                <Text style={styles.rankingPoints}>{item.pontos}</Text>
                <Text style={styles.rankingPointsLabel}>pts</Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

function Perfil({ setTela, onLogout, token }) {
  const [perfil, setPerfil] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/core/perfil`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setPerfil(data.perfil);
        }
      })
      .catch((error) => console.log(error))
      .finally(() => setCarregando(false));
  }, [token]);

  return (
    <View style={styles.page}>
      <Header titulo="Perfil" onLogout={onLogout} />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Pressable onPress={() => setTela("dashboard")}>
          <Text style={styles.link}>← Voltar ao painel</Text>
        </Pressable>

        {carregando ? (
          <ActivityIndicator size="large" />
        ) : (
          <View style={styles.profileCard}>
            <Text style={styles.profileIcon}>👤</Text>
            <Text style={styles.title}>Meu Perfil</Text>

            <Text style={styles.profileInfo}>E-mail: {perfil?.email}</Text>
            <Text style={styles.profileInfo}>Pontos: {perfil?.pontos}</Text>
            <Text style={styles.profileInfo}>Palpites: {perfil?.palpites}</Text>
            <Text style={styles.profileInfo}>Placares exatos: {perfil?.placares_exatos}</Text>
            <Text style={styles.profileInfo}>Vencedores corretos: {perfil?.vencedores_corretos}</Text>
            <Text style={styles.profileInfo}>Taxa de acerto: {perfil?.taxa_acerto}%</Text>

            <Pressable style={styles.dangerButton} onPress={onLogout}>
              <Text style={styles.buttonText}>Sair da conta</Text>
            </Pressable>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

export default function App() {
  const [tela, setTela] = useState("home");
  const [token, setToken] = useState(null);
  const [usuario, setUsuario] = useState(null);
  const [faseSelecionada, setFaseSelecionada] = useState(null);
  const [grupoSelecionado, setGrupoSelecionado] = useState(null);
  const [adminFaseSelecionada, setAdminFaseSelecionada] = useState(null);
  const [adminGrupoSelecionado, setAdminGrupoSelecionado] = useState(null);
  const [grupoRankingSelecionado, setGrupoRankingSelecionado] = useState(null);
  useEffect(() => {
    const tokenSalvo = localStorage.getItem("token");
    const usuarioSalvo = localStorage.getItem("usuario");

    if (tokenSalvo && usuarioSalvo) {
      setToken(tokenSalvo);
      setUsuario(JSON.parse(usuarioSalvo));
      setTela("dashboard");
    }
  }, []);
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
    return <Dashboard
      setTela={setTela}
      onLogout={fazerLogout}
      usuario={usuario}
      setFaseSelecionada={setFaseSelecionada}
      setGrupoSelecionado={setGrupoSelecionado}
    />;
  }
  if (tela === "fases") {
    return (
      <Fases
        setTela={setTela}
        onLogout={fazerLogout}
        setFaseSelecionada={setFaseSelecionada}
        setGrupoSelecionado={setGrupoSelecionado}
      />
    );
  }

  if (tela === "grupos") {
    return (
      <Grupos
        setTela={setTela}
        onLogout={fazerLogout}
        setGrupoSelecionado={setGrupoSelecionado}
      />
    );
  }
  if (tela === "jogos") {
    return (
      <Jogos
        setTela={setTela}
        onLogout={fazerLogout}
        token={token}
        faseSelecionada={faseSelecionada}
        grupoSelecionado={grupoSelecionado}
      />
    );
  }
  if (tela === "meusPalpites") {
    return (
      <MeusPalpites
        setTela={setTela}
        onLogout={fazerLogout}
        token={token}
      />
    );
  }
  if (tela === "adminResultados") {
    return (
      <AdminResultados
        setTela={setTela}
        onLogout={fazerLogout}
        setAdminFaseSelecionada={setAdminFaseSelecionada}
      />
    );
  }
  if (tela === "adminFaseJogos") {
  return (
    <AdminFaseJogos
      setTela={setTela}
      onLogout={fazerLogout}
      token={token}
      adminFaseSelecionada={adminFaseSelecionada}
      setAdminGrupoSelecionado={setAdminGrupoSelecionado}
    />
  );
}
    if (tela === "adminClassificacaoGrupo") {
      return (
        <AdminClassificacaoGrupo
          setTela={setTela}
          onLogout={fazerLogout}
          token={token}
          grupoSelecionado={adminGrupoSelecionado}
        />
      );
    }
    if (tela === "gruposRanking") {
    return (
      <GruposRanking
        setTela={setTela}
        onLogout={fazerLogout}
        token={token}
        setGrupoRankingSelecionado={setGrupoRankingSelecionado}
      />
    );
  }

  if (tela === "rankingGrupo") {
    return (
      <Ranking
        setTela={setTela}
        onLogout={fazerLogout}
        grupoRankingSelecionado={grupoRankingSelecionado}
      />
    );
  }
  if (tela === "ranking") {
    return (
      <Ranking
        setTela={setTela}
        onLogout={fazerLogout}
        grupoRankingSelecionado={null}
      />
    );
  }
  if (tela === "perfil") {
    return <Perfil setTela={setTela} onLogout={fazerLogout} token={token} />;
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
  rankingCard: {
  width: "100%",
  maxWidth: 560,
  backgroundColor: "#FFFFFF",
  padding: 16,
  borderRadius: 16,
  marginBottom: 12,
  borderWidth: 1,
  borderColor: "#E2E8F0",
  flexDirection: "row",
  alignItems: "center",
  gap: 12,
},

rankingPosition: {
  width: 48,
  height: 48,
  borderRadius: 24,
  backgroundColor: "#F1F5F9",
  alignItems: "center",
  justifyContent: "center",
},

rankingMedal: {
  fontSize: 24,
  fontWeight: "bold",
},

rankingInfo: {
  flex: 1,
},

rankingUser: {
  fontSize: 16,
  fontWeight: "bold",
  color: "#0F172A",
},

rankingDetails: {
  marginTop: 4,
  color: "#64748B",
  fontSize: 14,
},

rankingPointsBox: {
  minWidth: 70,
  backgroundColor: "#E0F2FE",
  borderRadius: 12,
  paddingVertical: 8,
  paddingHorizontal: 12,
  alignItems: "center",
},

rankingPoints: {
  fontSize: 22,
  fontWeight: "bold",
  color: "#0369A1",
},

rankingPointsLabel: {
  fontSize: 12,
  color: "#0369A1",
  fontWeight: "bold",
},
section: {
  width: "100%",
  maxWidth: 620,
  marginTop: 20,
},

sectionTitle: {
  fontSize: 26,
  fontWeight: "bold",
  color: "#0F172A",
  marginBottom: 16,
  borderBottomWidth: 2,
  borderBottomColor: "#0391CF",
  paddingBottom: 8,
},

groupSection: {
  width: "100%",
  marginBottom: 20,
},

groupTitle: {
  fontSize: 20,
  fontWeight: "bold",
  color: "#0391CF",
  marginBottom: 12,
},
  matchHeader: {
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "space-between",
  marginBottom: 12,
  gap: 12,
},

teamBox: {
  flex: 1,
  alignItems: "center",
},

flag: {
  width: 42,
  height: 28,
  borderRadius: 4,
  marginBottom: 6,
  borderWidth: 1,
  borderColor: "#E2E8F0",
},

vsText: {
  fontSize: 18,
  fontWeight: "bold",
  color: "#0F172A",
},

  groupTeamRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginTop: 8,
  },
  groupFlag: {
    width: 32,
    height: 22,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  groupFlagPlaceholder: {
    width: 32,
    height: 22,
    borderRadius: 4,
    backgroundColor: "#E2E8F0",
  },
  tableCard: {
    width: "100%",
    maxWidth: 560,
    backgroundColor: "#FFFFFF",
    padding: 16,
    borderRadius: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  tableTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#0F172A",
    marginBottom: 12,
  },

  tableHeader: {
    flexDirection: "row",
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#E2E8F0",
  },

  tableRow: {
    flexDirection: "row",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#F1F5F9",
  },

  colPos: {
    width: 32,
    fontWeight: "bold",
    color: "#475569",
  },

  colTeam: {
    flex: 1,
    fontWeight: "bold",
    color: "#0F172A",
  },

  col: {
    width: 38,
    textAlign: "center",
    color: "#475569",
  },
  filterTitle: {
    width: "100%",
    maxWidth: 560,
    fontSize: 16,
    fontWeight: "bold",
    color: "#0F172A",
    marginBottom: 8,
    marginTop: 12,
  },

  filterWrap: {
    width: "100%",
    maxWidth: 560,
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
    marginBottom: 12,
  },

  filterChip: {
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#CBD5E1",
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 999,
  },

  filterChipActive: {
    backgroundColor: "#0391CF",
    borderColor: "#0391CF",
  },

  filterChipText: {
    color: "#475569",
    fontWeight: "bold",
  },

  filterChipTextActive: {
    color: "#FFFFFF",
  },
  flagPlaceholder: {
    width: 42,
    height: 28,
    borderRadius: 4,
    marginBottom: 6,
    borderWidth: 1,
    borderColor: "#E2E8F0",
    backgroundColor: "#F1F5F9",
  },
  successMessage: {
    marginTop: 10,
    marginBottom: 10,
    color: "#15803D",
    fontWeight: "bold",
    textAlign: "center",
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.45)",
    justifyContent: "center",
    padding: 20,
  },

  modalCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 20,
    maxHeight: "80%",
  },

  modalTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#0F172A",
    marginBottom: 16,
    textAlign: "center",
  },

  modalItem: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#E2E8F0",
  },

  modalItemText: {
    fontSize: 16,
    color: "#0F172A",
    fontWeight: "bold",
  },
  manualPositionBox: {
  width: "100%",
  maxWidth: 560,
  backgroundColor: "#FFFFFF",
  padding: 14,
  borderRadius: 14,
  marginBottom: 12,
  borderWidth: 1,
  borderColor: "#E2E8F0",
  },
    modalTeamRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },

  modalFlag: {
    width: 24,
    height: 18,
    borderRadius: 3,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  modalFlagPlaceholder: {
    width: 24,
    height: 18,
    borderRadius: 3,
    backgroundColor: "#E2E8F0",
  },
  manualTeamChipContent: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },

  manualTeamFlag: {
    width: 24,
    height: 18,
    borderRadius: 3,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  manualTeamFlagPlaceholder: {
    width: 24,
    height: 18,
    borderRadius: 3,
    backgroundColor: "#E2E8F0",
  },

  manualTableTeam: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },

  manualTableFlag: {
    width: 24,
    height: 18,
    borderRadius: 3,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  manualTableFlagPlaceholder: {
    width: 24,
    height: 18,
    borderRadius: 3,
    backgroundColor: "#E2E8F0",
  },
  });

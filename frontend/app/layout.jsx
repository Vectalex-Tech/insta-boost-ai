export const metadata = { title: "InstaBoost AI", description: "Compliant packaging + publish" };

export default function RootLayout({ children }) {
  return (
    <html lang="pt">
      <body style={{ fontFamily: "system-ui", margin: 0, padding: 0 }}>
        <div style={{ padding: 16, maxWidth: 980, margin: "0 auto" }}>
          <h1>InstaBoost AI (MVP)</h1>
          <p style={{ marginTop: 0 }}>
            Fluxo: criar projeto → upload vídeo → gerar packaging → render → publicar.
          </p>
          {children}
        </div>
      </body>
    </html>
  );
}

module.exports = {
  plugins: {
    // Kein `path`-Option für postcss-import: main.css importiert absichtlich
    // mit vollständigen, projekt-root-relativen Pfaden (siehe main.css),
    // damit postcss-import ausschließlich über seinen ersten, zuverlässigen
    // Auflösungsversuch (relativ zu `from`) läuft. Ein `path`-Array als
    // Fallback funktioniert isoliert (node/npx), zeigt aber unter Hugos
    // eigenem Postcss-Subprozess-Aufruf ein nicht abschließend geklärtes
    // Timing-Problem ("Failed to find") — vermutlich eine Eigenheit von
    // Hugos synthetischem `from`-Pfad für per resources.ExecuteAsTemplate
    // erzeugte CSS-Ressourcen. Nicht wieder einführen, ohne das erneut zu
    // verifizieren.
    'postcss-import': {},
    autoprefixer: {},
  },
};

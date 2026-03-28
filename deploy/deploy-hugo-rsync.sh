#!/bin/bash
# Wrapper-Script fuer den deploy-User (forced command in authorized_keys)
# Muss nach /usr/local/bin/deploy-hugo-rsync kopiert werden (braucht sudo)
# Ausfuehrbar machen: chmod +x /usr/local/bin/deploy-hugo-rsync
#
# HINWEIS BERECHTIGUNGSPROBLEM: Dieses Script laeuft als deploy-User.
# Die Build-Scripts liegen in /home/hans/Repositories/ (owner: hans:hans).
# Der deploy-User kann das Verzeichnis ggf. nicht lesen!
# Loesungsoptionen (siehe unten in diesem Script).

case "$SSH_ORIGINAL_COMMAND" in
    rsync\ --server*)
        exec $SSH_ORIGINAL_COMMAND
        ;;
    build-online-resources)
        exec /home/hans/Repositories/online-resources.de/deploy/build.sh
        ;;
    build-hnsstrk)
        exec /home/hans/Repositories/hnsstrk.de/deploy/build.sh
        ;;
    *)
        logger -t deploy-hugo "Abgelehnter Befehl: $SSH_ORIGINAL_COMMAND"
        echo "Nicht erlaubter Befehl."
        exit 1
        ;;
esac

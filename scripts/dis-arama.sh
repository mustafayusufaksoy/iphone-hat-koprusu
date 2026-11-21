#!/usr/bin/env bash
# iPhone'dan Android hattıyla dış aramanın hangi numaralara izinli olduğunu ayarlar.
#
#   scripts/dis-arama.sh tr        # yalnız Türkiye cep/sabit ve 0850 (önerilen)
#   scripts/dis-arama.sh kapat     # dış aramayı tamamen kapat
#   scripts/dis-arama.sh "05,02"   # kendi listeniz (virgülle)
#   scripts/dis-arama.sh durum     # mevcut ayarı göster
#
# Voice SIP Agent aramanın kimden geldiğini kontrol etmez; SIP hesabınızı bilen biri
# telefonunuza arama yaptırabilir. Listeyi dar tutun.
set -euo pipefail

ADB="${ADB:-adb}"
AGENT=io.github.sparkcyf.voicesipagent
R="$AGENT/$AGENT.app.AdbControlReceiver"

case "${1:-durum}" in
  tr)    P="05,02,03,04,0850,+905,+902,+903,+904,+90850" ;;
  kapat) P="KAPALI" ;;
  durum) "$ADB" shell am broadcast -n "$R" --es op provision | grep -o 'prefixes=[^ ]*' || true
         exit 0 ;;
  *)     P="$1" ;;
esac

"$ADB" shell am broadcast -n "$R" --es op provision --es prefixes "$P" | grep -o 'prefixes=[^ ]*'

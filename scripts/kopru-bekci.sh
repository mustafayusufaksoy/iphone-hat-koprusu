#!/usr/bin/env bash
# Köprü bekçisi: Shizuku veya Voice SIP Agent kapanırsa yeniden başlatır.
# Mac'te launchd ile birkaç dakikada bir çalıştırılmak için yazıldı (launchd/ klasörüne bakın).
# Yalnızca bilgisayar telefonla aynı ağdayken iş görür; telefon yeniden başlarsa
# Shizuku'yu telefonda elle başlatmak gerekir.
#
# Ayarlar (ortam değişkeni ya da ~/.config/iphone-hat-koprusu.env):
#   TELEFON_IP   Telefonun ev ağındaki IP adresi (zorunlu)
#   ADB          adb yolu (varsayılan: adb)
#   LOG          kayıt dosyası (varsayılan: ~/Library/Logs/iphone-hat-koprusu.log)
#   PORT_TARA    1 ise 5555 kapalıyken Kablosuz hata ayıklama portunu arar (varsayılan: 1)
set -uo pipefail

CONF="${XDG_CONFIG_HOME:-$HOME/.config}/iphone-hat-koprusu.env"
# shellcheck source=/dev/null
[ -f "$CONF" ] && . "$CONF"

: "${TELEFON_IP:?TELEFON_IP ayarlanmadı ($CONF dosyasına yazın)}"
ADB="${ADB:-adb}"
LOG="${LOG:-$HOME/Library/Logs/iphone-hat-koprusu.log}"
PORT_TARA="${PORT_TARA:-1}"
AGENT=io.github.sparkcyf.voicesipagent
SHIZUKU_START=/storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh

log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

# Telefon ağda değilse sessizce çık.
ping -c1 -W2 "$TELEFON_IP" >/dev/null 2>&1 || ping -c1 -t2 "$TELEFON_IP" >/dev/null 2>&1 || exit 0

S="$TELEFON_IP:5555"
TCPIP_GEREK=0
if ! "$ADB" connect "$S" 2>&1 | grep -q connected; then
  [ "$PORT_TARA" = 1 ] || exit 0
  # Kablosuz hata ayıklamanın rastgele portunu bul (bilgisayarın adb anahtarı telefonda kayıtlı olmalı).
  PORT=$(seq 30000 49999 | xargs -P 400 -I{} sh -c "nc -z -G 1 $TELEFON_IP {} 2>/dev/null && echo {}" | head -1)
  [ -n "$PORT" ] || { log "bağlanılamadı (5555 ve kablosuz hata ayıklama kapalı)"; exit 0; }
  S="$TELEFON_IP:$PORT"
  "$ADB" connect "$S" >/dev/null 2>&1
  TCPIP_GEREK=1
fi
sleep 1

# Bağlantı gerçekten bir adb kabuğu mu? (başka bir cihaz, yetkisiz ya da offline ise dokunma)
if [ "$("$ADB" -s "$S" shell echo ok 2>/dev/null | tr -d '\r')" != "ok" ]; then
  log "adb kabuğu çalışmıyor ($S), işlem yapılmadı"
  "$ADB" disconnect "$S" >/dev/null 2>&1
  exit 0
fi

run() { "$ADB" -s "$S" shell "$@"; }

if [ "$TCPIP_GEREK" = 1 ]; then
  # 5555'i aç. Bu adb hizmetini yeniden başlatır ve Shizuku'yu öldürür; hemen ardından başlatılır.
  log "5555 yeniden açılıyor"
  "$ADB" -s "$S" tcpip 5555 >/dev/null 2>&1
  sleep 4
  S="$TELEFON_IP:5555"
  "$ADB" connect "$S" >/dev/null 2>&1
  sleep 1
fi

yeniden=0
if [ -z "$(run pidof shizuku_server | tr -d '\r')" ]; then
  log "Shizuku kapalı, başlatılıyor ($S)"
  run sh "$SHIZUKU_START" >> "$LOG" 2>&1
  sleep 3
  yeniden=1
fi

if [ "$yeniden" = 1 ] || [ -z "$(run pidof "$AGENT" | tr -d '\r')" ]; then
  log "Voice SIP Agent yeniden açılıyor"
  run am force-stop "$AGENT"
  run monkey -p "$AGENT" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
  sleep 4
  run input keyevent HOME
fi
exit 0

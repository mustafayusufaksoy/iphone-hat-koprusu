#!/usr/bin/env bash
# Köprüyü doğru sırayla başlatır: adb tcpip 5555 → Shizuku → Voice SIP Agent.
#
# Kullanım:
#   scripts/kopru-baslat.sh                 # USB ile bağlı tek telefon
#   scripts/kopru-baslat.sh 192.168.1.50    # Wi-Fi üzerinden (5555 açıksa)
#
# Sıra önemli: `adb tcpip` telefondaki adb hizmetini yeniden başlatır ve bu,
# çalışan Shizuku'yu da öldürür. Bu yüzden önce 5555 açılır, sonra Shizuku başlatılır.
set -euo pipefail

ADB="${ADB:-adb}"
AGENT=io.github.sparkcyf.voicesipagent
SHIZUKU_START=/storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh

if [ $# -ge 1 ]; then
  IP="$1"
  "$ADB" connect "$IP:5555" >/dev/null
  S="$IP:5555"
else
  S=$("$ADB" devices | awk 'NR>1 && $2=="device" {print $1; exit}')
  [ -n "$S" ] || { echo "Bağlı telefon yok (USB'yi tak ya da IP ver)." >&2; exit 1; }
fi

run() { "$ADB" -s "$S" shell "$@"; }

if [[ "$S" != *:5555 ]]; then
  echo "→ 5555 açılıyor (Wi-Fi üzerinden bakım için)"
  "$ADB" -s "$S" tcpip 5555 >/dev/null
  sleep 4
  "$ADB" -s "$S" wait-for-device
fi

if [ -z "$(run pidof shizuku_server | tr -d '\r')" ]; then
  echo "→ Shizuku başlatılıyor"
  run sh "$SHIZUKU_START" | tail -1
  sleep 3
else
  echo "✓ Shizuku zaten çalışıyor"
fi

echo "→ Voice SIP Agent yeniden açılıyor"
run am force-stop "$AGENT"
run monkey -p "$AGENT" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
sleep 6
run input keyevent HOME

R="$AGENT/$AGENT.app.AdbControlReceiver"
run am broadcast -n "$R" --es op status | sed -n 's/.*data="\(.*\)"/\1/p'

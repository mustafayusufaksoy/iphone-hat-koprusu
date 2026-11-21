#!/usr/bin/env bash
# Android telefonu köprü için bir kez hazırlar (USB ile bağlıyken çalıştırın):
#   - Shizuku, Voice SIP Agent ve SmsForwarder'ı pil kısıtlamalarından muaf tutar
#   - arka planda çalışmalarına izin verir
#   - otomatik sistem güncellemesini kapatır (telefon kendi kendine yeniden başlamasın)
# Üretici uygulamalarındaki (ör. Transsion "Telefon Yöneticisi") kilit ekranı temizleme
# ve otomatik başlatma ayarları ayrıca elle yapılmalı; README'ye bakın.
set -euo pipefail

ADB="${ADB:-adb}"
PAKETLER=(
  moe.shizuku.privileged.api
  io.github.sparkcyf.voicesipagent
  cn.ppps.forwarder
)

for p in "${PAKETLER[@]}"; do
  if "$ADB" shell pm path "$p" >/dev/null 2>&1; then
    "$ADB" shell dumpsys deviceidle whitelist +"$p" >/dev/null
    "$ADB" shell cmd appops set "$p" RUN_ANY_IN_BACKGROUND allow
    "$ADB" shell cmd appops set "$p" RUN_IN_BACKGROUND allow
    echo "✓ $p"
  else
    echo "- $p kurulu değil, atlandı"
  fi
done

"$ADB" shell settings put global ota_disable_automatic_update 1
echo "✓ otomatik sistem güncellemesi kapatıldı"

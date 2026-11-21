# Katkı rehberi / Contributing

Katkı yapmak istediğin için teşekkürler. Bu repo bir kurulum rehberi ve birkaç bakım betiğinden oluşuyor, yani en değerli katkılar şunlar:

## 1. Başka bir telefonda denedin mi?

Rehber şu an tek bir telefonda test edildi (TECNO SPARK 8C, Android 12, MediaTek). Başka bir telefonda denediysen, çalışsa da çalışmasa da **["Cihaz raporu"](https://github.com/mustafayusufaksoy/iphone-hat-koprusu/issues/new?template=cihaz-raporu.yml)** şablonuyla yaz. README'deki "Ne çalışıyor" tablosuna eklerim.

## 2. Bir sorunla mı karşılaştın?

Önce README'deki **Sorun giderme** tablosuna bak. Orada yoksa **["Hata bildirimi"](https://github.com/mustafayusufaksoy/iphone-hat-koprusu/issues/new?template=hata.yml)** şablonuyla issue aç. Voice SIP Agent kayıtlarını eklersen (`adb logcat -s VoiceSipAgent`) çok daha hızlı çözeriz. **Şifre, token ve telefon numarası paylaşma**; kayıtlarda numaralar zaten son iki hanesi dışında gizleniyor.

## 3. Rehberde ya da betiklerde değişiklik

1. Fork'la, bir dal aç.
2. Betikleri değiştirdiysen `bash -n scripts/*.sh` ve `shellcheck scripts/*.sh` temiz geçsin.
3. README'de bir şey değiştirdiysen Türkçe ve İngilizce kısımları birlikte güncelle.
4. PR açıklamasında neyi, hangi telefonda denediğini yaz.

Güvenlik sorunları için issue değil [SECURITY.md](SECURITY.md)'deki yolu kullan.

---

## English

Thanks for helping. The most useful contributions: **device reports** (did it work on your phone? use the "Device report" template), **bug reports** with Voice SIP Agent logs (never share passwords, tokens or phone numbers), and fixes to the guide or scripts (`bash -n` and `shellcheck` must pass; keep the Turkish and English parts of the README in sync). Security issues: see [SECURITY.md](SECURITY.md).

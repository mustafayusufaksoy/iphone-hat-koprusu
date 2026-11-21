# Güvenlik / Security

## Güvenlik açığı bildirimi

Bir güvenlik sorunu bulduysan (ör. köprü üzerinden izinsiz arama yaptırılabilmesi, bilgi sızması) **herkese açık issue açma**. Bunun yerine:

- GitHub'da **[özel güvenlik bildirimi](https://github.com/mustafayusufaksoy/iphone-hat-koprusu/security/advisories/new)** gönder, ya da
- X'te [@codewandertech](https://x.com/codewandertech) hesabına özel mesaj at.

Birkaç gün içinde dönüş yaparım. Sorun bu repodaki betikler ya da rehberle ilgiliyse burada düzeltirim; [Voice SIP Agent](https://github.com/sparkcyf/android-voice-sip-agent), Shizuku, Linphone veya SmsForwarder ile ilgiliyse ilgili projeye iletmene yardım ederim.

## Bilinen risk

Voice SIP Agent dış arama isteklerinde arayanın kim olduğunu kontrol etmiyor; Android'in SIP hesap adını bilen biri telefona arama yaptırabilir. README'deki önlemler: tahmin edilmesi zor hesap adı, izinli numara listesi (`scripts/dis-arama.sh`), kullanılmıyorsa dış aramayı kapatmak.

---

## Reporting a vulnerability

Please **do not open a public issue**. Use a [private security advisory](https://github.com/mustafayusufaksoy/iphone-hat-koprusu/security/advisories/new) or a DM to [@codewandertech](https://x.com/codewandertech). Issues in upstream projects (Voice SIP Agent, Shizuku, Linphone, SmsForwarder) belong to those projects; I can help route them.

Known risk: Voice SIP Agent does not authenticate the caller on outbound calls. Use an unguessable SIP account name and restrict dial-out prefixes.

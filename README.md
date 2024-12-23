# Teneo Community Node BOT
Teneo Community Node BOT

Download Extension Here : [Teneo Community Node](https://chromewebstore.google.com/detail/teneo-community-node/emcclcoaglgcpoognfiggmhnhgabppkm) | Use Code : X8sT2

## Fitur

  - Auto Get Account Information
  - Auto Run With Auto Proxy if u Choose 1
  - Auto Use [Monosans Proxy](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) if u Choose Run With Auto Proxy
  - Auto Run With Manual Proxy if u Choose 2
  - Auto Run Without Proxy if u Choose 3
  - Auto Connect Node
  - Auto Send Ping
  - Multi Account With Thread

## Prasyarat

Pastikan Anda telah menginstal Python3.9 dan PIP.

## Instalasi

1. **Kloning repositori:**
   ```bash
   git clone https://github.com/vonssy/Teneo-BOT.git
   ```
   ```bash
   cd Teneo-BOT
   ```

2. **Instal Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Konfigurasi

- **accounts.json:** Anda akan menemukan file `accounts.json` di dalam direktori proyek. Pastikan `accounts.json` berisi data yang sesuai dengan format yang diharapkan oleh skrip. Berikut adalah contoh format file:

  ```bash
    [
        {
            "Email": "your_email_address 1",
            "Password": "your_password 1"
        },
        {
            "Email": "your_email_address 2",
            "Password": "your_password 2"
        }
    ]
  ```
- **manual_proxy.txt:** Anda akan menemukan file `manual_proxy.txt` di dalam direktori proyek. Pastikan `manual_proxy.txt` berisi data yang sesuai dengan format yang diharapkan oleh skrip. Berikut adalah contoh format file:
  ```bash
    ip:port #http or socks5 - change schemes in line 110
    http://ip:port
    socks4://ip:port
    socks5://ip:port
    http://ip:port@user:pass #idk its work or not, cuase i don't have authentic proxy
    socks4://ip:port@user:pass #idk its work or not, cuase i don't have authentic proxy
    socks5://ip:port@user:pass #idk its work or not, cuase i don't have authentic proxy
  ```

## Jalankan

```bash
python bot.py #or python3 bot.py
```

## Penutup

Terima kasih telah mengunjungi repository ini, jangan lupa untuk memberikan kontribusi berupa follow dan stars.
Jika Anda memiliki pertanyaan, menemukan masalah, atau memiliki saran untuk perbaikan, jangan ragu untuk menghubungi saya atau membuka *issue* di repositori GitHub ini.

**vonssy**
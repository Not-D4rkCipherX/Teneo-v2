# Teneo Community Node BOT
Teneo Community Node BOT

- Register Here : [Teneo Community Node Dashboard](https://dashboard.teneo.pro/auth/signup)
- Download Extension Here : [Teneo Community Node Extension](https://chromewebstore.google.com/detail/teneo-community-node/emcclcoaglgcpoognfiggmhnhgabppkm)
- Use Code : fGgJ4

## Features

  - Auto Get Account Information
  - Auto Run With [Monosans](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) Proxy - Choose 1
  - Auto Run With Private Proxy - Choose 2
  - Auto Run Without Proxy - Choose 3
  - Auto Claim Refferal Reward
  - Auto Claim Refferal & Heartbeat Campaigns Reward
  - Auto Connect and Reconnect Websocket
  - Auto Receive Message Every 15 Minutes
  - Multi Accounts With Threads

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/Not-D4rkCipherX/Teneo-v2.git
   ```
   ```bash
   cd Teneo-v2
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
```bash
nano accounts.json
```
- **accounts.json:** You will find the file `accounts.json` inside the project directory. Make sure `accounts.json` contains data that matches the format expected by the script. Here are examples of file formats:
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

- **proxy.txt:** You will find the file `proxy.txt` inside the project directory. Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats: (Proxy Is Optional)
  ```
  nano proxy.txt
  ```
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Run

```bash
python bot.py
```

Thank you for visiting this repository, don't forget to contribute in the form of follows and stars.
If you have questions, find an issue, or have suggestions for improvement, feel free to contact me or open an *issue* in this GitHub repository.

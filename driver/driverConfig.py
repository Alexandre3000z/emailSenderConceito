import os, sys, subprocess, requests, zipfile, shutil


def get_chrome_version():
    """Lê a versão do Chrome instalado no Windows."""
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        return version.split(".")[0]  # só o major, ex: "124"
    except Exception:
        # Fallback via subprocess
        result = subprocess.run(
            ['reg', 'query',
             r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'],
            capture_output=True, text=True
        )
        # parse da saída...
        return None

def get_driver_path():
    """Retorna pasta persistente de dados do app (fora do exe)."""
    base = os.path.join(os.environ.get("APPDATA", ""), "MeuApp", "drivers")
    os.makedirs(base, exist_ok=True)
    return base

def ensure_chromedriver():
    driver_dir = get_driver_path()
    driver_exe = os.path.join(driver_dir, "chromedriver.exe")
    version_file = os.path.join(driver_dir, "version.txt")

    chrome_version = get_chrome_version()
    if not chrome_version:
        raise RuntimeError("Não foi possível detectar a versão do Chrome.")

    # Verifica se o driver já está na versão correta
    if os.path.exists(driver_exe) and os.path.exists(version_file):
        with open(version_file) as f:
            cached = f.read().strip()
        if cached == chrome_version:
            return driver_exe  # tudo certo, usa o cache

    print(f"Atualizando ChromeDriver para Chrome {chrome_version}...")

    # Chrome 115+ usa a nova API do Chrome for Testing
    url = (f"https://googlechromelabs.github.io/chrome-for-testing/"
           f"LATEST_RELEASE_{chrome_version}")
    full_version = requests.get(url, timeout=10).text.strip()

    zip_url = (f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"
               f"{full_version}/win64/chromedriver-win64.zip")
    
    zip_path = os.path.join(driver_dir, "chromedriver.zip")
    with requests.get(zip_url, stream=True, timeout=30) as r:
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    with zipfile.ZipFile(zip_path, "r") as z:
        # O zip tem subpasta chromedriver-win64/chromedriver.exe
        for member in z.namelist():
            if member.endswith("chromedriver.exe"):
                with z.open(member) as src, open(driver_exe, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                break
    
    os.remove(zip_path)

    # Salva a versão no cache
    with open(version_file, "w") as f:
        f.write(chrome_version)

    return driver_exe



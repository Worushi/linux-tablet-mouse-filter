# 🎨 PenPriority-Linux / Приоритет Пера для Linux

**[English](#english)** | **[Русский](#русский)**

---

<a id="english"></a>
## 🇬🇧 English

A lightweight Python daemon for Linux that solves the "mouse vs. pen" conflict on drawing tablets. When you bring your pen close to the tablet, it completely disables your physical mouse (preventing accidental clicks and cursor jumps) and converts your mouse scroll wheel into Zoom In/Out shortcuts. 

Perfect for digital painting in **Krita**, **Blender**, **MyPaint**, etc.

### ✨ Features
- 🖊️ **Pen Priority:** Completely disables mouse movement and clicks when the pen hovers over the tablet.
- 🔄 **Scroll to Zoom:** Converts mouse scroll wheel events into keyboard shortcuts (`+` / `-`) when the pen is active.
- 🚀 **Hi-Res Wheel Support:** Correctly handles modern mice with high-resolution scroll wheels without causing zoom spam.
- 🧹 **Clean Virtual Devices:** Creates separate virtual mouse and keyboard devices to prevent DE (KDE/GNOME) confusion.

### 🛠️ Prerequisites
- Python 3.8+
- `evdev` library
- Linux system with `/dev/input/` access (Wayland and X11 both supported)

### 📦 Installation

1. **Install dependencies:**
   ```bash
   # For Fedora/RHEL:
   sudo dnf install python3-evdev
   
   # For Ubuntu/Debian:
   sudo apt install python3-evdev
   
   # Or via pip:
   pip install evdev
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/Worushi/linux-tablet-mouse-filter.git
   cd linux-tablet-mouse-filter
   ```

3. **Find your device paths:**
   You need to find the exact paths for your tablet and mouse. Run:
   ```bash
   ls -l /dev/input/by-id/
   ```
   Look for your tablet (e.g., `*event-mouse` or `*event-kbd`) and your physical mouse.

4. **Configure the script:**
   Open `tablet_priority.py` and update the paths at the top of the file:
   ```python
   TABLET_PATH = '/dev/input/by-id/usb-YOUR_TABLET-event-mouse'
   MOUSE_PATH = '/dev/input/by-id/usb-YOUR_MOUSE-event-mouse'
   ```

### 🚀 Usage

**Option 1: Run manually (requires root or `input` group)**
```bash
sudo python3 tablet_priority.py
```

**Option 2: Add your user to the `input` group (Recommended)**
```bash
sudo usermod -aG input $USER
# Log out and log back in for changes to take effect!
python3 tablet_priority.py
```

**Вариант 3: Create script and load in systemctl**
```bash
sudo nano /usr/local/bin/tablet_priority.py

# Paste demon in terminal
```
```
sudo systemctl enable --now tablet-priority.service
sudo systemctl start tablet-priority.service

```

### ⚙️ Configuration & Troubleshooting

- **Zoom doesn't work in Krita?** 
  By default, the script emulates Numpad `+` and `-`. Ensure your Krita shortcuts for Zoom In/Out are set to these keys (`Settings -> Configure Keyboard Shortcuts`).
- **Permission Denied errors?** 
  You must run the script as `root` (via `sudo`) or add your user to the `input` group (see Usage Option 2).
- **Script crashes with `OSError: [Errno 22] Invalid argument`?**
  This is fixed in the current version. The script manually defines clean mouse capabilities instead of blindly copying them from the physical mouse.

---

<a id="русский"></a>
## 🇷🇺 Русский

Легковесный Python-демон для Linux, который решает конфликт «мыши и пера» на графических планшетах. Когда вы подносите перо к планшету, скрипт полностью отключает физическую мышь (предотвращая случайные клики и прыжки курсора) и превращает колесико мыши в шорткаты Зума.

Идеально подходит для рисования в **Krita**, **Blender**, **MyPaint** и других программах. Проверено на Arch linux и Fedora

### ✨ Возможности
- 🖊️ **Приоритет пера:** Полностью отключает движение и клики мыши, когда перо находится в зоне видимости планшета.
- 🔄 **Скролл в Зум:** Превращает колесико мыши в нажатия клавиш (`+` / `-`) при активном пере.
- 🚀 **Поддержка Hi-Res колесика:** Корректно работает с современными мышами, не вызывая «спама» зумом.
- 🧹 **Чистые виртуальные устройства:** Создает раздельные виртуальные мышь и клавиатуру, чтобы KDE/GNOME не сходили с ума.

### 🛠️ Требования
- Python 3.8+
- Библиотека `evdev`
- Linux (поддерживаются Wayland и X11)

### 📦 Установка

1. **Установите зависимости:**
   ```bash
   # Для Fedora:
   sudo dnf install python3-evdev
   
   # Для Ubuntu/Debian:
   sudo apt install python3-evdev
   
   # Или через pip:
   pip install evdev
   ```

2. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Worushi/linux-tablet-mouse-filter.git
   cd linux-tablet-mouse-filter
   ```

3. **Найдите пути к вашим устройствам:**
   Выполните команду, чтобы найти точные пути к планшету и мыши:
   ```bash
   ls -l /dev/input/by-id/
   ```
   Найдите в списке ваш планшет (обычно оканчивается на `*event-mouse`) и вашу физическую мышь.

4. **Настройте скрипт:**
   Откройте `tablet_priority.py` и замените пути в начале файла на ваши:
   ```python
   TABLET_PATH = '/dev/input/by-id/usb-ВАШ_ПЛАНШЕТ-event-mouse'
   MOUSE_PATH = '/dev/input/by-id/usb-ВАША_МЫШЬ-event-mouse'
   ```

### 🚀 Запуск

**Вариант 1: Запуск через sudo**
```bash
sudo python3 tablet_priority.py
```

**Вариант 2: Добавить пользователя в группу `input` (Рекомендуется)**
```bash
sudo usermod -aG input $USER
# Обязательно перезагрузитесь или выйдите из системы и зайдите снова!
python3 tablet_priority.py
```

**Вариант 3: Добавить скрипт в автозагрузку через nano**
```bash
sudo nano /usr/local/bin/tablet_priority.py

# В терминал вставляете скрипт
```
```
sudo systemctl enable --now tablet-priority.service
sudo systemctl start tablet-priority.service

```

### ⚙️ Настройка и решение проблем

- **Зум не работает в Krita?** 
  По умолчанию скрипт эмулирует клавиши `+` и `-` с цифрового блока (Numpad). Убедитесь, что в настройках Krita (`Настройки -> Настроить сочетания клавиш`) зум назначен именно на эти клавиши.
- **Ошибки доступа (Permission Denied)?** 
  Скрипт требует доступа к `/dev/input/`. Запускайте его через `sudo` или добавьте своего пользователя в группу `input` (см. Вариант 2).
- **Скрипт падает с ошибкой `Invalid argument`?**
  В текущей версии это исправлено. Скрипт вручную задает чистые параметры виртуальной мыши, чтобы избежать конфликтов с ядром Linux.

---

### 🤝 Contributing / Вклад
Feel free to open issues or submit pull requests if you have ideas for improvements!
Буду рад советам по демону, если у вас есть идеи по улучшению!

### 📜 License / Лицензия
MIT License.

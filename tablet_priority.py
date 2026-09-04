import evdev
import threading
import time
from evdev import ecodes

"""Пути к устройствам"""
TABLET_PATH = '/dev/input/by-id/usb-UGTABLET_11.6_inch_PenDisplay-if01-event-mouse'
MOUSE_PATH = '/dev/input/by-id/usb-Logitech_USB_Receiver-if02-event-mouse'

try:
    tablet = evdev.InputDevice(TABLET_PATH)
    mouse = evdev.InputDevice(MOUSE_PATH)
    rel_axes = [ecodes.REL_X, ecodes.REL_Y, ecodes.REL_WHEEL, ecodes.REL_HWHEEL]
    
    if hasattr(ecodes, 'REL_WHEEL_HI_RES'):
        rel_axes.append(ecodes.REL_WHEEL_HI_RES)
    if hasattr(ecodes, 'REL_HWHEEL_HI_RES'):
        rel_axes.append(ecodes.REL_HWHEEL_HI_RES)

    mouse_caps = {
        ecodes.EV_KEY: [
            ecodes.BTN_LEFT, ecodes.BTN_RIGHT, ecodes.BTN_MIDDLE,
            ecodes.BTN_SIDE, ecodes.BTN_EXTRA, ecodes.BTN_FORWARD, ecodes.BTN_BACK
        ],
        ecodes.EV_REL: rel_axes
    }
    
    v_mouse = evdev.UInput(mouse_caps, name="Virtual_Mouse_Filtered")
    
    kb_caps = {
        ecodes.EV_KEY: [ecodes.KEY_KPPLUS, ecodes.KEY_KPMINUS]
    }
    v_kb = evdev.UInput(kb_caps, name="Virtual_Keyboard_Zoom")
    
except FileNotFoundError as e:
    print(f"Ошибка: Не найдено устройство {e}")
    exit(1)
except PermissionError:
    print("Ошибка: Нет прав доступа. Запустите скрипт через sudo или добавьте пользователя в группу input.")
    exit(1)
except OSError as e:
    print(f"Ошибка ядра при создании устройства: {e}")
    exit(1)

pen_hovering = False

def monitor_tablet():
    """Следит за пером планшета"""
    global pen_hovering
    for event in tablet.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code in [ecodes.BTN_TOOL_PEN, ecodes.BTN_TOOL_RUBBER]:
                pen_hovering = (event.value == 1)

def emit_key(device, keycode):
    """Эмулирует нажатие клавиши с микро-задержкой"""
    device.write(ecodes.EV_KEY, keycode, 1)
    device.syn()
    time.sleep(0.03)  # 30мс задержка, чтобы Krita успела зарегистрировать
    device.write(ecodes.EV_KEY, keycode, 0)
    device.syn()

def monitor_mouse():
    """Перехватывает мышь и фильтрует события"""
    global pen_hovering
    mouse.grab() 
    
    for event in mouse.read_loop():
        if event.type == ecodes.EV_REL:
            if event.code in [ecodes.REL_X, ecodes.REL_Y]:
                if not pen_hovering:
                    v_mouse.write_event(event)
                    
            elif event.code == ecodes.REL_WHEEL:
                if pen_hovering:
                    if event.value > 0:
                        emit_key(v_kb, ecodes.KEY_KPPLUS)
                    elif event.value < 0:
                        emit_key(v_kb, ecodes.KEY_KPMINUS)
                else:
                    v_mouse.write_event(event)
                    
            elif event.code in [getattr(ecodes, 'REL_WHEEL_HI_RES', -1), getattr(ecodes, 'REL_HWHEEL_HI_RES', -1)]:
                if not pen_hovering:
                    v_mouse.write_event(event)
                    
            else:
                if not pen_hovering:
                    v_mouse.write_event(event)
                    
        elif event.type == ecodes.EV_KEY:
            if not pen_hovering:
                v_mouse.write_event(event)
                
        else:
            if not pen_hovering:
                v_mouse.write_event(event)

if __name__ == '__main__':
    print("Гибридный фильтр мыши-клавиатуры запущен.")
    print("Когда перо у экрана - мышь отключается, колесико зумит.")
    
    t_tablet = threading.Thread(target=monitor_tablet, daemon=True)
    t_mouse = threading.Thread(target=monitor_mouse, daemon=True)
    
    t_tablet.start()
    t_mouse.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        try:
            mouse.ungrab()
        except Exception:
            pass
        v_mouse.close()
        v_kb.close()
        print("\nСкрипт остановлен.")

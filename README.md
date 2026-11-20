# VanishCam for macOS

Webcam effects that make you disappear and reappear with a hand gesture. You can see
the result in a preview window, or use it as your camera in Teams, Zoom, Meet,
FaceTime and similar apps.

Ported from [Nicovic17/vanish_webcam](https://github.com/Nicovic17/vanish_webcam), which was written for Windows.
All video is processed on your Mac. Nothing is recorded or uploaded.

## Requirements

- macOS on Apple Silicon or Intel
- Python 3 (`python3 --version`)
- A webcam
- [OBS Studio](https://obsproject.com) 30 or later, only if you want to use the effect in Teams or another video app

## Run it

```bash
cd ~/Desktop/projects/Cam-effect
./VanishCam.command
```

You can also double-click `VanishCam.command` in Finder.

The first launch creates a Python environment in `.venv` and installs the
dependencies, which takes a few minutes. It also downloads the MediaPipe models.
After that, it starts right away.

macOS will ask for camera access for Terminal or VS Code. Allow it. If you missed
the prompt, go to System Settings → Privacy & Security → Camera.

### Steps

1. **Choose a mode** with the mouse or keys `1`–`5`.
2. **Choose your webcam** with `+`/`-` or keys `0`–`9`, then press `Enter`.
3. **Goku only:** set how long to hold the gesture. Press `Enter` for 1 second.
4. **Step out of the frame for 4 seconds** while the empty background is captured.
   The terminal counts down.
5. **Come back and do the gesture.**

### Modes

| Mode | Vanish | Reappear | Effect |
|---|---|---|---|
| **1 Normal** | V sign (index and middle fingers) | `R` | Sparkling dissolve, played backwards to reappear |
| **2 Naruto** | Palms pressed together, fingers side by side, both hands visible | `R` | Smoke and a falling log; the log rises back into smoke to reappear |
| **3 Particles** | V sign | `R` | You blow away as particles in the wind; they fly back to reappear |
| **4 Goku** | Two fingers straight and together on your forehead, held for the set time | Same gesture again | Teleport speed lines and sound |
| **5 Itachi** | Both hands touching in front of the center of your chest | Same gesture again, or `R` | You scatter into crows, which come back to reappear |

Before reappearing, step back into the frame. In Particles mode, also hold still
when you press `R`, because your silhouette is captured at that moment.

### Keys

Click the VanishCam window first. Keys only work when it's focused.

| Key | Action |
|---|---|
| `V` | Vanish without a gesture (not in Goku) |
| `R` | Reappear (not in Goku) |
| `SPACE` | Capture the background again (step out of frame) |
| `F` | Toggle fullscreen |
| `Q` / `ESC` | Quit |

### Options

```bash
./VanishCam.command --mode naruto      # skip the menu: normal | naruto | particles | goku | itachi
./VanishCam.command --camera 1         # skip the webcam picker
./VanishCam.command --width 1280 --height 720 --fps 30
./VanishCam.command --no-mirror        # don't flip the image like a selfie
./VanishCam.command --no-virtual-camera  # preview window only
./VanishCam.command --virtual-camera   # stop with an error if the virtual camera is unavailable
./VanishCam.command --gesture-debug    # print gesture detection info in the terminal
```

## Use it in Teams (or Zoom, Meet, FaceTime…)

VanishCam sends its video to **OBS Virtual Camera**, and Teams uses that as a webcam.

### One-time OBS setup

1. Install OBS Studio from <https://obsproject.com>, or run:
   ```bash
   brew install --cask obs
   ```
2. Open OBS: press `⌘ Space`, type **OBS**, then press `Enter`. If the
   auto-configuration wizard appears, click **Cancel**.
3. Click **Start Virtual Camera** in the bottom-right Controls panel.
4. Allow the OBS camera extension when macOS asks. To find the setting:
   - In System Settings, search for **Extensions**, open **Camera Extensions**
     and turn **OBS** on.
   - Or, under **Privacy & Security**, click **Allow** next to the
     "System software from 'OBS' was blocked" message.
   - Or, from Terminal:
     `open "x-apple.systempreferences:com.apple.LoginItems-Settings.extension"`
5. Click **Stop Virtual Camera** and quit OBS (`⌘ Q`). Restart your Mac if the
   check below fails.

Check that it works:

```bash
systemextensionsctl list | grep -i obs   # should show [activated enabled]
.venv/bin/python -c "import pyvirtualcam; c=pyvirtualcam.Camera(640,480,30); print('OK', c.device); c.close()"
```

### Every time

1. **Make sure OBS is closed,** or at least that its virtual camera is stopped.
   Only one app can drive the virtual camera.
2. **Start VanishCam** with `./VanishCam.command`. The terminal should show:
   `[Webcam] Virtual output active: OBS Virtual Camera`.
3. **Choose a mode and your real webcam,** then step out of the frame for 4 seconds.
4. **In Teams,** go to **Settings → Devices → Camera** (or use the arrow next to
   the camera button in a meeting) and choose **OBS Virtual Camera**.
5. **Do the gesture.** Everyone in the call sees the effect.

### Tips

- **Keep the VanishCam window open.** Minimise it if you like. If you close it,
  Teams shows a black or placeholder image.
- **Restart Teams** if OBS Virtual Camera isn't listed. Teams only checks for
  cameras at launch, so start VanishCam first.
- **Keep the camera and lighting still** after the background capture. If
  anything changes, press `SPACE` to capture it again.
- **Mirroring:** the image is mirrored like a selfie, so others see any text
  behind you backwards. Use `--no-mirror` to avoid that.

## Troubleshooting

| Problem | Fix |
|---|---|
| `OBS Virtual Camera is not installed` | Do the one-time OBS setup above, then restart your Mac. |
| Virtual camera busy or unavailable | Stop "Start Virtual Camera" in OBS, or quit OBS. |
| `Webcam 0 not available` | Close other apps that use the camera, or try `--camera 1`. Check camera permission. |
| Model download fails | Check your internet connection. The launcher already works around the missing SSL certificates in python.org Python. |
| Gesture not detected | Use good lighting and keep your hands fully in frame. Run with `--gesture-debug` to see what's detected. |
| Your outline looks patchy | Capture the background again with `SPACE` and keep the camera still. |

## Tests

```bash
.venv/bin/python -m unittest discover -s local_app -t . -p 'test_*.py'
```

## Project layout

```
VanishCam.command        macOS launcher (creates .venv, installs deps, runs the app)
local_app/vanish_cam.py  main app: menus, camera loop, gestures, virtual camera output
local_app/*_effect.py    effect renderers (naruto, particles, goku, itachi)
local_app/assets/        log sprite, crow sprites, Sharingan, sounds
local_app/models/        MediaPipe models (downloaded on first run)
```

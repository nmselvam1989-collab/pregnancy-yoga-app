# கர்ப்பகால யோகா (Pregnancy Yoga) — Tamil Android App

A Kivy-based Python app with 9 pregnancy-safe yoga poses, step-by-step
instructions in Tamil, and a per-pose countdown timer.

## Why there's no .apk file in this download

Building an Android APK requires the Android SDK, NDK, and Buildozer
running with internet access to download those toolchains — that isn't
available in the environment used to generate this code. What you have
here is the **complete, ready-to-build source code**. You build the APK
yourself with one command (steps below), either on your own Linux/WSL
machine or automatically via GitHub Actions (no local setup needed).

## 1. Add a Tamil font (required)

Android's default font can't render Tamil script. Download **Noto Sans
Tamil** (free, Google Fonts) and save it as:

```
assets/fonts/NotoSansTamil-Regular.ttf
```

Get it here: https://fonts.google.com/noto/specimen/Noto+Sans+Tamil
(click "Download family", unzip, pick the Regular weight, rename it to
match the path above).

Without this file, the app still runs but Tamil text shows as blank
boxes.

## 2. Test on your computer first (optional but recommended)

```bash
pip install kivy
python main.py
```

This opens a desktop window so you can check the layout before building
for Android.

## 3. Build the APK

### Option A — Build locally (Linux or WSL2 on Windows)

```bash
pip install buildozer cython
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf \
    libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev

cd pregnancy_yoga_app
buildozer -v android debug
```

The first build downloads the Android SDK/NDK automatically and can take
20–40 minutes. The finished file appears at:

```
bin/pregnancyyoga-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

Copy that .apk to your phone and install it (enable "Install unknown
apps" for your file manager/browser first).

### Option B — Build in the cloud with GitHub Actions (no local setup)

1. Push this folder to a new GitHub repository.
2. Add a workflow file `.github/workflows/build.yml`:

```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install buildozer cython
      - run: |
          sudo apt update
          sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool \
            pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
            cmake libffi-dev libssl-dev
      - run: buildozer -v android debug
      - uses: actions/upload-artifact@v4
        with:
          name: apk
          path: bin/*.apk
```

3. Push the commit. Once the Action finishes, download the `.apk` from
   the workflow run's "Artifacts" section.

## 4. Publishing to the Play Store (later)

For a real release you'll need a signed release build
(`buildozer android release`) and a Google Play Developer account.
Ask me when you're ready and I'll walk you through signing.

## Project structure

```
pregnancy_yoga_app/
├── main.py            # App UI, screens, timer logic
├── data.py             # All 9 exercises — Tamil names, steps, benefits
├── buildozer.spec      # Android packaging config
├── assets/
│   ├── fonts/           # put NotoSansTamil-Regular.ttf here
│   └── images/           # optional: icon.png, pose photos
└── README.md
```

## Customizing content

All exercise text lives in `data.py` — add, remove, or edit poses there
without touching `main.py`. Each entry supports a trimester tag so you
can later filter poses by trimester if you want that feature added.

## Safety note in the app

The app shows a disclaimer (button: "எச்சரிக்கை குறிப்பு") reminding
users to consult their doctor before starting and to stop immediately
if they feel pain, dizziness, or discomfort. Keep this — pregnancy
exercise apps should always carry this kind of notice.

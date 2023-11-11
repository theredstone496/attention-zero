# attention-zero
Adds subway surfers or other attention-catching content to a lecture to maintain the attention of people with ADD

# Features
1. Random popup window mode
- Launches new windows that play a video
- Video is always on top* (unless application also forces on top)
2. Editing that does split screen for you
3. Editing that simply pastes the video on top for you

# Installing
You need to download node and npm in order to use electronjs
You will also need to install [ffmpeg](https://www.ffmpeg.org/download.html) for the random popup video thing to work
```
cd attention-zero
npm install --save-dev electron
npm install
```

If you have issues with electronjs installation see [the Docs](https://www.electronjs.org/docs/latest/tutorial/installation)

you may need to install it globally:
```
npm install --save-dev -g electron
```

# Running

while you are still in the `/attention-zero` folder:
```
electron .
```

# Work Distribution Matrix

|--|hemidemisemipresent|theredstone496|foo-barian|
|--|--|--|--|
|electron.js app|✓|||
|video editing|||✓|
|algorithm/AI to detect empty parts of a video||✓||
|slides|✓|✓|✓|
|README|✓||✓|
|this matrix|✓|||
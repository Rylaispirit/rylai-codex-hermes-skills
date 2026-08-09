# Model-Neutral Video Prompting

> Portable Codex-Hermes replacement authored by Rylai.

## Shot Promp

Specify:

- Subject and persistent appearance
- Starting state and visible action
- Environment and time
- Shot size and camera position
- Camera movemen
- Lighting and color
- Motion speed and physical constraints
- Duration and aspect ratio
- Audio, dialogue, captions, or silence
- Elements that must not change

## Example Structure

```tex
Duration: [seconds]. Aspect ratio: [ratio].
Subject: [specific description].
Scene: [environment and time].
Action: [one continuous action with start and end state].
Camera: [shot size], [lens feel], [movement].
Lighting: [source and mood].
Continuity: keep [identity, clothing, product details] unchanged.
Audio: [voice, ambience, music, or none].
Avoid: [likely defects only].


## Multi-Shot Sequence

Plan each shot with:

| Shot | Duration | Purpose | Visual | Camera | Transition |
|---|---:|---|---|---|---|
| 1 |  | Hook |  |  |  |

Keep a continuity sheet for characters, wardrobe, props, location, time, color,
and screen direction.

## Text And Interface

Generate clean visual footage, then add important text, captions, logos, and UI
overlays deterministically in an editor or programmatic video tool.

## QA

- Identity and objects remain consistent.
- Motion does not jump or reverse unintentionally.
- Product geometry and UI are accurate.
- Captions remain within safe areas.
- Audio timing matches visible action.
- The delivered file has the requested duration, dimensions, and codec.

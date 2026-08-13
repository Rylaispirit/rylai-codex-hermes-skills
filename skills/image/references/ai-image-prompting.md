# Model-Neutral Image Prompting

> Portable Codex-Hermes-Claude replacement authored by Rylai.

## Prompt Structure

Describe:

1. Subject: exact people, objects, product, or environment.
2. Action and state: what is happening and what must be visible.
3. Composition: shot size, camera angle, layout, and empty space.
4. Lighting: source, direction, softness, and time of day.
5. Materials and color: concrete surfaces, palette, and contrast.
6. Style: photo, illustration, editorial, diagram, or texture.
7. Output: aspect ratio, resolution intent, transparency, and text policy.
8. Exclusions: only defects or elements likely to appear.

## Product Image

```text
[Product] shown from [angle] on [surface/environment]. Preserve exact shape,
materials, controls, and branding from the supplied reference. [Lighting].
[Composition and negative space]. [Aspect ratio]. No invented ports, labels,
accessories, or interface details.
```

## Editorial Illustration

```text
Illustrate [single idea] through [visual metaphor]. [Characters or objects],
[composition], [palette], [line or paint treatment], [mood]. Keep the hierarchy
clear at thumbnail size. No decorative text unless explicitly requested.
```

## UI Or Screenshot Rule

Do not ask an image model to recreate a real product interface when accuracy
matters. Capture or render the actual UI and use image generation only for
supporting art, backgrounds, or clearly fictional concepts.

## Consistency

For a series, repeat the same character description, camera language, palette,
materials, and rendering style. Change only the scene-specific action.

## QA

- Subject count and anatomy are correct.
- Product or brand details match references.
- Text is readable or absent as requested.
- Important content is inside safe crop areas.
- Lighting and shadows are physically coherent.
- The image works at its final display size.

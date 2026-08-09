# Deck Specification

The JSON root is an object:

- `title`: required presentation title.
- `subtitle`: optional title-slide supporting line.
- `slides`: required array of content slides.

Each slide supports:

- `title`: required slide title.
- `bullets`: optional array of short strings.
- `body`: optional paragraph used when there are no bullets.
- `image`: optional local image path. Remote image URLs are rejected.

Keep each slide focused on one message. Prefer three to five bullets, and keep
each bullet short enough to read without reducing the font size.

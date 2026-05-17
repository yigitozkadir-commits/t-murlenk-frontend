---
name: Imperial Command
colors:
  surface: '#131316'
  surface-dim: '#131316'
  surface-bright: '#39393c'
  surface-container-lowest: '#0e0e11'
  surface-container-low: '#1b1b1e'
  surface-container: '#1f1f22'
  surface-container-high: '#2a2a2d'
  surface-container-highest: '#353438'
  on-surface: '#e4e1e6'
  on-surface-variant: '#e1bebb'
  inverse-surface: '#e4e1e6'
  inverse-on-surface: '#303033'
  outline: '#a98986'
  outline-variant: '#59413e'
  surface-tint: '#ffb4ac'
  primary: '#ffb4ac'
  on-primary: '#690006'
  primary-container: '#9e1b1b'
  on-primary-container: '#ffafa7'
  inverse-primary: '#b22a27'
  secondary: '#e9c176'
  on-secondary: '#412d00'
  secondary-container: '#604403'
  on-secondary-container: '#dab36a'
  tertiary: '#bcc7dd'
  on-tertiary: '#263142'
  tertiary-container: '#465164'
  on-tertiary-container: '#b9c4da'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad6'
  primary-fixed-dim: '#ffb4ac'
  on-primary-fixed: '#410002'
  on-primary-fixed-variant: '#8f0e12'
  secondary-fixed: '#ffdea5'
  secondary-fixed-dim: '#e9c176'
  on-secondary-fixed: '#261900'
  on-secondary-fixed-variant: '#5d4201'
  tertiary-fixed: '#d8e3fa'
  tertiary-fixed-dim: '#bcc7dd'
  on-tertiary-fixed: '#111c2c'
  on-tertiary-fixed-variant: '#3c475a'
  background: '#131316'
  on-background: '#e4e1e6'
  surface-variant: '#353438'
typography:
  display-lg:
    fontFamily: ebGaramond
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: ebGaramond
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-sm:
    fontFamily: ebGaramond
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: jetbrainsMono
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: jetbrainsMono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  data-tabular:
    fontFamily: jetbrainsMono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-caps:
    fontFamily: jetbrainsMono
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.1em
spacing:
  unit: 4px
  gutter: 16px
  margin-safe: 32px
  panel-gap: 8px
  data-density: tight
---

## Brand & Style
The design system embodies the gravity of an imperial war room: authoritative, high-stakes, and unyielding. It targets users who require total oversight and strategic dominance. The aesthetic is a sophisticated blend of **Brutalism** and **Modern Corporate**, utilizing heavy structural framing and metallic textures to ground the interface in a physical, militaristic reality.

The emotional response should be one of "controlled urgency"—the feeling of standing before a secure tactical display in a palace bunker. Visuals are dense and information-rich, favoring functional precision over decorative whitespace. Every element is designed to feel like a machined component of a larger machine of state.

## Colors
The palette is rooted in a "Deep Gunmetal" neutral base to simulate dark metallic surfaces. 

- **Primary (Imperial Crimson):** Used sparingly for critical alerts, high-level commands, and state-level status indicators.
- **Secondary (Regal Gold):** Used for decorative accents, borders of high-priority containers, and royal decrees (headers). It signifies prestige and authority.
- **Tertiary (Tactical Slate):** A desaturated blue-grey used for secondary data visualizations and inactive UI states to maintain a technical, "radar-screen" atmosphere.
- **Surface Tones:** Use varying shades of charcoal with subtle blue tints to create the illusion of brushed steel and iron plating.

## Typography
This design system utilizes a dual-font strategy to balance imperial tradition with modern tactical efficiency.

- **The Serif (ebGaramond):** Reserved for high-level headers and narrative summaries. It provides a "literary" and "historical" weight, suggesting the longevity of the empire.
- **The Monospace (jetbrainsMono):** Used for all tactical data, coordinates, labels, and interactive components. The fixed-width nature ensures that shifting data values do not cause layout jumps, mimicking a command-line terminal or radar output.

All labels should be treated with high letter-spacing and uppercase styling to enhance the "instrument panel" aesthetic.

## Layout & Spacing
The layout follows a **Fixed Grid** philosophy, mirroring a hardware console where every "module" has a designated place. 

- **Grid:** Use a 12-column system with tight 16px gutters. Panels should be clearly demarcated by 1px borders rather than expansive white space.
- **Density:** High density is preferred. Information should be packed efficiently to allow for simultaneous monitoring of multiple data streams.
- **Adaptation:** On mobile, panels stack vertically, but the "bezel" (margins) remains thick to maintain the feeling of a portable ruggedized device.
- **Organization:** Group related data into "Tactical Blocks"—containers with specific headers and footer status bars.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** and **Metallic Outlines** rather than soft shadows.

- **Stacking:** The base layer is the darkest gunmetal. Overlaid panels use a slightly lighter grey (#1A1A1F). 
- **Borders as Depth:** Use 1px "inner-glow" borders (Gold for primary panels, Slate for secondary) to simulate the edge of a physical screen or metal plate.
- **Active States:** Elements don't "lift" towards the user; they "light up." Use neon-like glows (using the Crimson or Gold) to indicate focus or active status.
- **Glass:** Subtle use of dark, semi-transparent overlays (Backdrop Blur: 8px) can be used for modal "intercepts" that appear over the tactical map.

## Shapes
The shape language is strictly **Sharp (0)**. In an imperial war room, there is no room for soft corners. 

Everything—from buttons to the containers holding them—must have 90-degree angles. This reinforces the militaristic, industrial, and "machined" nature of the design system. For specialized tactical indicators (like map markers), use hexagonal or diamond shapes to differentiate them from standard UI rectangular containers.

## Components
- **Buttons:** Sharp-edged with 1px borders. Primary buttons use a solid Crimson fill with white mono text. Secondary buttons use a transparent background with a Gold border. Active states should involve a "scan-line" texture overlay.
- **Input Fields:** Styled as "Data Entry Brackets." Use a subtle background fill and a bottom-only 2px border in Slate. 
- **Status Chips:** Small, rectangular indicators. "Active" uses a steady Crimson glow; "Idle" uses a dim Slate.
- **Tactical Cards:** High-contrast containers with a "Header Bar" in a contrasting metal tone. Use monospaced data in the body and a Garamond title in the header.
- **Lists:** Dotted horizontal separators (1px dashed) between items. Each list item should have a "Coordinate ID" (e.g., [001-A]) in small mono text to the left.
- **Progress Bars:** Segmented blocks rather than a smooth fill, resembling vintage signal strength meters.
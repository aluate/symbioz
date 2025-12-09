# Visual Style Guide: Symbioz

**Purpose**: Define consistent visual style for all Symbioz artwork and concept images.

---

## Global Art Style

**Base Style String** (use at the start of every prompt):

```
Cinematic sci-fi concept art, slightly painterly, 16:9 aspect ratio, moody lighting, mix of Mass Effect and KOTOR aesthetic, detailed but not photoreal, no cartoon style.
```

**Key Elements**:
- **Style**: Cinematic concept art (not game screenshots, not hyperreal)
- **Detail Level**: Mid-detail (enough to show character, not every pore)
- **Lighting**: Moody, dramatic (not flat or bright)
- **Aspect Ratio**: 16:9 (widescreen)
- **Inspiration**: Mass Effect + Knights of the Old Republic
- **Avoid**: Cartoon style, anime, photorealistic, low-poly game models

---

## Camera & Framing Defaults

### Characters (Races + Classes):
- **View**: 3/4 view or slight angle
- **Framing**: Thighs-up or full body
- **Stance**: Neutral "ready for action" or class-specific pose
- **Background**: Environment-appropriate (derelict station, outpost, etc.)

### Creatures/Beasts:
- **View**: Full body, slight low angle (makes them imposing)
- **Framing**: Full body in frame
- **Pose**: In motion or aggressive stance
- **Background**: Their natural habitat (abandoned outpost, den, etc.)

### Weapons:
- **View**: Side-on or 3/4 view
- **Framing**: Weapon centered, neutral background
- **Style**: Armory display or equipment sheet
- **Background**: Dark neutral (like an armory display case)

---

## Palette & Vibe

### Tech Spaces:
- **Colors**: Cool blues, ambers, metallic grays
- **Mood**: Industrial, functional, slightly worn
- **Lighting**: Harsh fluorescent or emergency lighting

### Frontier Worlds:
- **Colors**: Rusty oranges, browns, muted earth tones
- **Mood**: Weathered, lived-in, survival-focused
- **Lighting**: Natural light or firelight

### Honey/Amber:
- **Color**: Warm amber, golden glow
- **Contrast**: High contrast with dark tech (amber glows against dark metal)
- **Usage**: Inlays in weapons, vials, glowing effects

---

## Race Visual Specs

### Stonelock
- **Body Plan**: Short, broad, dense, heavy bone structure
- **Silhouette**: Compact, thick torso, big arms, slightly hunched, low center of gravity
- **Skin**: Rocky, scarred, muted earth tones (slate, rust, basalt)
- **Face**: Flat nose, deep-set eyes, heavy brow, short beard or stubble
- **Tech Style**: Industrial, welded plates, exposed bolts, practical gear
- **Vibe**: Unmoving, patient, working-class tough

### Aeshura
- **Body Plan**: Tall, lithe, agile, long limbs
- **Silhouette**: Narrow waist, long legs, slightly elongated neck
- **Skin**: Smooth, faint bioluminescent markings, cool palette (blue, violet)
- **Face**: Sharp features, angular jaw, glowing irises
- **Tech Style**: Sleek armor, minimalistic, integrated HUD elements
- **Vibe**: Precise, focused, calm under pressure

### Human
- **Body Plan**: Balanced, average build, versatile
- **Silhouette**: Standard humanoid proportions
- **Skin**: Varied (all skin tones)
- **Face**: Varied features
- **Tech Style**: Mix of styles, adaptable
- **Vibe**: Versatile, adaptable, jack-of-all-trades

---

## Class Visual Specs

### Vanguard
- **Armor Style**: Bulky chest plates, reinforced shoulders, visible scarring on armor
- **Weapon Style**: Heavy melee weapon or compact rifle, close-quarters gear
- **Stance**: Forward-leaning, weight on front foot, shielded or braced
- **Vibe**: Frontline, unyielding, brawler energy

### Operative
- **Armor Style**: Light tactical suit, cloak or hood, minimal noise
- **Weapon Style**: Precision rifle or twin pistols, suppressed weapons
- **Stance**: Sideways, ready to move, scanning targets
- **Vibe**: Stealthy, surgical, assassin energy

### Tech Specialist
- **Armor Style**: Light rig with tool belts, cables, visors, drone interfaces
- **Weapon Style**: Pistol or compact SMG, not front and center
- **Stance**: Slightly hunched over devices, one hand on a console or drone
- **Vibe**: Problem-solver, distracted genius

### Pioneer
- **Armor Style**: Rugged, weathered survival gear, packs, canisters, climbing harness
- **Weapon Style**: Carbine or survival rifle, machete/knife as backup
- **Stance**: Steady, aware of surroundings, one foot on a rock or root
- **Vibe**: Calm, grounded, wilderness first

---

## Weapon Visual Specs

### Basic Pistol
- **Shape**: Compact pistol, squared frame, integrated smart sight
- **Tech**: Semi-futuristic ballistic, glowing status lights, subtle Honey injector port
- **Finish**: Matte dark metal with worn edges
- **Vibe**: Trusted survival sidearm

### Basic Sword
- **Shape**: Broad, single-edged blade, slight curve
- **Tech**: Low-tech with optional vibro-core hints, metal with honey-amber inlay
- **Finish**: Brushed steel, visible use wear
- **Vibe**: Close-combat workhorse

---

## Creature Visual Specs

### Scavenger
- **Body**: Humanoid raider, lean and desperate, patchwork armor
- **Gear**: Cheap rifle or pistol, jury-rigged plate pieces, scavenged helmet
- **Environment**: Derelict station corridor, dim emergency lighting, exposed cables
- **Vibe**: Dangerous but not elite, opportunistic attacker

### Wild Beast
- **Body**: Four-legged alien predator, muscular, spined back, thick hide
- **Head**: Elongated snout, multiple eyes, bioluminescent saliva
- **Environment**: Abandoned outpost courtyard, broken crates and metal debris
- **Vibe**: Territorial, feral, brutal impact attacks

---

## Prompt Template

### Character Art Template:

```
Cinematic sci-fi concept art of a [RACE] [CLASS] from the Symbioz universe. [BODY_PLAN from race] with [SILHOUETTE from race], [SKIN], and [FACE]. They wear [ARMOR_STYLE from class] and carry [WEAPON_STYLE from class]. Pose: [STANCE from class]. Background: [ENVIRONMENT]. Visual style: [global art style from guide].
```

### Example (Stonelock Vanguard):

```
Cinematic sci-fi concept art of a Stonelock Vanguard from the Symbioz universe. A short, broad, dense humanoid with heavy bone structure and a compact, powerful silhouette, thick arms and a low center of gravity. Skin is rocky and scarred with muted slate and rust tones, a heavy brow and short stubble beard. They wear bulky chest plates with reinforced shoulders and scarred armor, industrial welded plates with exposed bolts and practical gear straps. They wield a broad single-edged sword with a slight curve and honey-amber inlays along the blade, held ready at their side. Pose: forward-leaning, weight on the front foot, ready to strike. Background: a derelict space station corridor, flickering emergency lights, exposed cables, scattered crates and debris. Visual style: cinematic sci-fi concept art, slightly painterly, 16:9, moody lighting, mix of Mass Effect and KOTOR, detailed but not photoreal.
```

---

## Usage Notes

- Always include the global style string at the end
- Combine race + class specs for character art
- Use environment descriptions from creature/weapon specs
- Keep descriptions concise but specific
- Focus on what makes each race/class visually distinct

---

**Next Steps**: Create YAML files for structured data, then build a prompt generation script.


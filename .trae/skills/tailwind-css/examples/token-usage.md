# Tailwind Design Token Usage

## Color Token Patterns

### Semantic Colors
```html
<!-- Use semantic tokens instead of hardcoded colors -->
<div class="bg-primary text-primary-foreground">
  Primary button
</div>

<div class="bg-secondary text-secondary-foreground">
  Secondary surface
</div>

<div class="bg-destructive text-destructive-foreground">
  Error state
</div>
```

### Background and Foreground Pairs
```html
<!-- Always pair background with foreground -->
<div class="bg-background text-foreground">
  Main content area
</div>

<div class="bg-card text-card-foreground">
  Card component
</div>

<div class="bg-popover text-popover-foreground">
  Popover/dropdown
</div>
```

## Typography Tokens

### Text Color Tokens
```html
<!-- Muted text for secondary information -->
<p class="text-muted-foreground">
  Secondary text information
</p>

<!-- Accent text for emphasis -->
<span class="text-accent-foreground">
  Important accent text
</span>
```

### Font Size Tokens
```html
<!-- Use consistent typography scale -->
<h1 class="text-4xl font-bold">Main Heading</h1>
<h2 class="text-3xl font-semibold">Secondary Heading</h2>
<h3 class="text-2xl font-medium">Tertiary Heading</h3>
<p class="text-base">Body text</p>
<small class="text-sm">Small text</small>
```

## Border and Ring Tokens

### Border Tokens
```html
<!-- Standard border -->
<div class="border border-border">
  Element with standard border
</div>

<!-- Input borders -->
<input class="border border-input focus:border-ring" />

<!-- Error borders -->
<div class="border border-destructive">
  Error state element
</div>
```

### Focus Ring Tokens
```html
<!-- Standard focus ring -->
<button class="focus:outline-none focus:ring-2 focus:ring-ring">
  Focusable button
</button>

<!-- Focus with offset -->
<input class="focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2" />
```

## Shadow Tokens

### Shadow Usage
```html
<!-- Card shadow -->
<div class="bg-card shadow shadow-sm">
  Card with subtle shadow
</div>

<!-- Modal shadow -->
<div class="bg-popover shadow-lg">
  Modal/popover content
</div>

<!-- No shadow for flat design -->
<div class="bg-background">
  Flat design element
</div>
```

## Theme-Aware Patterns

### Light/Dark Mode Tokens
```html
<!-- Theme-aware background -->
<div class="bg-background text-foreground">
  Adapts to light/dark mode
</div>

<!-- Theme-aware card -->
<div class="bg-card text-card-foreground border border-border">
  Card that works in both themes
</div>
```

### Accent Patterns
```html
<!-- Accent backgrounds -->
<div class="bg-accent text-accent-foreground">
  Accent element
</div>

<!-- Muted accents -->
<div class="bg-muted text-muted-foreground">
  Muted background element
</div>
```

## Common Token Combinations

### Card Pattern
```html
<div class="bg-card text-card-foreground rounded-lg border border-border shadow-sm">
  <div class="p-6">
    <h3 class="text-lg font-semibold">Card Title</h3>
    <p class="text-sm text-muted-foreground">Card description</p>
  </div>
</div>
```

### Button Pattern
```html
<button class="bg-primary text-primary-foreground hover:bg-primary/90">
  Primary Action
</button>

<button class="bg-secondary text-secondary-foreground hover:bg-secondary/90">
  Secondary Action
</button>
```

### Form Pattern
```html
<div class="space-y-2">
  <label class="text-sm font-medium">Label</label>
  <input class="border border-input bg-background rounded-md px-3 py-2" />
  <p class="text-sm text-muted-foreground">Helper text</p>
</div>
```
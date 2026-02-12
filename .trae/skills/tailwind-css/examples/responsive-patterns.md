# Tailwind Responsive Patterns

## Breakpoint Patterns

### Mobile-First Approach
```html
<!-- Stack on mobile, columns on desktop -->
<div class="flex flex-col md:flex-row gap-4">
  <div class="w-full md:w-1/2">Column 1</div>
  <div class="w-full md:w-1/2">Column 2</div>
</div>

<!-- Text size scaling -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">Responsive Heading</h1>
```

### Responsive Grid Patterns
```html
<!-- Auto-fit responsive grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>

<!-- Responsive sidebar layout -->
<div class="flex flex-col lg:flex-row gap-6">
  <aside class="w-full lg:w-64 flex-shrink-0">Sidebar</aside>
  <main class="flex-1">Main Content</main>
</div>
```

## Responsive Components

### Responsive Navigation
```html
<!-- Mobile menu button (hidden on desktop) -->
<button class="lg:hidden p-2">
  <svg><!-- hamburger icon --></svg>
</button>

<!-- Desktop navigation (hidden on mobile) -->
<nav class="hidden lg:flex lg:space-x-6">
  <a href="#">Home</a>
  <a href="#">About</a>
  <a href="#">Contact</a>
</nav>
```

### Responsive Cards
```html
<!-- Card that changes layout at medium breakpoint -->
<div class="flex flex-col md:flex-row gap-4 p-4">
  <img class="w-full md:w-48 h-48 md:h-auto object-cover" src="image.jpg" alt="">
  <div class="flex-1">
    <h3 class="text-xl md:text-2xl">Card Title</h3>
    <p class="text-sm md:text-base">Card content goes here</p>
  </div>
</div>
```

## Responsive Typography

### Text Scaling
```html
<!-- Responsive text sizing -->
<p class="text-sm md:text-base lg:text-lg">
  This text scales with screen size
</p>

<!-- Responsive heading hierarchy -->
<h1 class="text-3xl md:text-4xl lg:text-5xl xl:text-6xl">
  Main Heading
</h1>
<h2 class="text-2xl md:text-3xl lg:text-4xl">
  Secondary Heading
</h2>
```

### Line Length Control
```html
<!-- Optimal reading width -->
<div class="max-w-none md:max-w-3xl lg:max-w-4xl mx-auto">
  <p class="text-lg leading-relaxed">
    Content with controlled line length for optimal readability
  </p>
</div>
```

## Responsive Utilities

### Spacing Adjustments
```html
<!-- Responsive padding -->
<div class="p-4 md:p-6 lg:p-8">
  Content with responsive padding
</div>

<!-- Responsive gap -->
<div class="flex gap-2 md:gap-4 lg:gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Display Utilities
```html
<!-- Show/hide elements responsively -->
<div class="hidden md:block">
  Only visible on medium screens and up
</div>

<div class="md:hidden">
  Only visible on small screens
</div>

<div class="lg:inline-block hidden">
  Inline only on large screens
</div>
```

## Common Responsive Patterns

### Mobile-First Card Grid
```html
<!-- 1 column on mobile, 2 on tablet, 3 on desktop -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-white p-4 rounded shadow">
    <h3 class="text-lg font-semibold mb-2">Card Title</h3>
    <p class="text-sm text-gray-600">Card content</p>
  </div>
  <!-- More cards... -->
</div>
```

### Responsive Table
```html
<!-- Horizontal scroll on mobile, full table on desktop -->
<div class="overflow-x-auto">
  <table class="min-w-full">
    <thead>
      <tr class="border-b">
        <th class="text-left p-2 md:p-4">Name</th>
        <th class="text-left p-2 md:p-4 hidden sm:table-cell">Email</th>
        <th class="text-left p-2 md:p-4 hidden md:table-cell">Phone</th>
      </tr>
    </thead>
    <tbody>
      <!-- Table rows -->
    </tbody>
  </table>
</div>
```
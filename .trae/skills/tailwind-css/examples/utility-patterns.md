# Tailwind Utility Patterns

## Basic Utility Combinations

### Layout Utilities
```html
<!-- Flex container with spacing -->
<div class="flex items-center justify-between gap-2">
  <span>Label</span>
  <button>Action</button>
</div>

<!-- Grid with responsive columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Spacing Patterns
```html
<!-- Consistent spacing scale -->
<div class="p-4 space-y-4">
  <div class="p-2">Small padding</div>
  <div class="p-4">Medium padding</div>
  <div class="p-6">Large padding</div>
</div>

<!-- Margin utilities -->
<div class="mb-4">Bottom margin</div>
<div class="mt-4">Top margin</div>
<div class="mx-auto">Horizontal center</div>
```

## State Variants

### Interactive States
```html
<!-- Hover and focus states -->
<button class="bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
  Interactive Button
</button>

<!-- Disabled state -->
<button class="bg-gray-300 text-gray-500 cursor-not-allowed" disabled>
  Disabled Button
</button>
```

### Form States
```html
<!-- Input states -->
<input class="border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500" />

<!-- Error state -->
<input class="border border-red-500 focus:border-red-500 focus:ring-1 focus:ring-red-500" />

<!-- Success state -->
<input class="border border-green-500 focus:border-green-500 focus:ring-1 focus:ring-green-500" />
```

## Dark Mode Patterns

### Dark Mode Utilities
```html
<!-- Dark mode text -->
<p class="text-gray-900 dark:text-gray-100">Adaptive text</p>

<!-- Dark mode backgrounds -->
<div class="bg-white dark:bg-gray-800">Adaptive background</div>

<!-- Dark mode borders -->
<div class="border-gray-200 dark:border-gray-700">Adaptive border</div>
```

## Common Anti-Patterns to Avoid

### ❌ Inline Style Equivalents
```html
<!-- Don't do this -->
<div class="block w-full h-12 px-4 py-3 text-base">
  Too many utilities for simple styling
</div>

<!-- Do this instead -->
<div class="w-full p-3 text-base">
  Simplified utility combination
</div>
```

### ❌ Over-Specific Utilities
```html
<!-- Don't do this -->
<div class="mt-1 mt-2 mt-3 mt-4">
  Conflicting margins
</div>

<!-- Do this instead -->
<div class="mt-4">
  Single clear utility
</div>
```
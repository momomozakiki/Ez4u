# Tailwind Examples

## Utility Composition
```
<div class="flex items-center justify-between gap-2 p-4 bg-card text-card-foreground border border-border rounded-md">
  <span class="text-sm">Label</span>
  <button class="h-9 px-3 rounded-md bg-primary text-primary-foreground hover:bg-primary/90">
    Action
  </button>
</div>
```

## Responsive Grid
```
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-muted/50 rounded p-4">A</div>
  <div class="bg-muted/50 rounded p-4">B</div>
  <div class="bg-muted/50 rounded p-4">C</div>
  <div class="bg-muted/50 rounded p-4">D</div>
  <div class="bg-muted/50 rounded p-4">E</div>
  <div class="bg-muted/50 rounded p-4">F</div>
</div>
```

## Tokens Usage
```
<section class="bg-background text-foreground">
  <p class="text-muted-foreground">Muted text</p>
  <div class="border border-border rounded-md p-4">Bordered box</div>
</section>
```

## Button (variants + sizes)
```tsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

type Variant = 'primary' | 'secondary' | 'outline' | 'destructive';
type Size = 'sm' | 'md' | 'lg';

const variantMap: Record<Variant, string> = {
  primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/90',
  outline: 'border border-border bg-transparent hover:bg-accent hover:text-accent-foreground',
  destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
};

const sizeMap: Record<Size, string> = {
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4 text-sm',
  lg: 'h-12 px-6 text-base'
};

export function buttonClasses(variant: Variant, size: Size, disabled?: boolean) {
  return twMerge(
    clsx(
      'inline-flex items-center justify-center rounded-md transition-colors',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
      variantMap[variant],
      sizeMap[size],
      { 'opacity-50 cursor-not-allowed': disabled }
    )
  );
}
```

## Card
```tsx
export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-card text-card-foreground rounded-lg shadow border border-border p-4">
      {children}
    </div>
  );
}
```

## Input
```tsx
type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

export function Input(props: InputProps) {
  return (
    <input
      {...props}
      className={twMerge(
        'w-full px-3 py-2 rounded-md',
        'bg-background text-foreground',
        'border border-input focus:ring-2 focus:ring-ring',
        'placeholder:text-muted-foreground',
        props.className || ''
      )}
    />
  );
}
```

## Popover Trigger (state variants)
```tsx
export function TriggerButton({ active }: { active?: boolean }) {
  return (
    <button
      className={twMerge(
        'inline-flex items-center gap-2 rounded-md h-9 px-3',
        'bg-secondary text-secondary-foreground hover:bg-secondary/90',
        { 'ring-2 ring-ring': active }
      )}
    >
      Open
    </button>
  );
}
```

## Layout: Page Section
```tsx
export function Section({ children }: { children: React.ReactNode }) {
  return (
    <section className="max-w-7xl mx-auto p-6">
      {children}
    </section>
  );
}
```

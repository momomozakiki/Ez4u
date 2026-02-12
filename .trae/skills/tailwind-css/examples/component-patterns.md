# Tailwind Component Patterns

## Reusable Component Classes

### Button Component Pattern
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

### Card Component Pattern
```tsx
export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-card text-card-foreground rounded-lg shadow border border-border p-4">
      {children}
    </div>
  );
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col space-y-1.5 p-6">
      {children}
    </div>
  );
}

export function CardContent({ children }: { children: React.ReactNode }) {
  return (
    <div className="p-6 pt-0">
      {children}
    </div>
  );
}
```

### Input Component Pattern
```tsx
export function Input({ 
  className, 
  type = 'text',
  ...props 
}: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      type={type}
      className={twMerge(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2',
        'text-sm ring-offset-background file:border-0 file:bg-transparent',
        'file:text-sm file:font-medium placeholder:text-muted-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
        'focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    />
  );
}
```

## Composition Patterns

### Slot-Based Components
```tsx
// Alert component with slots
export function Alert({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground">
      {children}
    </div>
  );
}

export function AlertTitle({ children }: { children: React.ReactNode }) {
  return (
    <h5 className="mb-1 font-medium leading-none tracking-tight">
      {children}
    </h5>
  );
}

export function AlertDescription({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-sm [&_p]:leading-relaxed">
      {children}
    </div>
  );
}
```

### Polymorphic Components
```tsx
// Button that can render as different elements
type ButtonProps<T extends React.ElementType = 'button'> = {
  as?: T;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
} & React.ComponentPropsWithoutRef<T>;

export function Button<T extends React.ElementType = 'button'>(
  { as, variant = 'primary', size = 'md', className, ...props }: ButtonProps<T>,
  ref: React.ComponentPropsWithRef<T>['ref']
) {
  const Component = as || 'button';
  
  return (
    <Component
      className={twMerge(
        buttonClasses(variant, size),
        className
      )}
      ref={ref}
      {...props}
    />
  );
}
```

## Component Variants

### Badge Variants
```tsx
const badgeVariants = {
  default: 'bg-primary text-primary-foreground',
  secondary: 'bg-secondary text-secondary-foreground',
  destructive: 'bg-destructive text-destructive-foreground',
  outline: 'text-foreground border border-border'
};

export function Badge({ 
  variant = 'default', 
  children 
}: { 
  variant?: keyof typeof badgeVariants;
  children: React.ReactNode;
}) {
  return (
    <div className={twMerge(
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold',
      badgeVariants[variant]
    )}>
      {children}
    </div>
  );
}
```
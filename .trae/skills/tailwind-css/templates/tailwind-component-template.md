# Tailwind Component Template

```tsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

type Variant = 'primary' | 'secondary' | 'outline';

const variantMap: Record<Variant, string> = {
  primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/90',
  outline: 'border border-border bg-transparent hover:bg-accent hover:text-accent-foreground'
};

export function Component({
  variant = 'primary',
  className,
  children
}: {
  variant?: Variant;
  className?: string;
  children: React.ReactNode;
}) {
  const base = 'inline-flex items-center justify-center h-9 px-3 rounded-md';
  return (
    <button className={twMerge(clsx(base, variantMap[variant], className))}>
      {children}
    </button>
  );
}
```

# Styling Pattern Detection Examples

## Tailwind Primitives Preservation

### Scenario: Adding variant support while preserving Tailwind pattern
```tsx
// BEFORE - Existing component using Tailwind primitives
const Button = ({ children }) => (
  <button className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">
    {children}
  </button>
)

// AFTER - Additive change preserving Tailwind pattern
const Button = ({ children, variant = 'primary' }) => (
  <button className={`bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded ${variantClasses[variant]}`}>
    {children}
  </button>
)
```

**Detection Points:**
- ✅ Uses Tailwind utility classes only
- ✅ No custom CSS files or styled-components
- ✅ Follows Tailwind hover/focus state patterns
- ✅ Preserves existing color scheme

## Custom CSS Preservation

### Scenario: Extending functionality while preserving custom CSS
```tsx
// BEFORE - Existing component using custom CSS
const Card = () => <div className="custom-card">...</div>

// AFTER - Preserve custom CSS, extend functionality
const Card = ({ children, title }) => (
  <div className="custom-card">
    {title && <h2 className="custom-card-title">{title}</h2>}
    {children}
  </div>
)
```

**Detection Points:**
- ✅ Uses project-specific CSS classes
- ✅ References external CSS files
- ✅ Follows BEM or similar naming conventions
- ✅ Maintains existing styling architecture

## Pattern Recognition Checklist

When analyzing styling patterns, check:
1. **File imports**: Look for CSS imports vs Tailwind usage
2. **Class naming**: Utility classes vs semantic/custom classes
3. **State handling**: Tailwind states vs custom pseudo-classes
4. **Responsive design**: Tailwind breakpoints vs custom media queries
5. **Theme system**: Tailwind config vs CSS custom properties

**Decision Matrix:**
| Pattern Found | Preservation Approach |
|---------------|----------------------|
| Tailwind utilities only | Extend with more utilities |
| Custom CSS classes | Maintain CSS architecture |
| Mixed patterns | Preserve dominant pattern |
| CSS-in-JS | Keep styled-components/emotion |
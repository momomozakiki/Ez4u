# Design Preservation Examples

## Example 1: Styling Pattern Detection

### Tailwind Primitives Preservation
```tsx
// BEFORE - Existing component using Tailwind primitives
const Button = ({ children }) => <button className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">{children}</button>

// AFTER - Additive change preserving pattern
const Button = ({ children, variant = 'primary' }) => (
  <button className={`bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded ${variantClasses[variant]}`}>
    {children}
  </button>
)
```

### Custom CSS Preservation
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

## Example 2: Component Pattern Detection

### Props API Preservation
```tsx
// BEFORE - Existing API
const FormInput = ({ name, value, onChange, label }) => (
  <div>
    <label>{label}</label>
    <input name={name} value={value} onChange={onChange} />
  </div>
)

// AFTER - Additive change preserving API
const FormInput = ({ name, value, onChange, label, error, helperText }) => (
  <div>
    <label>{label}</label>
    <input name={name} value={value} onChange={onChange} className={error ? 'error' : ''} />
    {helperText && <small>{helperText}</small>}
    {error && <span className="error-message">{error}</span>}
  </div>
)
```

## Example 3: Destructive Change Warning

### Pattern Replacement (Requires Confirmation)
```tsx
// BEFORE - Custom CSS pattern
const Modal = () => <div className="custom-modal-overlay">...</div>

// AFTER - Would replace with Tailwind (REQUIRES CONFIRMATION)
const Modal = () => <div className="fixed inset-0 bg-black bg-opacity-50">...</div>

// Output:
// [DESTRUCTIVE CHANGE WARNING] This replaces custom CSS pattern (used in 8 components)
// Confirm: "Yes, replace existing pattern" to proceed.
```

## Example 4: Verification Template Output

```
[PRESERVATION VERIFIED]
✓ Existing pattern preserved: Tailwind primitives with hover states
✓ Naming conventions matched: PascalCase components, kebab-case files
✓ Dependencies unaffected: 0 breaking changes
✓ Additive change only: New 'icon' prop added, existing API preserved
```

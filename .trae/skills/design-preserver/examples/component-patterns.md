# Component Pattern Detection Examples

## Props API Preservation

### Scenario: Adding error handling while preserving existing API
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

**Detection Points:**
- ✅ All original props remain unchanged
- ✅ New props are optional with defaults
- ✅ No breaking changes to prop types
- ✅ Existing consumers continue working

## Composition Pattern Preservation

### Scenario: Preserving clsx composition pattern
```tsx
// BEFORE - Existing clsx pattern
const Button = ({ children, variant, size }) => {
  const classes = clsx(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size]
  )
  return <button className={classes}>{children}</button>
}

// AFTER - Preserve clsx pattern, add icon support
const Button = ({ children, variant, size, icon, iconPosition = 'left' }) => {
  const classes = clsx(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    icon && iconSpacingClasses[iconPosition]
  )
  return (
    <button className={classes}>
      {icon && iconPosition === 'left' && <span className="icon-left">{icon}</span>}
      {children}
      {icon && iconPosition === 'right' && <span className="icon-right">{icon}</span>}
    </button>
  )
}
```

## Naming Convention Preservation

### Scenario: Maintaining existing naming patterns
```tsx
// BEFORE - PascalCase components, kebab-case files
// File: user-profile-card.tsx
const UserProfileCard = ({ user }) => { ... }

// AFTER - Preserve naming conventions
// File: user-profile-card-with-stats.tsx
const UserProfileCardWithStats = ({ user, showStats = false }) => { ... }
```

**Detection Points:**
- ✅ Component names: PascalCase
- ✅ File names: kebab-case
- ✅ Props: camelCase
- ✅ CSS classes: kebab-case or BEM

## Pattern Recognition Checklist

When analyzing component patterns, check:
1. **Props interface**: Required vs optional props
2. **Composition method**: clsx, classNames, or string concatenation
3. **State management**: Props vs hooks vs context
4. **Event handling**: Callback patterns and signatures
5. **File organization**: Feature-based vs type-based structure
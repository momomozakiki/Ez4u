# Destructive Change Warning Examples

## Pattern Replacement Scenarios

### Scenario: Replacing Custom CSS with Tailwind
```tsx
// BEFORE - Custom CSS pattern (used in 8 components)
const Modal = () => <div className="custom-modal-overlay">...</div>

// AFTER - Would replace with Tailwind (REQUIRES CONFIRMATION)
const Modal = () => <div className="fixed inset-0 bg-black bg-opacity-50">...</div>

// Output:
[DESTRUCTIVE CHANGE WARNING] This replaces custom CSS pattern (used in 8 components)
Confirm: "Yes, replace existing pattern" to proceed.
```

### Scenario: Breaking Props API Changes
```tsx
// BEFORE - Existing API (used by 12 consumers)
const Button = ({ children, variant, onClick }) => { ... }

// AFTER - Would remove onClick prop (REQUIRES CONFIRMATION)
const Button = ({ children, variant, onPress }) => { ... }

// Output:
[DESTRUCTIVE CHANGE WARNING] This removes onClick prop (breaking 12 consumers)
Confirm: "Yes, break existing API" to proceed.
```

### Scenario: Replacing State Management Pattern
```tsx
// BEFORE - Context-based state (used in 5 features)
const UserProvider = ({ children }) => {
  const [user, setUser] = useContext(UserContext)
  return children
}

// AFTER - Would replace with Redux (REQUIRES CONFIRMATION)
const UserProvider = ({ children }) => {
  const user = useSelector(state => state.user)
  return children
}

// Output:
[DESTRUCTIVE CHANGE WARNING] This replaces Context pattern with Redux (affects 5 features)
Confirm: "Yes, replace state management" to proceed.
```

## When Destructive Changes Are Justified

1. **Performance Issues**: Current pattern causes measurable performance problems
2. **Security Vulnerabilities**: Existing pattern has security flaws
3. **Maintenance Burden**: Current pattern is unmaintainable or deprecated
4. **Team Consensus**: Team has agreed on pattern migration strategy
5. **Major Version Release**: Breaking changes acceptable in major version

## Destructive Change Decision Matrix

| Change Type | Impact | Justification Required |
|-------------|--------|------------------------|
| Styling replacement | Affects all components | Team consensus + migration plan |
| Props API breaking | Affects all consumers | Major version + deprecation notice |
| State management | Affects entire app | Performance/security justification |
| File structure | Affects imports | Team agreement + automated migration |

## Approval Process

1. **Document impact**: List all affected files/components
2. **Provide justification**: Explain why destructive change is necessary
3. **Offer migration path**: Show how existing code will be updated
4. **Get explicit confirmation**: Require typed confirmation from user
5. **Plan rollback strategy**: Ensure change can be reverted if issues arise
# Common Design Patterns Reference

## Styling Patterns
- **Tailwind Primitives**: `bg-blue-500`, `p-4`, `rounded-lg`
- **Custom CSS Classes**: `custom-button`, `app-header`
- **CSS-in-JS**: `styled-components`, `emotion`
- **CSS Modules**: `styles.module.css`

## Component Patterns
- **Props-based**: All configuration via props
- **Context-based**: State management via React Context
- **Render Props**: Components that take functions as children
- **Compound Components**: Multiple components working together (e.g., `<Select>` and `<Select.Option>`)

## File Organization Patterns
- **Feature-based**: `src/features/auth/`
- **Type-based**: `src/components/`, `src/hooks/`, `src/utils/`
- **Domain-based**: `src/domains/user/`, `src/domains/products/`

## Naming Conventions
- **Components**: PascalCase (e.g., `UserProfile`, `ProductCard`)
- **Files**: kebab-case (e.g., `user-profile.tsx`, `product-card.tsx`)
- **Functions**: camelCase (e.g., `getUserData`, `calculateTotal`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_URL`, `MAX_ITEMS`)

# Accessibility (a11y) Compliance Standards

**Project:** TechGear Checkout Module  
**Target Standard:** WCAG 2.1 Level AA

---

## 1. Focus Management

### Visual Focus
- All interactive elements (buttons, inputs, radio buttons) must display a visible focus ring when navigated via keyboard (Tab key).
- **Requirement:** Use a 2px solid blue outline or a distinct shadow.

### Logical Order
Tabbing must follow the visual layout:

1. Product List (Add to Cart buttons)  
2. Cart Summary (Quantity inputs)  
3. Discount Field  
4. Checkout Form:
   - Name  
   - Email  
   - Address  
   - Shipping  
   - Payment  
   - Submit  

---

## 2. Screen Reader Support (ARIA)

### Icons
- Decorative icons must include `aria-hidden="true"`.

### Input Labels
- All form inputs must be programmatically associated with visible labels.
- **Technique:** `<label for="input-id">` paired with `<input id="input-id">`.

### Dynamic Content
- Success message containers must use `role="alert"` or `aria-live="polite"`.
- Error messages must be linked to inputs via `aria-describedby`.

---

## 3. Semantic Structure

### Headings
- Page title **TechGear Checkout** must be an `<h1>`.
- Section titles (e.g., *Available Products*, *Your Cart*) should be `<h2>`.

### Buttons vs Links
- Actions that submit data (e.g., **Pay Now**, **Apply Coupon**) must use `<button>` elements.
- Avoid clickable `<a>` or `<div>` for actions that are not navigation.

---

## 4. Color Contrast

- Body text contrast ratio: **≥ 4.5:1**
- Error text: Ensure red `#dc2626` maintains readable contrast on white.

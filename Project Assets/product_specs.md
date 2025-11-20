# Product Specification: E-Shop Checkout Logic
**Version:** 1.2  
**Last Updated:** 2023-10-25

## 1. Product Inventory & Pricing
The following products are available in the system. Prices are fixed and defined in USD.

| Product ID | Product Name        | Unit Price ($) |
|------------|----------------------|-----------------|
| 1          | Mechanical Keyboard  | 120.00          |
| 2          | Wireless Mouse       | 45.00           |
| 3          | USB-C Hub            | 30.00           |

## 2. Cart Mechanics
- **Quantity Limits:** A user cannot add more than 10 units of a single product type to the cart.
- **Persistence:** Cart data is currently session-based and clears on page refresh (MVP scope).
- **Empty Cart:** Users cannot proceed to checkout if the cart subtotal is $0.00.

## 3. Discount Codes
The system supports the following coupon codes. Codes are case-sensitive.

| Code     | Effect                               | Conditions |
|----------|----------------------------------------|------------|
| SAVE15   | Applies a 15% discount to the Subtotal | None       |
| FREESHIP | Sets Shipping Cost to $0.00            | None       |

**Note:** Only one discount code can be applied at a time. Applying a new code overwrites the previous one.

## 4. Shipping Logic
**Standard Shipping:**
- Cost: **$0.00** (Free)
- Delivery: 5-7 Business Days

**Express Shipping:**
- Cost: **$10.00** Flat Rate
- Delivery: 1-2 Business Days

## 5. Payment Processing
- Supported methods: **Credit Card**, **PayPal**.
- No actual payment gateway integration is active in the current build; clicking **"Pay Now"** only simulates a transaction delay (1.5s).


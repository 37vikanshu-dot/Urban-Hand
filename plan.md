# Urban Hand - Local Service Connection Platform

## Project Overview
A local service connection platform connecting nearby customers and service providers (plumbers, electricians, tailors, tutors, photographers, tiffin services, etc.) in small towns and cities.

**Brand Colors**: Teal & White
**Tech Stack**: Reflex, Firebase (Firestore, Auth, Storage), Google Maps API

---

## Phase 1: Home Page & Core Layout ✅
**Goal**: Create the main landing page with search, categories, and featured providers sections

- [x] Set up app structure with navigation header (logo, search bar, user menu)
- [x] Design home page hero section with tagline "Connecting Local Hands to Local Needs"
- [x] Create service category grid with icons (Electrician ⚡, Plumber 💧, Tailor 👕, Carpenter 🪚, Tiffin 🍱, Tutor 📘, Photographer 📷, Others)
- [x] Build "Featured Providers" carousel component for paid listings
- [x] Add "Top Rated Near You" section with provider cards
- [x] Implement responsive layout with teal/white theme and rounded corners

---

## Phase 2: Search, Listings & Business Detail Pages ✅
**Goal**: Build search functionality, listing cards, and detailed business profiles

- [x] Create search & filter page with category, distance, rating, and "Open Now" filters
- [x] Design provider card component (photo, name, location, WhatsApp/call buttons, rating stars)
- [x] Build business detail page with full profile information
- [x] Add interactive elements: "Call Now", "Chat on WhatsApp", "View Location on Map", "Share Profile" buttons
- [x] Implement state management for filtering and navigation
- [x] Add "🌟 Featured Business" badge for paid listings

---

## Phase 3: Service Provider Registration & Admin Panel ✅
**Goal**: Enable service providers to register and create admin dashboard for management

- [x] Create "Get Listed" page with registration form (name, business name, category, contact, address, description, photo upload)
- [x] Display pricing plans (Basic Free, Featured ₹199/month, Premium Partner ₹499/3 months) with feature comparison
- [x] Add UPI payment section with QR code and screenshot upload
- [x] Implement form state management and submission workflow
- [x] Add conditional rendering for payment section based on selected plan
- [x] Create success modal for application submission

---

## Phase 4: Firebase Integration & Full Admin Control Panel ✅
**Goal**: Integrate Firebase backend and build comprehensive admin panel with full app customization

### Firebase Setup & Authentication ✅
- [x] Set up Firebase configuration (Firestore, Auth, Storage)
- [x] Implement admin authentication (email/password login)
- [x] Create secure admin-only routes with authentication guards
- [x] Create Firebase service module with get/save functions
- [x] Add graceful fallback when Firebase not configured

### Admin Dashboard Structure ✅
- [x] Build admin dashboard home with sidebar navigation
- [x] Create navigation menu: App Settings, Categories, Listings, Payments, Reviews
- [x] Add logout functionality
- [x] Implement page routing within admin panel

### Admin Panel - App Settings & Customization ✅
- [x] **Text Content Management**: Admin can edit all app text
  - Hero section title and subtitle
  - Button labels (Get Listed text)
  - App name in header
  - Store all text in Firestore `app_settings` collection
  - Settings apply in real-time to main app ✅ (Verified working!)
- [x] **Branding Management**:
  - Color picker for accent/primary colors
  - Settings save to Firestore
  - Changes reflect immediately on frontend ✅ (Verified working!)

### Admin Panel - Category Management ✅
- [x] **Browse Categories Control**:
  - View all service categories in editable table with icon/name/status/actions columns
  - Add new categories with name and icon picker (18 Lucide icons available)
  - Edit existing category names and icons via modal
  - Delete categories with confirmation dialog
  - Reorder categories with up/down arrow buttons
  - Enable/disable categories toggle (hide without deleting)
  - Store in Firestore `app_settings.service_categories` collection
  - Changes reflect immediately on main app home page and search filters
- [x] **Category Management State**:
  - AdminCategoriesState with full CRUD operations
  - load_categories, save_categories, add, edit, delete, move, toggle methods
  - Modal state management for add/edit workflows
  - Delete confirmation dialog state
- [x] **UI Components**:
  - Category table with icon preview, name, status badges, action buttons
  - "Add New Category" button with modal form
  - Icon picker grid (18 common Lucide icons)
  - Enable/disable checkbox in modal
  - Up/down reorder buttons
  - Edit pencil and delete trash buttons
  - Delete confirmation dialog

### Admin Panel - Listing Management ✅
- [x] **View All Listings Dashboard**:
  - Beautiful table layout with all business listings
  - Columns: Image (avatar), Name, Category, Location, Actions
  - Featured badge displayed for premium listings (yellow star icon)
  - Search by name or location with real-time filtering
  - Filter by category dropdown (All Categories + each service category)
  - Clean, responsive design with hover effects
  - Empty state with search-x icon when no results found
- [x] **Add New Listing**:
  - "Add New Listing" button opens modal form
  - Full form with all fields: Business Name, Category (dropdown from active categories), Address, Image URL
  - Featured listing toggle checkbox
  - Modal opens with open_add_modal() event handler
  - Form state managed in AdminListingsState
- [x] **Edit Existing Listings**:
  - Edit button (pencil icon) on each row
  - Opens modal pre-filled with listing data
  - Can modify all fields: name, category, address, image, featured status
  - Modal state managed with modal_is_editing flag
  - open_edit_modal(listing) event handler
- [x] **Delete Listings**:
  - Delete button (trash icon) on each row
  - Confirmation dialog before deletion
  - open_delete_confirm(listing_id) and confirm_delete_listing() handlers
  - Removes from both AdminListingsState.all_listings and UIState.providers
- [x] **State Management**:
  - AdminListingsState with full CRUD operations
  - Fields: search_query, category_filter, all_listings list
  - Modal fields: modal_business_name, modal_category, modal_address, modal_image_url, modal_featured
  - Delete confirmation: show_delete_confirm, listing_to_delete_id
  - Event handlers: load_listings, save_listing, open_add_modal, open_edit_modal, close_listing_modal, delete_listing
  - Computed var: filtered_listings (search + category filter)
- [x] **Integration**:
  - Loads listings from UIState.providers on mount
  - Syncs changes back to UIState.providers for frontend display
  - Featured status controls whether listing shows in "Featured Providers" section
  - Category filter populated from AdminCategoriesState.service_categories
  - Real-time search and filtering

---

## Phase 5: Payment Plan Management & Verification System 🔄 (IN PROGRESS)
**Goal**: Build comprehensive payment plan management and payment verification workflow

### Payment Plans Configuration
- [ ] **View/Edit Pricing Plans Page**:
  - Display all pricing tiers in editable table (Basic, Featured, Premium Partner)
  - Each plan shows: name, price, duration, feature list, status (Active/Inactive)
  - "Add New Plan" button to create custom plans
  - Edit button for each plan opens modal with all fields
  - Delete plan with confirmation dialog
  - Enable/disable plans (hide from "Get Listed" page without deleting)
- [ ] **Plan Editor Modal**:
  - Plan name input field
  - Price input (₹) with currency format
  - Duration dropdown (Free, Monthly, 3 Months, 6 Months, Yearly)
  - Feature list manager (add/remove/reorder features)
  - Active/Inactive toggle
  - Save/Cancel buttons
- [ ] **Payment Method Configuration**:
  - Edit UPI ID for payments (e.g., urbanhand@upi)
  - Upload/change QR code image via file upload
  - Add multiple payment options (UPI, Bank Transfer, Card - future)
  - Set custom payment instructions text
  - Configure automated payment reminder settings
- [ ] **Pricing Plans State**:
  - AdminPaymentPlansState with plan management
  - Fields: pricing_plans list, show_plan_modal, modal_plan_data
  - Methods: load_plans, save_plan, delete_plan, toggle_plan_status
  - Payment config fields: upi_id, qr_code_url, payment_instructions

### Payment Verification Workflow
- [ ] **Pending Payments Dashboard**:
  - View all pending payment submissions in table
  - Columns: Applicant Name, Business Name, Plan Selected, Amount, Screenshot Preview, Submit Date, Actions
  - Filter by plan type (Featured/Premium)
  - Sort by date submitted
  - Status badges: Pending, Approved, Rejected
- [ ] **Payment Review Interface**:
  - Click submission row to open detailed review modal
  - Display full applicant details (name, business, category, contact)
  - Show enlarged payment screenshot with zoom capability
  - Plan details (selected plan, price, duration)
  - Admin actions: Approve, Reject, Request Re-upload buttons
  - Add notes/comments field for rejection reason
- [ ] **Payment Approval Actions**:
  - Approve button → Activates paid plan for listing
  - Update listing status to Featured/Premium
  - Set plan expiration date automatically
  - Send confirmation notification/email to provider
  - Move submission to "Approved" archive
- [ ] **Payment History & Revenue Reports**:
  - View all approved payments with date, plan, amount
  - Total revenue calculation by time period (month/year)
  - Export payment history as CSV
  - Revenue analytics charts (monthly income, plan distribution)
- [ ] **Payment Verification State**:
  - AdminPaymentVerificationState for verification workflow
  - Fields: pending_payments, payment_history, show_review_modal, selected_payment
  - Methods: load_pending_payments, approve_payment, reject_payment, request_reupload
  - Integration with AdminListingsState to update listing plan status

---

## Phase 6: Google Maps Integration & Advanced Features (Upcoming)
**Goal**: Add location services, rating system, and user interaction features

- [ ] Integrate Google Maps API for "View Location on Map" feature
- [ ] Implement location-based search with distance filtering
- [ ] Add map view on business detail pages
- [ ] Build rating and review submission system:
  - Star rating (1-5) with half-star support
  - Text review with character limit
  - User authentication for reviews (prevent spam)
  - Display reviews on business detail page
  - Sort reviews by date/rating
- [ ] Implement "Open Now" business hours system:
  - Admin/provider sets business hours
  - Automatic "Open Now" badge display
  - Filter by open/closed status
- [ ] Add search suggestions and autocomplete
- [ ] Create city/area-based filtering
- [ ] Implement share profile functionality (WhatsApp, Facebook, copy link)

---

## Phase 7: Multi-language Support & Polish (Upcoming)
**Goal**: Add Hindi language support and final refinements

- [ ] Implement multi-language system (English + Hindi toggle)
- [ ] Translate all UI text to Hindi
- [ ] Store language preference in user session
- [ ] Admin can edit translations for both languages
- [ ] Add loading states and skeleton loaders
- [ ] Implement comprehensive error handling
- [ ] Optimize image loading with lazy loading and caching
- [ ] Add image compression for uploaded photos
- [ ] Create promotional banner ad management (admin can add/remove banners)
- [ ] Test responsive design across all device sizes
- [ ] Add accessibility features (ARIA labels, keyboard navigation)

---

## Phase 8: Testing, Optimization & Launch (Upcoming)
**Goal**: Final testing, performance optimization, and production deployment

- [ ] End-to-end testing of all user flows
- [ ] Performance optimization (bundle size, load times)
- [ ] Security audit (Firebase rules, input validation)
- [ ] SEO optimization (meta tags, sitemap)
- [ ] Set up production Firebase project
- [ ] Configure custom domain
- [ ] Deploy to production
- [ ] Set up monitoring and analytics
- [ ] Create user documentation
- [ ] Plan marketing and launch strategy

---

## Notes
- **Admin has full control**: Can change any text, logo, categories, listings, payment plans, and payment methods
- **Real-time updates**: Changes in admin panel reflect immediately on frontend ✅ (Verified working!)
- **Manual payment verification**: Admin reviews UPI screenshots before activating paid plans
- **Focus on simplicity**: Easy-to-use admin interface with no technical knowledge required
- **Scalable architecture**: Firestore structure supports growth and new features
- **Firebase Setup**: To connect Firebase, add `serviceAccountKey.json` file to project root (download from Firebase Console > Project Settings > Service Accounts)

---

## Current Status
**Phase 5 Starting**: 🔄 Payment Plan Management & Verification System

**Completed:**
- ✅ Phase 1-4: Full admin panel with settings, categories, and listings management
- ✅ Admin authentication system
- ✅ Real-time state synchronization between admin and main app

**Currently Implementing:**
- 🔄 Payment plans configuration page (view/edit pricing tiers)
- 🔄 Payment verification workflow (approve/reject submissions)
- 🔄 Revenue reporting and analytics

**Next After This Phase:** Google Maps integration and rating/review system
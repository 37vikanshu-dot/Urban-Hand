# Urban Hand - Complete Supabase Control & Analytics Setup

## 🎯 CURRENT MISSION: Full Supabase Setup for Complete App Control

### ✅ What You Already Have (Working)
- Supabase connected with URL and KEY ✅
- Tables: `app_settings`, `providers`, `pricing_plans`, `payment_submissions` ✅
- Admin panel with full control over content, categories, listings ✅
- Real-time sync between admin changes and main website ✅

### 🚀 What We Need to Add (Phase 5 - Analytics & Tracking)

---

## 📊 STEP 1: CREATE SUPABASE ANALYTICS TABLES

### Table 1: `user_analytics` - Track Every User Interaction
```sql
CREATE TABLE user_analytics (
  id BIGSERIAL PRIMARY KEY,
  event_type TEXT NOT NULL,  -- 'search', 'view_listing', 'click_call', 'click_whatsapp', 'share', 'view_location'
  provider_id INTEGER,  -- Which business was interacted with
  category TEXT,  -- Which category was searched
  search_query TEXT,  -- What the user searched for
  user_ip TEXT,  -- Anonymized user IP
  user_city TEXT,  -- User's location
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  metadata JSONB  -- {device_type, browser, referrer, filters_used}
);

-- Indexes for fast queries
CREATE INDEX idx_analytics_event_type ON user_analytics(event_type);
CREATE INDEX idx_analytics_provider_id ON user_analytics(provider_id);
CREATE INDEX idx_analytics_timestamp ON user_analytics(timestamp DESC);
CREATE INDEX idx_analytics_category ON user_analytics(category);
```

### Table 2: `business_analytics` - Aggregated Metrics Per Business
```sql
CREATE TABLE business_analytics (
  provider_id INTEGER PRIMARY KEY,
  total_views INTEGER DEFAULT 0,
  total_calls INTEGER DEFAULT 0,
  total_whatsapp INTEGER DEFAULT 0,
  total_shares INTEGER DEFAULT 0,
  last_viewed TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Table 3: `reviews` - Customer Reviews & Ratings
```sql
CREATE TABLE reviews (
  id BIGSERIAL PRIMARY KEY,
  provider_id INTEGER NOT NULL,
  user_name TEXT NOT NULL,
  rating NUMERIC(2,1) CHECK (rating >= 1 AND rating <= 5),  -- 1.0 to 5.0
  review_text TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  status TEXT DEFAULT 'pending'  -- 'pending', 'approved', 'flagged'
);

CREATE INDEX idx_reviews_provider_id ON reviews(provider_id);
CREATE INDEX idx_reviews_status ON reviews(status);
```

---

## 🔒 STEP 2: SETUP ROW LEVEL SECURITY (RLS) POLICIES

### For `user_analytics` table:
```sql
-- Enable RLS
ALTER TABLE user_analytics ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can insert analytics events
CREATE POLICY "Allow public insert" ON user_analytics
  FOR INSERT WITH CHECK (true);

-- Policy: Only admin can read analytics
CREATE POLICY "Admin read only" ON user_analytics
  FOR SELECT USING (false);  -- Update this when you add admin auth
```

### For `business_analytics` table:
```sql
ALTER TABLE business_analytics ENABLE ROW LEVEL SECURITY;

-- Public can read aggregated stats
CREATE POLICY "Public can view stats" ON business_analytics
  FOR SELECT USING (true);

-- Only app can update
CREATE POLICY "App can update" ON business_analytics
  FOR UPDATE USING (true);
```

### For `reviews` table:
```sql
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- Public can view approved reviews
CREATE POLICY "Public view approved" ON reviews
  FOR SELECT USING (status = 'approved');

-- Anyone can submit review
CREATE POLICY "Public can submit" ON reviews
  FOR INSERT WITH CHECK (true);
```

---

## 📦 STEP 3: CREATE SUPABASE STORAGE BUCKETS

Go to Supabase Dashboard → Storage → Create buckets:

1. **`business-photos`** - For provider uploaded images
   - Public bucket: ✅
   - File size limit: 5MB
   - Allowed types: image/jpeg, image/png, image/webp

2. **`payment-screenshots`** - For UPI payment proof uploads
   - Public bucket: ❌ (Admin only)
   - File size limit: 3MB
   - Allowed types: image/jpeg, image/png

3. **`qr-codes`** - For payment QR code images
   - Public bucket: ✅
   - File size limit: 1MB
   - Allowed types: image/png, image/svg+xml

---

## 📈 STEP 4: IMPLEMENT TRACKING IN APP CODE

### Task 4.1: Create Analytics State Module ✅
- [x] Create `app/states/analytics_state.py`
- [x] Add event tracking methods: `track_search()`, `track_view()`, `track_call()`, `track_whatsapp()`, `track_share()`
- [x] Batch updates to reduce database calls
- [x] Error handling (tracking failures don't break user experience)

### Task 4.2: Add Tracking to UI Components
- [ ] **Home Page**: Track category clicks, hero search
- [ ] **Search Page**: Track every search query with filters used
- [ ] **Business Detail Page**: 
  - Track page view when opened
  - Track "Call Now" button clicks
  - Track "WhatsApp" button clicks
  - Track "Share Profile" clicks
  - Track "View Location" clicks
- [ ] **Listings Cards**: Track card clicks (leads to detail page)

### Task 4.3: Create Analytics Service
- [ ] Create `app/services/analytics_service.py`
- [ ] Add functions: `log_event()`, `update_business_stats()`, `get_analytics_data()`
- [ ] Use background tasks for non-blocking inserts

---

## 📊 STEP 5: BUILD ADMIN ANALYTICS DASHBOARD

### Task 5.1: Create Analytics Overview Page
- [ ] Add "Analytics" menu item to admin sidebar
- [ ] Create `AdminAnalyticsState` with data loading
- [ ] Show key metrics cards:
  - 📊 Total Searches (today, week, month)
  - 👁️ Total Views (today, week, month)
  - 📞 Total Calls (today, week, month)
  - 💬 Total WhatsApp Clicks (today, week, month)
  - 🔄 Conversion Rate (views → contact actions)
  - 💰 Total Revenue
  - 📝 Total Listings (approved/pending/rejected)
  - ⭐ Featured Listings Count

### Task 5.2: Add Analytics Charts
- [ ] **Line Chart**: Searches per day (last 30 days)
- [ ] **Bar Chart**: Top 10 most viewed businesses
- [ ] **Pie Chart**: Searches by category distribution
- [ ] **Bar Chart**: Revenue by plan type (Basic, Featured, Premium)
- [ ] **Line Chart**: New listings per week
- [ ] **Bar Chart**: Contact actions by day (Calls vs WhatsApp)

### Task 5.3: Add Performance Tables
- [ ] **Top Performing Businesses Table**:
  - Columns: Rank, Business Name, Views, Calls, WhatsApp, Conversion Rate
  - Sort by views, calls, or conversion rate
  - Filter by date range
- [ ] **Recent Searches Table**:
  - Columns: Timestamp, Search Query, Category, Results Count
  - Show last 100 searches
  - Filter by category
- [ ] **Traffic Sources** (future):
  - Show referrer breakdown (Google, Facebook, Direct, etc.)

### Task 5.4: Export & Reports
- [ ] Add CSV export button for analytics data
- [ ] Date range selector (today, week, month, custom)
- [ ] Export business performance report
- [ ] Export revenue report with payment details

---

## 💳 STEP 6: COMPLETE PAYMENT MANAGEMENT SYSTEM

### Task 6.1: Payment Plan Editor (Already in code, needs testing)
- [x] View all pricing plans
- [x] Add/Edit/Delete plans
- [x] Configure: name, price, duration, features list
- [x] Enable/disable plans

### Task 6.2: Payment Configuration Page
- [ ] Edit UPI ID (currently hardcoded as `urbanhand@upi`)
- [ ] Upload QR Code to Supabase Storage
- [ ] Display current QR code preview
- [ ] Edit payment instructions text
- [ ] Save to `app_settings` table under `payment_config` key

### Task 6.3: Payment Submissions Dashboard (Enhanced)
- [x] View all pending submissions
- [ ] Enhanced table with:
  - Applicant Name, Business Name
  - Plan Selected, Amount
  - **Screenshot Preview** (thumbnail, click to enlarge)
  - Submit Date, Status badge
  - Actions: Review, Approve, Reject
- [ ] Filter by: Status (Pending/Approved/Rejected), Plan Type
- [ ] Sort by: Date submitted (newest first)

### Task 6.4: Payment Review & Approval Flow
- [ ] **Review Modal**:
  - Show full applicant details
  - Display enlarged payment screenshot (zoomable)
  - Plan details (price, duration, features)
  - Approve/Reject buttons
  - Add notes/comments field
- [ ] **Approve Action**:
  - Create listing in `providers` table with featured status
  - Update submission status to "Approved"
  - Set reviewed_at timestamp and reviewed_by (admin email)
  - Calculate plan expiration date
  - Show success toast
- [ ] **Reject Action**:
  - Open rejection reason modal
  - Save rejection notes
  - Update status to "Rejected"
  - Show rejection toast

### Task 6.5: Payment History & Revenue Tracking
- [ ] Separate "Payment History" tab
- [ ] Show all approved payments with:
  - Date, Business Name, Plan, Amount, Duration
  - Who approved it
- [ ] Revenue analytics:
  - Total revenue (all time, this month, this year)
  - Monthly income chart
  - Plan distribution (Basic vs Featured vs Premium)
  - Revenue growth percentage
- [ ] Export payment history as CSV/PDF

---

## 🗺️ STEP 7: FUTURE ENHANCEMENTS (Phase 6)

### Google Maps Integration
- [ ] Integrate Google Maps API
- [ ] Show business location on map in detail page
- [ ] Distance-based filtering in search
- [ ] "View Location" button opens Google Maps

### Rating & Review System
- [ ] Star rating (1-5) with half-star support
- [ ] Text review submission form
- [ ] Display reviews on business detail page
- [ ] Admin review moderation (approve/reject)
- [ ] Average rating calculation
- [ ] Sort reviews by date/rating

### Business Hours System
- [ ] Admin/provider sets business hours (Mon-Sun)
- [ ] Auto "Open Now" badge based on current time
- [ ] Filter by open/closed status

### Advanced Search
- [ ] Autocomplete suggestions
- [ ] Search history
- [ ] Popular searches section

---

## 🚀 DEPLOYMENT CHECKLIST

### Supabase Production Setup
- [ ] Create production Supabase project (separate from dev)
- [ ] Run all table creation SQL scripts
- [ ] Set up RLS policies
- [ ] Create storage buckets
- [ ] Configure environment variables in deployment
- [ ] Test all CRUD operations
- [ ] Enable Supabase backup schedule

### Security Review
- [ ] Verify RLS policies are active
- [ ] Sanitize all user inputs
- [ ] Add rate limiting for analytics events
- [ ] HTTPS enforcement
- [ ] Secure admin authentication

### Performance Optimization
- [ ] Add database indexes on frequently queried columns
- [ ] Implement pagination for large tables
- [ ] Use Supabase caching
- [ ] Optimize image uploads (compression, WebP format)
- [ ] Lazy load analytics data

---

## 📝 CURRENT STATUS

**Phase 5 - Analytics & Payment Management**: 🔄 IN PROGRESS

**What's Working:**
- ✅ Supabase connected and verified
- ✅ Admin panel with full control
- ✅ Settings, categories, listings management
- ✅ Real-time sync between admin and main app
- ✅ Payment plans structure in code

**What Needs Setup:**
- 🔄 Create analytics tables in Supabase
- 🔄 Implement tracking in UI components
- 🔄 Build admin analytics dashboard
- 🔄 Complete payment review workflow
- 🔄 Add charts and reports

**Next Immediate Steps:**
1. Go to Supabase Dashboard → SQL Editor
2. Run table creation scripts (user_analytics, business_analytics, reviews)
3. Set up RLS policies
4. Create storage buckets
5. I'll implement tracking code in your app

---

## 🎯 SUCCESS METRICS

After Phase 5 is complete, you'll be able to:

✅ Track every user action (searches, views, clicks)  
✅ See which businesses get the most engagement  
✅ Know which categories are most popular  
✅ Verify payments and approve listings easily  
✅ See total revenue and payment history  
✅ Export analytics reports  
✅ Make data-driven decisions to grow Urban Hand  

**Full Supabase control means**: You can manage EVERYTHING from Supabase Dashboard + Admin Panel without touching code!
-- Meta Ads Database Schema
-- Stores Facebook/Instagram ad data and competitor intelligence

-- Ads Catalog
CREATE TABLE IF NOT EXISTS ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id TEXT UNIQUE NOT NULL,
    page_name TEXT,
    page_id TEXT,
    ad_creative_body TEXT,
    ad_creative_link_title TEXT,
    ad_snapshot_url TEXT,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN,
    platform TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ad Spend Data
CREATE TABLE IF NOT EXISTS ad_spend (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id TEXT NOT NULL,
    spend_lower REAL,
    spend_upper REAL,
    currency TEXT DEFAULT 'USD',
    date DATE,
    impressions_lower INTEGER,
    impressions_upper INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id)
);

-- Ad Targeting Data
CREATE TABLE IF NOT EXISTS ad_targeting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id TEXT NOT NULL,
    age_min INTEGER,
    age_max INTEGER,
    gender TEXT,
    locations TEXT,
    interests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id)
);

-- Ad Creatives
CREATE TABLE IF NOT EXISTS ad_creatives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id TEXT NOT NULL,
    creative_type TEXT,
    image_url TEXT,
    video_url TEXT,
    thumbnail_url TEXT,
    headline TEXT,
    link_description TEXT,
    call_to_action TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id)
);

-- Ad Performance Metrics
CREATE TABLE IF NOT EXISTS ad_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id TEXT NOT NULL,
    reach_lower INTEGER,
    reach_upper INTEGER,
    engagement_count INTEGER,
    click_count INTEGER,
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES ads(ad_id)
);

-- Competitor Analysis
CREATE TABLE IF NOT EXISTS competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT NOT NULL,
    page_id TEXT UNIQUE,
    industry TEXT,
    total_active_ads INTEGER,
    avg_ad_spend REAL,
    last_analyzed TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ad Search Results
CREATE TABLE IF NOT EXISTS ad_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_keyword TEXT NOT NULL,
    ad_id TEXT NOT NULL,
    relevance_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_ads_page ON ads(page_name);
CREATE INDEX IF NOT EXISTS idx_ads_active ON ads(is_active);
CREATE INDEX IF NOT EXISTS idx_ad_spend_date ON ad_spend(date);
CREATE INDEX IF NOT EXISTS idx_competitors_page ON competitors(page_name);
CREATE INDEX IF NOT EXISTS idx_ad_searches_keyword ON ad_searches(search_keyword);


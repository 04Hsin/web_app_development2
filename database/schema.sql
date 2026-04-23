-- 建立分類表
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立紀錄表
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category_id INTEGER NOT NULL,
    note TEXT,
    record_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL
);

-- 插入預設分類 (若尚未存在)
INSERT INTO categories (name, type) 
SELECT '飲食', 'expense' 
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name='飲食' AND type='expense');

INSERT INTO categories (name, type) 
SELECT '交通', 'expense' 
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name='交通' AND type='expense');

INSERT INTO categories (name, type) 
SELECT '娛樂', 'expense' 
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name='娛樂' AND type='expense');

INSERT INTO categories (name, type) 
SELECT '薪水', 'income' 
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name='薪水' AND type='income');

INSERT INTO categories (name, type) 
SELECT '獎金', 'income' 
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name='獎金' AND type='income');

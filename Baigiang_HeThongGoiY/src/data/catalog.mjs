// ============================================================
// BỘ DỮ LIỆU MINH HỌA NHẤT QUÁN — xuyên suốt toàn video.
// Mọi con số là GIẢ ĐỊNH để dạy học, KHÔNG phải kết quả thực nghiệm.
// Engine (app.js) và tài liệu đều tham chiếu bộ này để tránh lệch số liệu.
// ============================================================

// Catalog 5 điện thoại (thông số rút gọn, minh họa).
export const ITEMS = [
  { id: 'I1', name: 'Galaxy S24',   brand: 'Samsung', ram: 12, rom: 256, pin: 5000, cam: 200, tag: 'Cấu hình cao' },
  { id: 'I2', name: 'Galaxy A55',   brand: 'Samsung', ram: 8,  rom: 256, pin: 5000, cam: 50,  tag: 'Tầm trung' },
  { id: 'I3', name: 'iPhone 15',    brand: 'Apple',   ram: 6,  rom: 128, pin: 3349, cam: 48,  tag: 'Camera' },
  { id: 'I4', name: 'iPhone 15 Pro',brand: 'Apple',   ram: 8,  rom: 256, pin: 3274, cam: 48,  tag: 'Camera Pro' },
  { id: 'I5', name: 'Xiaomi 14',    brand: 'Xiaomi',  ram: 12, rom: 256, pin: 4610, cam: 50,  tag: 'Cấu hình cao' }
];

// Persona người dùng.
export const USERS = [
  { id: 'A', label: 'Người dùng A', taste: 'Thích Samsung, cấu hình cao', color: '#2563EB' },
  { id: 'B', label: 'Người dùng B', taste: 'Thích iPhone, quan tâm camera', color: '#8B5CF6' },
  { id: 'C', label: 'Người dùng C', taste: 'Người mới, chưa có lịch sử', color: '#64748B' },
  { id: 'D', label: 'Người dùng D', taste: 'Cùng gu cấu hình cao với A', color: '#06B6D4' }
];

// Ma trận User–Item (đánh giá 1–5). null = CHƯA tương tác (không phải 0).
// Hàng: A, B, C, D — Cột: I1..I5
export const MATRIX = {
  cols: ['I1', 'I2', 'I3', 'I4', 'I5'],
  rows: [
    { user: 'A', r: [5, 4, null, null, null] },
    { user: 'B', r: [3, null, 5, null, null] },
    { user: 'C', r: [null, null, null, null, null] },
    { user: 'D', r: [5, 4, 2, null, 5] }
  ]
};

// Tín hiệu phổ biến (minh họa). Lượt mua theo đúng ví dụ của đề: 1000 / 750 / 500.
export const POPULARITY = [
  { id: 'I1', name: 'Galaxy S24', buys: 1000, views: 12000, rating: 4.8 },
  { id: 'I3', name: 'iPhone 15',  buys: 750,  views: 9500,  rating: 4.7 },
  { id: 'I5', name: 'Xiaomi 14',  buys: 500,  views: 6000,  rating: 4.6 }
];
// Điểm phổ biến chuẩn hóa theo lượt mua (max = 1000).
export const POP_SCORE = { I1: 1.0, I3: 0.75, I5: 0.5 };

// KNN user-based: A và D đồng đánh giá I1=5, I2=4 -> cosine trên ô cùng đánh giá = 1.00 (vector trùng nhau).
// k=1, láng giềng D. Dự đoán trung bình có trọng số: r̂(A,I5) = sim·r(D,I5)/sim = 5.0.
// D đã đánh giá I5=5, A chưa -> dự đoán A thích I5 (Xiaomi 14). Mọi số là GIẢ ĐỊNH.
export const KNN = {
  target: 'A', neighbor: 'D', k: 1,
  coRated: ['I1', 'I2'],
  cosineAD: 1.00,
  predict: { item: 'I5', from: 'D', rating: 5, score: 5.0 },
  alsoLow: { item: 'I3', from: 'D', rating: 2, score: 2.0 }
};

// Weighted Hybrid cho ứng viên I5 (Xiaomi 14) với người dùng A.
// Điểm đã chuẩn hóa về [0,1] trước khi kết hợp.
export const WEIGHTED = {
  item: 'I5', user: 'A',
  wCF: 0.5, wCB: 0.3, wPOP: 0.2,
  sCF: 0.9, sCB: 0.8, sPOP: 0.5,
  // 0.5*0.9 + 0.3*0.8 + 0.2*0.5 = 0.45 + 0.24 + 0.10 = 0.79
  score: 0.79
};

// Cascade: danh sách ứng viên -> SVD -> Content-Based -> xếp hạng.
export const CASCADE = [
  { id: 'I5', name: 'Xiaomi 14',     svd: 4.6, cb: 0.86, final: 0.88 },
  { id: 'I4', name: 'iPhone 15 Pro', svd: 3.1, cb: 0.55, final: 0.52 },
  { id: 'I2', name: 'Galaxy A55',    svd: 4.0, cb: 0.72, final: 0.74 },
  { id: 'I3', name: 'iPhone 15',     svd: 2.4, cb: 0.40, final: 0.38 },
  { id: 'I1', name: 'Galaxy S24',    svd: 4.9, cb: 0.95, final: 0.95, owned: true }
];

// TF-IDF: từ khóa trích từ mô tả sản phẩm (minh họa).
export const TFIDF_TERMS = ['samsung', 'ram', '12gb', 'pin', '5000', 'camera', '200mp', 'iphone', 'apple'];
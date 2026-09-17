use('fashion_custom_ecommerce');

db.createCollection('users');
db.createCollection('products');
db.createCollection('custom_designs');
db.createCollection('carts');
db.createCollection('orders');

db.products.createIndex({ slug: 1 }, { unique: true });
db.custom_designs.createIndex({ productSlug: 1, variantSku: 1, createdAt: -1 });
db.orders.createIndex({ userId: 1, createdAt: -1 });

db.products.updateOne(
  { slug: 'ao-thun-studio' },
  {
    $set: {
      slug: 'ao-thun-studio', name: 'Áo thun Studio', basePrice: 249000, currency: 'VND',
      image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80',
      variants: [
        { sku: 'TS-BLK-S', color: 'Đen', hex: '#151515', size: 'S', stock: 12, price: 249000 },
        { sku: 'TS-BLK-M', color: 'Đen', hex: '#151515', size: 'M', stock: 18, price: 249000 },
        { sku: 'TS-WHT-M', color: 'Trắng', hex: '#f6f4ef', size: 'M', stock: 20, price: 249000 },
        { sku: 'TS-CRM-L', color: 'Kem', hex: '#e4d6bd', size: 'L', stock: 7, price: 259000 }
      ], customization: { printFee: 35000, maxTextLength: 24 }
    }
  }, { upsert: true }
);

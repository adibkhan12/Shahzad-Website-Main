export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  date_joined: string;
  referral_source?: string;
  referral_other?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  parent: number | null;
  image: string;
  properties: any[];
  product_count?: number;
}

export interface BrandRef {
  id: number;
  name: string;
  slug: string;
  category?: number | null;
  category_name?: string;
  category_slug?: string;
  logo?: string;
  description?: string;
  is_active?: boolean;
  order?: number;
}

/** Distinct-by-name brand grouping returned by /catalog/products/brands/.
 *  Each entry aggregates the categories that brand sells under. */
export interface BrandGroup {
  name: string;
  slug: string;
  categories: { name: string; slug: string }[];
}

export interface CatalogProperty {
  id: number;
  property_name: string;
  property_values: string[];
}

export interface ColorVariantData {
  id: number;
  color_name: string;
  price: string | null;
  order: number;
  images: string[];
}

export interface Product {
  id: number;
  title: string;
  slug: string;
  description?: string;
  price: string;
  sale_price: string | null;
  effective_price: string;
  on_sale: boolean;
  primary_image: string;
  images: string[];
  stock: number;
  brand: BrandRef | null;
  category: number | Category | null;
  category_slug?: string;
  category_name?: string;
  is_active: boolean;
  is_featured: boolean;
  has_color_variants?: boolean;
  is_price_same?: boolean;
  color_variants_data?: ColorVariantData[];
  properties?: Record<string, any>;
  product_properties?: Record<string, string>;
  rating_avg?: number;
  rating_count?: number;
  created_at?: string;
  updated_at?: string;
}

export interface Review {
  id: number;
  product?: number;
  user: string;
  rating: number;
  text: string;
  images?: string[];
  created_at: string;
}

export interface QA {
  id: number;
  product?: number;
  user: string;
  question: string;
  answer: string;
  created_at: string;
  answered_at?: string | null;
}

export interface Banner {
  id: number;
  title: string;
  desc: string;
  image: string;
  button: string;
  link: string;
  bg: string;
  order: number;
}

export interface CartItem {
  id: number;
  product: Product;
  quantity: number;
  added_at: string;
  line_total: string;
}

export interface Cart {
  id?: number;
  items: CartItem[];
  subtotal: string;
  count: number;
  updated_at?: string;
}

export interface Address {
  id: number;
  name: string;
  email: string;
  phone: string;
  address_line1: string;
  address_line2: string;
  city: string;
  postal_code: string;
  country: string;
  is_default: boolean;
  created_at?: string;
}

export interface OrderItem {
  id: number;
  product: number | null;
  title: string;
  unit_price: string;
  quantity: number;
  image: string;
  line_total: string;
}

export interface Order {
  id: number;
  reference: string;
  short_ref: string;
  user: number | null;
  name: string;
  email: string;
  phone: string;
  address_line1: string;
  address_line2: string;
  city: string;
  postal_code: string;
  country: string;
  region: 'UAE' | 'KSA';
  currency: string;
  subtotal: string;
  shipping_fee: string;
  bnpl_surcharge: string;
  total: string;
  payment_method: 'cod' | 'tamara' | 'tabby';
  provider: string;
  provider_ref: string;
  paid: boolean;
  status: 'pending' | 'paid' | 'shipped' | 'delivered' | 'cancelled' | 'failed';
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

export interface RepairService {
  id: number;
  name: string;
  slug: string;
  device: string;
  short_desc: string;
  description: string;
  base_price: string;
  est_minutes: number;
  icon: string;
  is_featured: boolean;
  order: number;
}

export interface RepairBooking {
  id: number;
  reference: string;
  short_ref: string;
  service: number | null;
  service_name?: string;
  service_slug?: string;
  name: string;
  email: string;
  phone: string;
  device_brand: string;
  device_model: string;
  issue: string;
  preferred_drop_off: string | null;
  quoted_price: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

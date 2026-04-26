from datetime import datetime
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select, or_, func
from database import engine, init_db
from models import (ProductDB, Product, ProductOut, ProductSearchRequest, SortBy,  OrderDB, OrderOut, OrderCreate, OrderStatus, OrderItemDB, PaymentDB, Payment, PaymentOut, CustomerDB, Customer, CustomerOut, SellerDB, Seller, SellerOut, CategoryDB, CartItemDB, CartItemCreate, CustomerDB, PostDB, Post, PostOut, CommentDB, Comment, CommentOut,SigninRequest)
from fastapi.middleware.cors import CORSMiddleware

init_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # อนุญาตให้ทุกพอร์ตคุยด้วยได้
    allow_credentials=True,
    allow_methods=["*"], # อนุญาตทุก Method (รวมถึง OPTIONS ที่ทำให้เกิด 405)
    allow_headers=["*"],
)

#Product
RUN_SEED_DATA = True #ตอนจะinsertค่อยเปลี่ยนเป็นTrue #เป็น flag variable
#เพิ่มสินค้าใหม่
def insert_product():
    product_1 = ProductDB(
        pname = "เสื้อเชิ้ตลายสก็อต Uniqlo Flanel",
        price= 350.0,
        brand= "Uniqlo",
        description= "สภาพ 95% ผ้าหนานุ่ม ใส่สบาย อก 42 นิ้ว ยาว 28 นิ้ว",
        categoryID= 1,
        seller_id= 101,
        tags= "เสื้อเชิ้ต, แบรนด์เนม, ยูนิโคล่",
        product_status= "available"
    )


    product_2 = ProductDB(
        pname= "กางเกงยีนส์ Levi's 501 ริมแดง",
        price= 1200.0,
        brand= "Levi's",
        description= "วินเทจยุค 90s เอว 32 นิ้ว มีตำหนิรอยขาดเล็กน้อยที่ปลายขาซ้าย",
        categoryID= 2,
        seller_id= 102,
        tags= "กางเกงยีนส์, วินเทจ, levis",
        product_status= "available"
    )
   
    product_3 = ProductDB(
        pname= "เสื้อกันหนาวไหมพรมทรง Oversize",
        price= 490.0,
        brand= "H&M",
        description= "สีครีมมินิมอล งานปักมือ ไซซ์ Free size อกได้ถึง 46 นิ้ว",
        categoryID= 1,
        seller_id= 103,
        tags= "เสื้อกันหนาว, มินิมอล, แฟชั่นเกาหลี",
        product_status= "reserved"
    )

    with Session(engine) as session:
        session.add(product_1)
        session.add(product_2)
        session.add(product_3)
        session.commit()
        print("✅ Inserted products successfully!")

#เพิ่มประเภทของ category
def insert_categories():
    categories = [
        "เสื้อเชิ้ตผู้ชาย", "เสื้อยืดผู้ชาย", "กางเกงผู้ชาย", "แจ็คเก็ตผู้ชาย",
        "ชุดเดรสผู้หญิง", "เสื้อบลาวส์ผู้หญิง", "กระโปรง", "กางเกงผู้หญิง",
        "เสื้อยืดผู้หญิง", "เสื้อผ้าเด็ก",
        "เครื่องประดับ", "รองเท้า", "กระเป๋า", "ชุดชั้นใน", "ชุดกีฬา"
    ] 

    with Session(engine) as session:
        for name in categories:
            session.add(CategoryDB(category_name=name))
        session.commit()
        print("✅ Inserted categories successfully!")

if __name__ == "__main__":
    if RUN_SEED_DATA:
        insert_product()
        insert_categories()
    else:
        print("ℹ️ Seed data disabled (RUN_SEED_DATA = False)")



@app.get("/categories/")
async def get_all_categories():
    with Session(engine) as session:
        categories = session.exec(select(CategoryDB)).all()
        return categories


#post product
@app.post("/products/")
async def create_product(product: Product) -> ProductOut:
    with Session(engine) as session:
        db_product = ProductDB(
            pname=product.pname,
            price=product.price,
            brand=product.brand,
            description=product.description,
            categoryID=product.categoryID,
            seller_id=product.seller_id,
            tags=product.tags,
            product_status=product.product_status,
            image_url=product.image_url
        )
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product

#อัพเดตรูปสินค้าที่มีอยู่แล้ว (ได้แค่รูปเดียว)
@app.patch("/products/{product_id}/image")
async def update_product_image(product_id: int, image_url: str):
    with Session(engine) as session:
        product = session.get(ProductDB, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.image_url = image_url
        session.add(product)
        session.commit()
        session.refresh(product)
        return {"image_url": product.image_url}

#endpoints ดึงสินค้าตามid
@app.get("/products/{product_id}")
async def Get_product_by_ID(product_id: int) -> ProductOut:
    with Session(engine) as s:
        statement = select(ProductDB).where(ProductDB.product_id == product_id)
        product = s.exec(statement).first()
       
        if product != None:
            print(product)
            return product
       
    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
#endpoint ดึงสินค้าทั้งหมด
@app.get("/products/")
async def get_all_products() -> list[ProductOut]:
    """Get all products from database"""
    with Session(engine) as session:
        statement = select(ProductDB)
        products = session.exec(statement).all()
        return products


#อัพเดตข้อมูลสินค้า
@app.put("/products/{product_id}")
async def update_product(product_id: int, new_product: Product):
    with Session(engine) as session:
        product = session.get(ProductDB, product_id)

        if (product != None):
            product.pname = new_product.pname
            #อยากอัพอันไหน ใส่ข้อมูลอันนั้น กันหาย

            session.add(product)
            session.commit()
            session.refresh(product)
            return {"message"  : "Product update succesfully"}

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

###Order
#สร้าง order พร้อม orderitem + คำนวณ total price
def validate_product_for_order(product: ProductDB, item_qty: int):
    if product.product_status != "available":
        raise HTTPException(status_code=400, detail="Product not available")

    if product.price is None or product.price <= 0:
        raise HTTPException(status_code=400, detail="Invalid product price")

    return True

def process_order_logic(session, cus_id, items_to_process, shipping_cost):
    total_price = 0

    for item in items_to_process:
        product = session.get(ProductDB, item.product_id)
        validate_product_for_order(product, item.qty)
        total_price += product.price * item.qty

    # ← สร้าง order
    new_order = OrderDB(
        cus_id=cus_id,
        total_price=total_price,
        shipping_cost=shipping_cost,
        grand_total=total_price + shipping_cost,
        order_status="pending"
    )
    session.add(new_order)
    session.flush()  # ได้ order_id ก่อน commit

    # ← สร้าง order items
    for item in items_to_process:
        product = session.get(ProductDB, item.product_id)
        order_item = OrderItemDB(
            order_id=new_order.order_id,
            product_id=item.product_id,
            qty=item.qty,
            price=product.price
        )
        session.add(order_item)
        product.product_status = "reserved"
        session.add(product)

    return new_order  # ← return กลับไปให้ checkout

#ซื้อเลย (Buy Now)
@app.post("/create-order/")
async def create_order(order: OrderCreate):
    with Session(engine) as session:
        try:
            # เรียกใช้ "กุ๊ก" (Helper Function) ตรงนี้ครับ!
            new_order = process_order_logic(session, order.cus_id, order.items, order.shipping_cost)
            session.commit()
            session.refresh(new_order)
            return {"message": "Order created via Buy Now", "order_id": new_order.order_id}
        except Exception as e:
            session.rollback()
            raise e

#หน้าตะกร้า (Checkout)
@app.post("/orders/checkout/{cus_id}")
async def checkout(cus_id: int):
    with Session(engine) as session:
        cart_items = session.exec(select(CartItemDB).where(CartItemDB.cus_id == cus_id)).all()
        
        if not cart_items:
            raise HTTPException(status_code=400, detail="ตะกร้าว่างเปล่าจ้า")

        # คำนวณ total ก่อน
        total_price = 0
        for item in cart_items:
            product = session.get(ProductDB, item.product_id)
            if product:
                total_price += product.price * item.qty

        shipping_cost = 50.0

        # สร้าง order พร้อม field ครบ
        new_order = OrderDB(
            cus_id=cus_id,
            total_price=total_price,
            shipping_cost=shipping_cost,
            grand_total=total_price + shipping_cost,
            order_status="pending"
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        # สร้าง order items + ลบ cart
        for item in cart_items:
            product = session.get(ProductDB, item.product_id)
            order_item = OrderItemDB(
                order_id=new_order.order_id,
                product_id=item.product_id,
                qty=item.qty,
                price=product.price if product else 0
            )
            session.add(order_item)
            session.delete(item)

            if product:
                product.product_status = "sold"
                session.add(product)

        session.commit()
        return {"message": "สั่งซื้อสำเร็จ", "order_id": new_order.order_id}
        
#get all order
@app.get("/orders/")
async def get_all_orders() -> list[OrderOut]:
    with Session(engine) as session:
        statement = select(OrderDB)
        orders = session.exec(statement).all()
        return orders       

#get order by id   
@app.get("/orders/{order_id}")
async def Get_order_by_id(order_id: int) -> OrderOut:
    with Session(engine) as s:
        statement = select(OrderDB).where(OrderDB.order_id == order_id)
        order = s.exec(statement).first()
       
        if order != None:
            print(order)
            return order
       
    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )

@app.get("/orders/customer/{cus_id}")
async def get_orders_by_customer(cus_id: int):
    with Session(engine) as session:
        orders = session.exec(
            select(OrderDB).where(OrderDB.cus_id == cus_id)
        ).all()
        return orders
#get order พร้อม item ใช้ where แทนการวน loop

@app.get("/order_items/{order_id}")
async def get_order_item(order_id: int):
    with Session(engine) as session:
        db_order = session.get(OrderDB, order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # ดึง Order Items
        items_statement = select(OrderItemDB).where(OrderItemDB.order_id == order_id)
        order_items = session.exec(items_statement).all()

        if not order_items:
            return {
                "order_id": db_order.order_id,
                "cus_id": db_order.cus_id,
                "total_price": float(db_order.total_price),
                "shipping_cost": float(db_order.shipping_cost),
                "grand_total": float(db_order.grand_total),
                "order_status": db_order.order_status,
                "created_at": db_order.created_at.isoformat(),
                "items": []
            }

        # ดึง Products ทั้งหมดพร้อมกัน (1 query)
        product_ids = [item.product_id for item in order_items]
        products_statement = select(ProductDB).where(ProductDB.product_id.in_(product_ids))
        products = session.exec(products_statement).all()
        # สร้าง dict สำหรับ lookup
        products_dict = {p.product_id: p for p in products}
        
        # ใช้ products_dict แทนการ unpack tuple
        items_with_details = [
            {
                "orderitem_id": item.orderitem_id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "product_name": products_dict.get(item.product_id).pname if products_dict.get(item.product_id) else "Product Deleted",  # ✅ ใช้ .get()
                "brand": products_dict.get(item.product_id).brand if products_dict.get(item.product_id) else "Unknown",  # ✅ ใช้ .get()
                "qty": item.qty,
                "price": float(item.price),
                "subtotal": float(item.price * item.qty)
            }
            for item in order_items  # ✅ loop item เดียว
        ]
        
        return {
            "order_id": db_order.order_id,
            "cus_id": db_order.cus_id,
            "total_price": float(db_order.total_price),
            "shipping_cost": float(db_order.shipping_cost),
            "grand_total": float(db_order.grand_total),
            "order_status": db_order.order_status,
            "created_at": db_order.created_at.isoformat(),
            "items": items_with_details
        }

#cancel order
@app.put("/orders/{order_id}/cancel")
async def cancel_order(order_id: int):
    with Session(engine) as session:
        order = session.get(OrderDB, order_id)
        
        if order.order_status == "cancelled" :
            return {"message": "Order is already cancelled"}
        
        order.order_status = "cancelled"
        session.add(order)
            
        statement = select(OrderItemDB).where(OrderItemDB.order_id == order_id)
        order_items = session.exec(statement).all()

        for item in order_items:
            product = session.get(ProductDB, item.product_id)
            if product:
                
                product.product_status = "available" 
                session.add(product)    
            
        session.commit()
        session.refresh(order)
        return order
    
        raise HTTPException(
            status_code=404,
            detail="Order no found"
        )
    
#เปลี่ยนสถานะ order
@app.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, status: OrderStatus):
    with Session(engine) as session:
        order = session.get(OrderDB, order_id)
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.order_status = status
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


#Payment
@app.post("/payments/")
async def create_payment(payment_data: Payment) -> PaymentOut:
    with Session(engine) as session:
        #สร้างลิสต์รายการที่อนุญาต
        allowed_methods = ["credit_card", "qr_code", "bank_transfer"]
    
        #ตรวจสอบว่าค่าที่ส่งมาอยู่ในรายการไหม
        if payment_data.payment_method not in allowed_methods:
            raise HTTPException(
            status_code=400, 
            detail=f"Invalid payment method. Allowed: {allowed_methods}"
        )

        #ตรวจสอบว่า Order มีอยู่จริงไหม (Validation)
        order = session.get(OrderDB, payment_data.order_id)
        if not order:
            raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

        #บันทึกการชำระเงิน
        db_payment = PaymentDB(
            order_id=payment_data.order_id,
            payment_method=payment_data.payment_method,
            payment_amount=payment_data.payment_amount,
            payment_status=payment_data.payment_status,
            payment_date=payment_data.payment_date,
            transaction_no=payment_data.transaction_no
        )
        session.add(db_payment)
        
        #อัปเดตสถานะ Order เป็น "paid" 
        order.order_status = "paid"  
        session.add(order)
        session.commit()
        session.refresh(db_payment)
        return db_payment
    
# get all Payment    
@app.get("/payments/")
async def get_all_payments():
    with Session(engine) as session:
        
        statement = select(PaymentDB)
        results = session.exec(statement).all()
        return results

# get id Payment   
@app.get("/payments/{payment_id}")
async def get_payment_by_id(payment_id: int):
    with Session(engine) as session:
        payment = session.get(PaymentDB, payment_id)

        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found")
        return payment


#Customer
#post
@app.post("/customers/")
async def create_customers(customers: list[Customer]) -> list[CustomerOut]:
    with Session(engine) as session:
        created_customers = []
        
        for customer_data in customers:
            # เช็ค Email ซ้ำเบื้องต้น
            existing = session.exec(
                select(CustomerDB).where(CustomerDB.email == customer_data.email)
            ).first()
            
            if not existing:
                db_customer = CustomerDB(
                    username=customer_data.username,
                    email=customer_data.email,
                    customer_phone=customer_data.customer_phone,
                    password=customer_data.password,
                    display_name=customer_data.display_name,
                    avatar=customer_data.avatar
                )
                session.add(db_customer)
                created_customers.append(db_customer)
        
        session.commit()
        # Refresh ข้อมูลเพื่อให้ได้ ID กลับมาโชว์
        for c in created_customers:
            session.refresh(c)
            
        return created_customers


#get all
@app.get("/customers/")
def get_all_customers():
    with Session(engine) as session:
        customers = session.exec(select(CustomerDB)).all()
        return customers
    
#get by id
@app.get("/customers/{cus_id}")
def get_customer_by_id(cus_id: int):
    with Session(engine) as session:
        customer = session.get(CustomerDB, cus_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return customer 

#Seller
@app.post("/sellers/")
async def create_seller(seller: Seller) -> SellerOut :
    with Session(engine) as session:
        db_seller = SellerDB(
            seller_name=seller.seller_name,
            email=seller.email,
            seller_phone=seller.seller_phone,
            store_name=seller.store_name,
            verification_status=seller.verification_status
        )

        session.add(db_seller)
        session.commit()
        session.refresh(db_seller)

        return db_seller

#Get all seller
@app.get("/sellers/")
async def get_all_sellers() -> list[SellerOut]:
    with Session(engine) as session:
        statement = select(SellerDB)
        sellers = session.exec(statement).all()
        return sellers

#Get seller by id
@app.get("/sellers/{seller_id}")
async def get_seller_by_id(seller_id: int) -> SellerOut:
    with Session(engine) as session:
        seller = session.get(SellerDB, seller_id)

        if seller is None:
            raise HTTPException(
                status_code=404,
                detail="Seller not found"
            )

        return seller

###Search product
@app.post("/products/search")
async def search_products(search: ProductSearchRequest):
    """
    🔍 Smart Search สินค้า
    
    Features:
    - Search by text (ชื่อ, brand, description)
    - Filter by: category, brand, tags
    - Sort by: price (low/high), newest, oldest
    - Pagination
    """
    
    with Session(engine) as session:
        # เริ่มต้น query
        query = select(ProductDB)
        
        # ===== 1. TEXT SEARCH =====
        if search.query:
            search_term = f"%{search.query}%"
            query = query.where(
                or_(
                    ProductDB.pname.ilike(search_term),
                    ProductDB.brand.ilike(search_term),
                    ProductDB.description.ilike(search_term)
                )
            )
        
        # ===== 2. FILTER BY CATEGORY =====
        if search.category_id:
            query = query.where(ProductDB.categoryID == search.category_id)
        
        # ===== 3. FILTER BY BRAND =====
        if search.brand:
            query = query.where(ProductDB.brand.ilike(f"%{search.brand}%"))
        
        # ===== 4. FILTER BY TAGS =====
        if search.tags:
            # ค้นหาสินค้าที่มี tag ใดๆ ที่ระบุ
            tag_conditions = [
                ProductDB.tags.ilike(f"%{tag}%") for tag in search.tags
            ]
            query = query.where(or_(*tag_conditions))
        
        # ===== 5. PRICE RANGE (Optional) =====
        if search.min_price is not None:
            query = query.where(ProductDB.price >= search.min_price)
        
        if search.max_price is not None:
            query = query.where(ProductDB.price <= search.max_price)
        
        # ===== 6. DEFAULT: แสดงเฉพาะ available =====
        query = query.where(ProductDB.product_status == "available")
        
        # ===== 7. SORTING =====
        if search.sort_by == SortBy.PRICE_LOW:
            query = query.order_by(ProductDB.price.asc())
        elif search.sort_by == SortBy.PRICE_HIGH:
            query = query.order_by(ProductDB.price.desc())
        elif search.sort_by == SortBy.NEWEST:
            query = query.order_by(ProductDB.product_id.desc())
        elif search.sort_by == SortBy.OLDEST:
            query = query.order_by(ProductDB.product_id.asc())
        
        # ===== 8. COUNT TOTAL =====
        count_query = select(func.count()).select_from(query.subquery())
        total = session.exec(count_query).one()
        
        # ===== 9. PAGINATION =====
        offset = (search.page - 1) * search.page_size
        query = query.offset(offset).limit(search.page_size)
        
        # ===== 10. EXECUTE =====
        products = session.exec(query).all()
        
        # ===== 11. BUILD RESPONSE =====
        total_pages = (total + search.page_size - 1) // search.page_size
        
        return {
            "total": total,
            "page": search.page,
            "page_size": search.page_size,
            "total_pages": total_pages,
            "products": [
                {
                    "product_id": p.product_id,
                    "pname": p.pname,
                    "price": float(p.price) if p.price else None,
                    "brand": p.brand,
                    "description": p.description,
                    "categoryID": p.categoryID,
                    "seller_id": p.seller_id,
                    "tags": p.tags,
                    "product_status": p.product_status,
                    "image_url": p.image_url or "https://placehold.co/400x400"
                }
                for p in products
            ]
        }
    
#Cart
#"เพิ่ม" สินค้าลงตะกร้า
@app.post("/cart/add")
async def add_to_cart(item: CartItemCreate):
    with Session(engine) as session:
        # เช็กก่อนว่าเคยหยิบชิ้นนี้ใส่ตะกร้าหรือยัง
        statement = select(CartItemDB).where(
            CartItemDB.cus_id == item.cus_id, 
            CartItemDB.product_id == item.product_id
        )
        existing_item = session.exec(statement).first()

        if existing_item:
            # ถ้ามีแล้ว ไม่ต้องทำอะไร หรือจะเพิ่มจำนวนก็ได้ (แต่โปรเจกต์นี้เสื้อผ้ามีชิ้นเดียว เลยข้ามไป)
            return {"message": "มีสินค้านี้ในตะกร้าแล้ว"}
        else:
            # ถ้ายังไม่มี ให้บันทึกลง Database
            db_item = CartItemDB(cus_id=item.cus_id, product_id=item.product_id, qty=item.qty)
            session.add(db_item)
            session.commit()
            return {"message": "เพิ่มลงตะกร้าสำเร็จ"}

#"ดึงข้อมูล" ตะกร้าของลูกค้าแต่ละคน
@app.get("/cart/{cus_id}")
async def get_cart(cus_id: int):
    with Session(engine) as session:
        # ดึงสินค้าในตะกร้า
        statement = select(CartItemDB).where(CartItemDB.cus_id == cus_id)
        cart_items = session.exec(statement).all()

        # ดึงรายละเอียดสินค้า (ชื่อ, ราคา, รูป) มาประกอบกัน
        results = []
        for item in cart_items:
            product = session.get(ProductDB, item.product_id)
            if product:
                results.append({
                    "cartitem_id": item.cartitem_id,
                    "product_id": product.product_id,
                    "name": product.pname,
                    "price": product.price,
                    "shop": product.brand,
                    "description": product.description,
                    "selected": True, # ให้ติ๊กถูกไว้เลยตั้งแต่แรก
                    "img": product.image_url or 'https://placehold.co/400x400'
                })
        return results

#"ลบ" สินค้าออกจากตะกร้า
@app.delete("/cart/remove/{cartitem_id}")
async def remove_from_cart(cartitem_id: int):
    with Session(engine) as session:
        item = session.get(CartItemDB, cartitem_id)
        if item:
            session.delete(item)
            session.commit()
            return {"message": "ลบสำเร็จ"}
        return {"message": "ไม่พบข้อมูล"}


###Community
# 1. ดึงโพสต์ทั้งหมด (สำหรับหน้า Feed)
@app.get("/posts/")
async def get_all_posts() -> list[dict]:
    with Session(engine) as session:
        # 1. ดึงโพสต์ทั้งหมดจาก DB (เรียงจากใหม่ไปเก่า หรือตาม ID)
        statement = select(PostDB).order_by(PostDB.post_id.asc())
        posts_db = session.exec(statement).all()

        final_result = []

        for p in posts_db:
            # 2. หาข้อมูลเจ้าของโพสต์ (name, username, avatar)
            user = session.get(CustomerDB, p.customer_id)
            
            # 3. หาคอมเมนต์ทั้งหมดของโพสต์นี้ เพื่อทำเป็น staticComments
            comment_statement = select(CommentDB).where(CommentDB.post_id == p.post_id)
            comments_db = session.exec(comment_statement).all()
            
            static_comments = []
            for c in comments_db:
                c_user = session.get(CustomerDB, c.customer_id)
                static_comments.append({
                    "name": c_user.display_name if c_user else "Unknown",
                    "avatar": c_user.avatar if c_user else "",
                    "text": c.text,
                    "time": c.time_str  # เช่น "2 hrs"
                })

            # 4. ประกอบร่างให้เหมือนโครงสร้างใน data.js
            post_obj = {
                "id": p.post_id,
                "name": user.display_name if user else "Unknown",
                "username": f"@{user.username}" if user else "@unknown",
                "avatar": user.avatar if user else "",
                "content": p.content,
                "image": p.image_url, # เปลี่ยนชื่อจาก image_url เป็น image ตาม data.js
                "likes": p.likes,
                "reposts": p.reposts,
                "shares": p.shares,
                "staticComments": static_comments,
                "comments": len(static_comments) # นับจำนวนคอมเมนต์
            }
            final_result.append(post_obj)

        return final_result


# 2. ดึงรายละเอียดโพสต์รายอัน พร้อมเม้นท์ (สำหรับหน้า Post Detail)
# ในไฟล์ main.py
@app.get("/posts/{post_id}")
async def get_post_detail(post_id: int):
    with Session(engine) as session:
        # 1. ดึงข้อมูลโพสต์ (ใช้ post_id ตามในรูปของคุณ)
        # ในรูปคอลัมน์ชื่อ post_id ดังนั้นเราต้องใช้คำสั่งดึงให้ถูก
        statement = select(PostDB).where(PostDB.post_id == post_id)
        db_post = session.exec(statement).first()
       
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")


        # 2. ไปดึงข้อมูลคนโพสต์จาก CustomerDB โดยใช้ customer_id จากตารางโพสต์
        author = session.get(CustomerDB, db_post.customer_id)


        # 3. ดึงคอมเมนต์ (เหมือนเดิม)
        comment_stmt = select(CommentDB).where(CommentDB.post_id == post_id)
        db_comments = session.exec(comment_stmt).all()


        comments_list = []
        for c in db_comments:
            c_user = session.get(CustomerDB, c.customer_id)
            comments_list.append({
                "name": c_user.display_name if c_user else "Guest",
                "avatar": c_user.avatar if c_user else "https://placehold.co/100x100",
                "text": c.text,
                "time": "Just now"
            })


        # 4. ส่งกลับโครงสร้างข้อมูลที่ถูกต้อง (Mapping ชื่อฟิลด์ให้ตรงกับรูป)
        return {
            "post_info": {
                "id": db_post.post_id,         # ในรูปคุณใช้ชื่อ post_id
                "content": db_post.content,
                "image": db_post.image_url,    # ในรูปคุณใช้ชื่อ image_url
                "likes": db_post.likes,
                "reposts": db_post.reposts,
                "shares": db_post.shares,
                "name": author.display_name if author else "Unknown",
                "username": author.username if author else "user",
                "avatar": author.avatar if author else ""
            },
            "static_comments": comments_list
        }


# 3. สร้างโพสต์ใหม่
@app.post("/posts/")
async def create_post(post: Post) -> PostOut:
    with Session(engine) as session:
        db_post = PostDB(**post.dict())
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        
        customer = session.get(CustomerDB, db_post.customer_id)
        return PostOut(
            **db_post.dict(),
            customer_name=customer.display_name if customer else "Unknown",
            customer_username=f"@{customer.username}" if customer else "@unknown",
            customer_avatar=customer.avatar if customer else "",
            comments_count=0
        )

# 4. เพิ่มคอมเมนต์ใหม่
@app.post("/posts/{post_id}/comments")
async def add_comment(post_id: int, comment: Comment) -> dict:
    with Session(engine) as session:
        # ตรวจสอบว่ามีโพสต์อยู่จริงไหม
        db_post = session.get(PostDB, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")

        db_comment = CommentDB(
            text=comment.text,
            post_id=post_id,
            customer_id=comment.customer_id,
            time_str="Just now"
        )
        session.add(db_comment)
        session.commit()
        session.refresh(db_comment)

        customer = session.get(CustomerDB, comment.customer_id)
        return {
            "comment_id": db_comment.comment_id,
            "name": customer.display_name if customer else "You",
            "avatar": customer.avatar if customer else "",
            "text": db_comment.text,
            "time": "Just now"
        }


@app.post("/signin")
def login(credentials: SigninRequest):
    
    with Session(engine) as session:
        
        statement = select(CustomerDB).where(
            CustomerDB.email == credentials.email,
            CustomerDB.password == credentials.password
        )
        
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=401, 
                detail="อีเมลหรือรหัสผ่านไม่ถูกต้อง"
            )
        # หา seller ที่ผูกกับ email นี้
        seller = session.exec(
            select(SellerDB).where(SellerDB.email == credentials.email)
        ).first()

        # ถ้ายังไม่มี seller → สร้างให้อัตโนมัติเลย
        if not seller:
            seller = SellerDB(
                seller_name=user.display_name or user.username,
                email=user.email,
                seller_phone=user.customer_phone or "",
                store_name=f"{user.display_name or user.username}'s Shop",
                verification_status="verified"
            )
            session.add(seller)
            session.commit()
            session.refresh(seller)

        return {
            "message": "Login successful",
            "customer_id": user.customer_id,
            "username": user.username,
            "display_name": user.display_name, 
            "avatar": user.avatar,             
            "seller_id": seller.seller_id if seller else None
        }
from datetime import datetime
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, or_, func
from database import engine, init_db
from models import (ProductDB, Product, ProductOut, ProductSearchRequest, SortBy,  OrderDB, OrderOut, OrderCreate, OrderStatus, OrderItemDB, PaymentDB, Payment, PaymentOut, CustomerDB, Customer, CustomerOut, SellerDB, Seller, SellerOut, CategoryDB )

init_db()
app = FastAPI()

#Product
RUN_SEED_DATA = False #ตอนจะinsertค่อยเปลี่ยนเป็นTrue #เป็น flag variable
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
            product_status=product.product_status
        )
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product

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
    
@app.post("/create-order/")
async def create_order(order: OrderCreate) -> dict:
    """
    สร้าง Order พร้อม Order Items
    - ดึง price จาก Product table
    - Validate product status และ price
    - Calculate total
    - เปลี่ยน Product Status เป็น sold
    """
    # Validate
    if not order.items or len(order.items) == 0:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    
    with Session(engine) as session:
        try:
            # 1. Validate products และดึงราคา
            validated_items = []
            products_to_update = []  # เพิ่ม: เก็บ products ที่จะอัพเดท
            total_price = 0
            
            for item in order.items:
                # ดึง product จาก database
                product = session.get(ProductDB, item.product_id)
                
                # ตรวจสอบว่า product มีอยู่
                if not product:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Product ID {item.product_id} not found"
                    )
                
                # Validate product (status, price)
                validate_product_for_order(product, item.qty)
                
                # คำนวณราคา
                item_price = product.price  # รับประกันว่าไม่ใช่ None แล้ว
                item_total = item_price * item.qty
                total_price += item_total
                
                validated_items.append({
                    'product_id': item.product_id,
                    'product_name': product.pname,
                    'brand': product.brand,
                    'qty': item.qty,
                    'price': item_price,
                    'subtotal': item_total
                })

                products_to_update.append(product)  # เพิ่ม: เก็บ product object

            
            # 2. คำนวณยอดรวม
            grand_total = total_price + order.shipping_cost
            
            # 3. สร้าง Order
            db_order = OrderDB(
                cus_id=order.cus_id,
                total_price=total_price,
                shipping_cost=order.shipping_cost,
                grand_total=grand_total,
                order_status=OrderStatus.pending,
                created_at=datetime.now()
            )
            session.add(db_order)
            session.flush()  # ได้ order_id
            
            # 4. สร้าง Order Items (เก็บ DB objects แยกต่างหาก)
            db_order_items = []  #  เก็บ DB objects
            for item_data in validated_items:
                db_item = OrderItemDB(
                    order_id=db_order.order_id,
                    product_id=item_data['product_id'],
                    qty=item_data['qty'],
                    price=item_data['price']
                )
                session.add(db_item)
                db_order_items.append(db_item)  # เก็บ DB object
            
            # 4.5 เปลี่ยน Product Status เป็น sold
            for product in products_to_update:
                product.product_status = "sold"
                print(f"✅ Changed {product.pname} status to sold")  # Debug
            
            # 5. Commit
            session.commit()
            
            # 6. Refresh
            session.refresh(db_order)
            for db_item in db_order_items:  #refresh DB objects
                session.refresh(db_item)
            
            # 7. Return response
            return {
                "message": "Order created successfully",
                "order_id": db_order.order_id,
                "cus_id": db_order.cus_id,
                "total_price": float(db_order.total_price),
                "shipping_cost": float(db_order.shipping_cost),
                "grand_total": float(db_order.grand_total),
                "order_status": db_order.order_status,
                "created_at": db_order.created_at.isoformat(),
                "items": [
                    {
                        "orderitem_id": db_item.orderitem_id,
                        "order_id": db_item.order_id,
                        "product_id": db_item.product_id,
                        "product_name": validated_items[i]['product_name'],
                        "brand": validated_items[i]['brand'],
                        "qty": db_item.qty,
                        "price": float(db_item.price),
                        "subtotal": float(db_item.price * db_item.qty)
                    } for i, db_item in enumerate(db_order_items)
                ]
            }
            
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to create order: {str(e)}"
            )

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
async def create_customer(customer: Customer) -> CustomerOut :
    with Session(engine) as session:
        existing = session.exec(
            select(CustomerDB).where(CustomerDB.email == customer.email)
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
        
        db_customer = CustomerDB(
            username=customer.username,
            email=customer.email,
            customer_phone=customer.customer_phone
        )
        
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)

        return db_customer

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
                    "product_status": p.product_status
                }
                for p in products
            ]
        }
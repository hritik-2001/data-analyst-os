import csv, os, random, sqlite3
from datetime import date, timedelta
random.seed(7)
ROOT='/mnt/data/data-analyst-os-v1/data'

def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

# Commerce
regions=['North','South','East','West']
segments=['Consumer','SMB','Enterprise']
countries=['India','UAE','Singapore','UK']
customers=[]
for i in range(1,3001):
    customers.append(dict(customer_id=i, customer_name=f'Customer {i:04d}', segment=random.choices(segments,[.55,.30,.15])[0], region=random.choice(regions), country=random.choice(countries), signup_date=(date(2023,1,1)+timedelta(days=random.randint(0,900))).isoformat()))
products=[]
for i in range(1,151):
    cat=random.choice(['Electronics','Home','Office','Apparel','Beauty'])
    price=round(random.uniform(15,900),2)
    products.append(dict(product_id=i, product_name=f'Product {i:03d}', category=cat, unit_cost=round(price*random.uniform(.45,.78),2), list_price=price))
orders=[]; items=[]; payments=[]; returns=[]
start=date(2024,1,1)
for oid in range(1,20001):
    c=random.choice(customers); od=start+timedelta(days=random.randint(0,970))
    status=random.choices(['Completed','Cancelled','Pending'],[.86,.08,.06])[0]
    orders.append(dict(order_id=oid, customer_id=c['customer_id'], order_date=od.isoformat(), status=status, channel=random.choice(['Web','Mobile','Partner']), region=c['region']))
    n=random.randint(1,4); total=0
    chosen=random.sample(products,n)
    for p in chosen:
        qty=random.randint(1,5); price=round(p['list_price']*random.uniform(.88,1.03),2); total += qty*price
        items.append(dict(order_id=oid, product_id=p['product_id'], quantity=qty, unit_price=price, discount=round(random.uniform(0,.20),3)))
    payments.append(dict(payment_id=oid, order_id=oid, payment_date=od.isoformat(), amount=round(total*(1-random.uniform(.0,.03)),2), method=random.choice(['Card','UPI','Bank','Wallet']), status='Paid' if status=='Completed' else random.choice(['Failed','Pending','Paid'])))
    if status=='Completed' and random.random()<.055:
        returns.append(dict(return_id=len(returns)+1, order_id=oid, return_date=(od+timedelta(days=random.randint(2,35))).isoformat(), reason=random.choice(['Damaged','Wrong Item','Changed Mind','Late Delivery']), refund_amount=round(total*random.uniform(.25,1.0),2)))
for name,rows,fields in [
 ('customers.csv',customers,['customer_id','customer_name','segment','region','country','signup_date']),
 ('products.csv',products,['product_id','product_name','category','unit_cost','list_price']),
 ('orders.csv',orders,['order_id','customer_id','order_date','status','channel','region']),
 ('order_items.csv',items,['order_id','product_id','quantity','unit_price','discount']),
 ('payments.csv',payments,['payment_id','order_id','payment_date','amount','method','status']),
 ('returns.csv',returns,['return_id','order_id','return_date','reason','refund_amount'])]:
    write_csv(os.path.join(ROOT,'commerce',name),rows,fields)

# Operations
ops=[]
for i in range(1,12001):
    ship=date(2024,1,1)+timedelta(days=random.randint(0,970))
    promised=ship+timedelta(days=random.randint(2,8))
    delivered=promised+timedelta(days=random.randint(-2,8)) if random.random()<.94 else ''
    ops.append(dict(shipment_id=i, ship_date=ship.isoformat(), promised_date=promised.isoformat(), delivered_date=delivered, warehouse=random.choice(['WH-A','WH-B','WH-C','WH-D']), carrier=random.choice(['Carrier-1','Carrier-2','Carrier-3']), region=random.choice(regions), weight_kg=round(random.uniform(.2,80),1), freight_cost=round(random.uniform(4,240),2), priority=random.choice(['Standard','Express','Critical'])))
write_csv(os.path.join(ROOT,'operations','shipments.csv'),ops,list(ops[0].keys()))

# Marketing
campaigns=[]
channels=['Search','Social','Email','Affiliate','Display']
for i in range(1,1201):
    d=date(2025,1,1)+timedelta(days=random.randint(0,500))
    spend=round(random.uniform(500,50000),2); impressions=random.randint(10000,900000); clicks=max(1,int(impressions*random.uniform(.004,.09))); conversions=max(1,int(clicks*random.uniform(.01,.18)))
    campaigns.append(dict(campaign_id=i,date=d.isoformat(),channel=random.choice(channels),region=random.choice(regions),spend=spend,impressions=impressions,clicks=clicks,conversions=conversions,revenue=round(conversions*random.uniform(45,600),2)))
write_csv(os.path.join(ROOT,'marketing','campaigns.csv'),campaigns,list(campaigns[0].keys()))

# HR
employees=[]
for i in range(1,1601):
    join=date(2021,1,1)+timedelta(days=random.randint(0,1500))
    employees.append(dict(employee_id=i,department=random.choice(['Sales','Operations','Finance','Technology','HR','Marketing']),level=random.choice(['Junior','Mid','Senior','Lead']),join_date=join.isoformat(),location=random.choice(['Bengaluru','Mumbai','Delhi','Pune','Chennai','Hyderabad']),base_salary=round(random.uniform(350000,2200000),2),performance_score=round(random.uniform(2.2,5.0),2),left_company='Y' if random.random()<.13 else 'N'))
write_csv(os.path.join(ROOT,'hr','employees.csv'),employees,list(employees[0].keys()))

# SQLite DB with commerce schema/data
path=os.path.join(ROOT,'commerce','commerce_lab.db')
if os.path.exists(path): os.remove(path)
conn=sqlite3.connect(path)
cur=conn.cursor()
cur.executescript('''
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, customer_name TEXT, segment TEXT, region TEXT, country TEXT, signup_date TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, unit_cost REAL, list_price REAL);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, channel TEXT, region TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price REAL, discount REAL);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, payment_date TEXT, amount REAL, method TEXT, status TEXT);
CREATE TABLE returns(return_id INTEGER PRIMARY KEY, order_id INTEGER, return_date TEXT, reason TEXT, refund_amount REAL);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_items_order ON order_items(order_id);
''')
for table, rows, fields in [('customers',customers,['customer_id','customer_name','segment','region','country','signup_date']),('products',products,['product_id','product_name','category','unit_cost','list_price']),('orders',orders,['order_id','customer_id','order_date','status','channel','region']),('order_items',items,['order_id','product_id','quantity','unit_price','discount']),('payments',payments,['payment_id','order_id','payment_date','amount','method','status']),('returns',returns,['return_id','order_id','return_date','reason','refund_amount'])]:
    q=f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join(['?']*len(fields))})"
    cur.executemany(q, [[r[f] for f in fields] for r in rows])
conn.commit(); conn.close()

print('Built datasets under',ROOT)

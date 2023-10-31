from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table,VARCHAR,JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID,ARRAY
from datetime import datetime
import pytz 
import uuid
timezonetash = pytz.timezone("Asia/Tashkent")
Base = declarative_base()






class Pages(Base):
    __tablename__ = 'pages'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    pages_crud = relationship('PageCrud',back_populates='crud_pages')

class PageCrud(Base):
    __tablename__='pagecrud'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    page_id = Column(Integer,ForeignKey('pages.id'))
    crud_pages = relationship('Pages',back_populates='pages_crud')
    crud_permission = relationship('Permissions',back_populates='permission_crud')


class Permissions(Base):
    __tablename__='permissions'
    id = Column(Integer,primary_key=True,index=True)
    pagecrud_id = Column(Integer,ForeignKey('pagecrud.id'))
    permission_crud = relationship('PageCrud',back_populates='crud_permission')
    role_id = Column(Integer,ForeignKey('roles.id'))
    permission_role = relationship('Roles',back_populates='role_permission')


class Roles(Base):
    __tablename__='roles'
    id = Column(Integer,primary_key=True,index=True)
    name= Column(String)
    status=Column(Integer,default=1)
    role_permission = relationship('Permissions',back_populates='permission_role')
    role_user = relationship('Users',back_populates='user_role')





class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=True)
    password = Column(String,nullable=True)
    phone_number = Column(String,nullable=True)
    full_name = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True),default=func.now())
    status = Column(Integer,default=0)
    is_client = Column(Integer,default=0)
    user_vs_order = relationship('Order',back_populates='order_vs_user')
    role_id = Column(Integer,ForeignKey("roles.id"),nullable=True)
    user_role = relationship('Roles',back_populates='role_user')
    tel_id = Column(BIGINT,nullable=True)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(length=255))
    status = Column(Integer,default=1)
    image = Column(String,nullable=True)
    category_vs_order = relationship('Order',back_populates='order_vs_category')
    category_vs_subcategory = relationship('SubCategory',back_populates='subcategory_vs_category')
    c_filling = relationship('Fillings',back_populates='filling')


"""
0=average
1=difficult
2=parties and weddings
"""

class Fillings(Base):
    __tablename__ = "fillings"
    id = Column(Integer,index=True,primary_key=True)
    name = Column(String)
    status = Column(Integer,default=1)
    ptype = Column(Integer,nullable=True)
    category_id = Column(Integer,ForeignKey('categories.id'))
    filling = relationship('Category',back_populates='c_filling')
    filler_order = relationship('OrderFilling',back_populates='filler')





"""
firstly_payment( 1 = yes, 0=no)
payment_type (0=cash, 1=payme, 2=click)
system (0=mastika otdel, 1=telegram bot, 2=sayt)
status (0=new created, 1= accepted, 2=rejected)
is_delivery (1=yes , 0=No)
"""

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True,index=True)
    order_user = Column(String,nullable=True)
    phone_number = Column(String,nullable=True)
    extra_number = Column(String,nullable=True)
    payment_type = Column(Integer,nullable=True)
    firstly_payment = Column(Integer,nullable=True)
    is_delivery = Column(Integer)
    comment = Column(String,nullable=True)
    reject_reason = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True),default=func.now())
    updated_at = Column(DateTime(timezone=True),nullable=True)
    deliver_date = Column(DateTime(timezone=True))
    status = Column(Integer,default=0)
    product_order = relationship('OrderProducts',back_populates='order_product')
    address  = Column(String,nullable=True)
    apartment =Column(String,nullable=True)
    home = Column(String,nullable=True)
    near_to = Column(String,nullable=True)
    department_id = Column(UUID(as_uuid=True),ForeignKey('departments.id'),nullable=True)
    order_br = relationship('Departments',back_populates='department_br')
    user_id = Column(Integer,ForeignKey('users.id'))
    order_vs_user = relationship('Users',back_populates='user_vs_order')
    category_id = Column(Integer,ForeignKey('categories.id'),nullable=True)
    order_vs_category = relationship('Category',back_populates='category_vs_order')
    order_vs_value = relationship('Value',back_populates='value_vs_order')
    lat = Column(String,nullable=True)
    long = Column(String,nullable=True)
    complexity = Column(Integer,nullable=True)
    packaging = Column(Integer,nullable=True)
    order_fill = relationship('OrderFilling',back_populates='fill_order')
    images = Column(ARRAY(String),nullable=True)
    color = Column(JSON,nullable=True)
    color_details = Column(String,nullable=True)



class OrderFilling(Base):
    __tablename__ = 'orderfilling'
    id = Column(Integer,primary_key=True,index=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    fill_order = relationship('Order',back_populates='order_fill')
    filling_id = Column(Integer,ForeignKey('fillings.id'))
    filler = relationship('Fillings',back_populates='filler_order')
    floor = Column(Integer,nullable=True)

class OrderProducts(Base):
    __tablename__='orderproducts'
    id = Column(Integer,primary_key=True,index=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    order_product = relationship('Order',back_populates='product_order')
    product_id = Column(UUID(as_uuid=True),ForeignKey('products.id'))
    order_vs_product = relationship('Products',back_populates='product_vs_order')
    comment = Column(String,nullable=True)
    amount = Column(Integer)
    floor = Column(Integer,nullable=True)
    portion = Column(Integer,nullable=True)





class ContentType(Base):
    __tablename__ = 'content_types'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(255))
    status = Column(Integer,default=1)
    contenttype_vs_subcategory = relationship('SubCategory',back_populates='subcategory_vs_contenttype')



class SubCategory(Base):
    __tablename__  = 'sub_categories'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    category_id = Column(Integer,ForeignKey('categories.id'))
    status = Column(Integer,default=1)
    subcategory_vs_category = relationship('Category',back_populates='category_vs_subcategory')
    contenttype_id = Column(Integer,ForeignKey('content_types.id'))
    subcategory_vs_contenttype = relationship('ContentType',back_populates='contenttype_vs_subcategory')
    subcat_vs_value = relationship('Value',back_populates='value_vs_subcat')
    subcat_vs_selval = relationship('SelectValues',back_populates='selval_vs_subcat')



class SelectValues(Base):
    __tablename__ = 'select_values'
    id =Column(Integer,primary_key=True,index=True)
    content = Column(String)
    value = Column(VARCHAR(length=255),nullable=True)
    status = Column(Integer,default=1)
    subcat_id = Column(Integer,ForeignKey('sub_categories.id'))
    selval_vs_subcat = relationship('SubCategory',back_populates='subcat_vs_selval')
    selval_vs_childselval = relationship('ChildSelVal',back_populates='childselval_vs_selval')
    select_vs_value = relationship('Value',back_populates='value_vs_select')





class ChildSelVal(Base):
    __tablename__ = 'childsel_values'
    id = Column(Integer,primary_key=True,index=True)
    selval_id = Column(Integer,ForeignKey('select_values.id'))
    childselval_vs_selval= relationship('SelectValues',back_populates='selval_vs_childselval')
    content = Column(VARCHAR(length=255))
    value = Column(String,nullable=True)
    status = Column(Integer,default=1)
    selchild_vs_value = relationship('Value',back_populates='value_vs_selchild')







class Value(Base):
    __tablename__ = 'values'
    id = Column(Integer,primary_key=True,index=True)
    content = Column(String,nullable=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    value_vs_order = relationship('Order',back_populates='order_vs_value')
    subcat_id = Column(Integer,ForeignKey('sub_categories.id'))
    value_vs_subcat = relationship('SubCategory',back_populates='subcat_vs_value')
    select_id = Column(Integer,ForeignKey('select_values.id'),nullable=True)
    value_vs_select = relationship('SelectValues',back_populates='select_vs_value')
    selchild_id = Column(Integer,ForeignKey('childsel_values.id'),nullable=True)
    value_vs_selchild = relationship('ChildSelVal',back_populates='selchild_vs_value')







class Branchs(Base):
    __tablename__='branchs'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    latitude = Column(Float,nullable=True)
    longtitude = Column(Float,nullable=True)
    country = Column(String,nullable=True)
    status = Column(Integer,default=0)
    department_br = relationship('Departments',back_populates='branch_dr')
    is_fabrica = Column(Integer,nullable=True)



class Departments(Base):
    __tablename__ = 'departments'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    department_br = relationship('Order',back_populates='order_br')
    branch_id = Column(UUID(as_uuid=True),ForeignKey('branchs.id'))
    branch_dr = relationship('Branchs',back_populates='department_br')
    origin = Column(Integer,default=0)
    status = Column(Integer,default=0)
    #supplier = relationship('Suppliers',back_populates='store')


class Groups(Base):
    __tablename__ = 'groups'
    id= Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    code=Column(String,nullable=True)
    group_r = relationship('Products',back_populates='product_r')
    status=Column(Integer,default=1)

class Products(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    status= Column(Integer,default=1)
    name = Column(String)
    productType = Column(String,nullable=True)
    group_id = Column(UUID(as_uuid=True),ForeignKey('groups.id'))
    product_r = relationship('Groups',back_populates='group_r')
    price = Column(Float,nullable=True)
    product_vs_order = relationship('OrderProducts',back_populates='order_vs_product')




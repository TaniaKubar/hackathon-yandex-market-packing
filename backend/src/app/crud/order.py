from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.exceptions import (NoProductError, OrderkeyAlreadyExistError,
                                OutOfStockError)
from app.crud.base import CRUDBase
from app.models.order import Order, OrderStatusEnum
from app.models.order_product import OrderProduct
from app.models.pack_variation import PackingVariation
from app.models.package import PackageProduct
from app.models.product import Product
from app.schemas.order import (ItemBase, OrderCreateSchema, OrderToUserSchema,
                               PackageSchema, ProductToUser)


class CRUDOrder(CRUDBase):
    async def add_order(
        self,
        order: OrderCreateSchema,
        session: AsyncSession,
    ) -> Order:
        new_order = Order()
        already_exist_orderkey = (await session.execute(
                select(Order).where(Order.orderkey == order.orderkey)
            )).scalars().first()
        if already_exist_orderkey:
            raise OrderkeyAlreadyExistError(orderkey=order.orderkey)
        new_order.orderkey = order.orderkey
        new_order.status = OrderStatusEnum.FORMING

        items = []
        for item in order.items:
            product = (await session.execute(
                select(Product).where(Product.sku == item.sku)
            )).scalars().first()
            if not product:
                raise NoProductError()
            if product.count < item.count:
                raise OutOfStockError()
            product.count -= item.count
            session.add(product)
            order_product = OrderProduct(
                orderkey=new_order.orderkey, sku=product.sku, count=item.count
            )
            items.append(order_product)
        new_order.products = items

        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)
        return new_order

    async def get_order_to_user(
        self,
        session: AsyncSession
    ) -> OrderToUserSchema:
        order = (await session.execute(
            select(Order)
            .options(joinedload(Order.products))
            .where(Order.status == OrderStatusEnum.WAITING)
        )).scalars().first()
        if not order:
            return OrderToUserSchema(
                status='No orders to pack'
                )
        order_to_user = OrderToUserSchema(
            orderkey=order.orderkey
        )

        goods = []
        for order_product in order.products:
            product = (await session.execute(
                select(Product)
                .options(joinedload(Product.cargotypes))
                .where(Product.sku == order_product.sku)
            )).scalars().first()
            fragility = False
            for cargotype in product.cargotypes:
                if cargotype.cargotype_tag == '360':
                    fragility = True
            product_to_user = ProductToUser(
                sku=product.sku,
                title=product.title,
                description=product.description,
                image=product.image,
                imei=product.need_imei,
                honest_sign=product.need_honest_sign,
                fragility=fragility
            )
            goods.append(product_to_user)
        order_to_user.goods = goods

        recomend_packing = []
        packing_variations = (await session.execute(
            select(PackingVariation)
            .options(joinedload(PackingVariation.packages))
            .where(PackingVariation.orderkey == order.orderkey)
        )).scalars().unique().all()
        for packing_variation in packing_variations:

            packages = []
            for package in packing_variation.packages:

                items_dict = {}
                package_to_user = PackageSchema(
                    cartontype=package.cartontype_tag
                )
                package_products = (await session.execute(
                    select(PackageProduct)
                    .where(PackageProduct.package_id == package.id)
                )).scalars().all()
                for product in package_products:
                    items_dict[product.product_sku] = (
                        items_dict.get(product.product_sku, 0) + 1
                    )
                items = []
                for item in items_dict.items():
                    items.append(ItemBase(
                        sku=item[0],
                        count=item[1]
                    ))
                package_to_user.items = items
                packages.append(package_to_user)
            recomend_packing.append(packages)
        order_to_user.recomend_packing = recomend_packing

        await self.set_order_status(
            orderkey=order.orderkey,
            status=OrderStatusEnum.COLLECT,
            session=session
        )
        return order_to_user

    async def set_order_status(
            self,
            orderkey: str,
            status: OrderStatusEnum,
            session: AsyncSession
    ) -> Order:
        order = (await session.execute(
            select(Order).where(Order.orderkey == orderkey)
        )).scalars().first()
        order.status = status
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order


order_crud = CRUDOrder(Order)

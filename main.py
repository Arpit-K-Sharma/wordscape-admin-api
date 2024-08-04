from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.controller.vendor_controller import vendor_route
from app.controller.purchase_order_controller import purchase_order_route
from app.controller.re_order_controller import re_order
from app.controller.inventory_controller import inventory_route
from app.controller.approved_orders_controller import approved_orders_route
from app.controller.user_controller import user_route
from app.controller.leftover_controller import left_over_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config.logger_config import get_logger
from app.controller.department_controller import department_route
from app.controller.staff_controller import staff_route
from app.controller.leave_controller import leave_route
from app.controller.holiday_controller import holiday_route
from app.controller.attendance_controller import attendance_route
from app.controller.payroll_controller import payroll_route
from app.controller.admin_auth_controller import admin_route
from app.middleware.exception_filter import httpexception_handler, exception_handler
from app.config.logger_config import get_logger
from app.service.payroll_service import PayrollService
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.controller.staff_auth_controller import staff_auth

from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
scheduler = AsyncIOScheduler()
logger = get_logger()


# CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inventory routes
app.include_router(vendor_route, tags=["vendors"])
app.include_router(purchase_order_route, tags=["purchase_order"])
app.include_router(re_order, tags=["re_order"])
app.include_router(inventory_route, tags=["inventory"])
app.include_router(approved_orders_route, tags=["approved_orders_route"])
app.include_router(user_route, tags=["user_name"])
app.include_router(left_over_router, tags=["leftover"])

# HR Routes
app.include_router(department_route, tags = ["department"])
app.include_router(staff_route, tags = ["staff"])
app.include_router(leave_route, tags = ["leave"])
app.include_router(holiday_route, tags = ["holiday"])
app.include_router(attendance_route, tags = ["attendance"])
app.include_router(payroll_route, tags = ["payroll"])

# Authentication Routes
app.include_router(admin_route, tags = ["admin login"])
app.include_router(staff_auth, tags=["staff login"])


#Exception Handler
app.add_exception_handler(HTTPException, httpexception_handler)
app.add_exception_handler(Exception, exception_handler)

# Root route 
@app.get("/ims")
async def root():
    return {"message": "Welcome to the Inventory ERP system"}

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(
        generate_monthly_payroll,
        CronTrigger(day="last", hour=23, minute=59),
        id="generate_monthly_payroll",
        name="Generate monthly payroll at the end of each month",
        replace_existing=True,
    )
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

async def generate_monthly_payroll():
    logger.info("generate_monthly_payroll started at %s", datetime.now())
    payroll_service = PayrollService()
    result = await payroll_service.generate_payroll()
    logger.info("Monthly payroll generation result: %s", result)
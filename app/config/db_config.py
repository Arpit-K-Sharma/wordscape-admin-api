import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://pukar:pukarpass@cluster0.2xqtwbl.mongodb.net/')

database = client.WORDSCAPE_PROD
collection = database.vendor
orders_collection = database.order
user_collection = database.user
cover_collection = database.coverTreatment
paper_collection = database.paper
inventory_collection = database.inventory

department_collection = database.department 
staff_collection = database.user
leave_collection = database.leave
holiday_collection = database.holiday
attendance_collection = database.attendance
payroll_collection = database.payroll



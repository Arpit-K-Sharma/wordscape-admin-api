import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://spandanbhattarai79:spandan123@spandan.ey3fvll.mongodb.net/')

database = client.Wordscape_Test
collection = database.vendor
database_erp = client.ERP_V2
orders_collection = database_erp.order
user_collection = database.user
cover_collection = database_erp.coverTreatment
paper_collection = database_erp.paper
inventory_collection = database.inventory

department_collection = database_erp.department 
staff_collection = database_erp.user
leave_collection = database_erp.leave
holiday_collection = database_erp.holiday
attendance_collection = database_erp.attendance
payroll_collection = database_erp.payroll


